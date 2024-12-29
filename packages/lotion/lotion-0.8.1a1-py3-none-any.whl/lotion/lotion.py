import os
from logging import Logger, getLogger
from typing import Type, TypeVar

from notion_client import Client
from notion_client.errors import APIResponseError, HTTPResponseError

from .base_page import BasePage
from .block import Block, BlockFactory
from .filter.builder import Builder
from .filter.condition.cond import Cond
from .filter.condition.prop import Prop
from .page.page_id import PageId
from .properties.cover import Cover
from .properties.multi_select import MultiSelect, MultiSelectElement, MultiSelectElements
from .properties.properties import Properties
from .properties.property import Property
from .properties.select import Select, Selects

NOTION_API_ERROR_BAD_GATEWAY = 502

T = TypeVar("T", bound="BasePage")
S = TypeVar("S", bound=Select)
M = TypeVar("M", bound=MultiSelect)


class AppendBlockError(Exception):
    def __init__(self, block_id: str, blocks: list[dict], e: Exception) -> None:
        self.block_id = block_id
        self.blocks = blocks
        self.e = e
        super().__init__(f"block_id: {block_id}, blocks: {blocks}, error: {e}")


class NotionApiError(Exception):
    def __init__(
        self,
        page_id: str | None = None,
        database_id: str | None = None,
        e: APIResponseError | HTTPResponseError | None = None,
        properties: Properties | dict | None = None,
    ) -> None:
        self.database_id = database_id
        self.e = e
        self.properties = properties

        message = ""
        if e is not None:
            message += f", error: {e}"
        if page_id is not None:
            message += f"page_id: {page_id}"
        if database_id is not None:
            message += f"database_id: {database_id}"
        if properties is not None:
            properties_ = properties.__dict__() if isinstance(properties, Properties) else properties
            message += f", properties: {properties_}"
        super().__init__(message)


class Lotion:
    def __init__(self, client: Client, max_retry_count: int = 3, logger: Logger | None = None) -> None:
        self.client = client
        self.max_retry_count = max_retry_count
        self._logger = logger or getLogger(__name__)

    @staticmethod
    def get_instance(max_retry_count: int = 3, logger: Logger | None = None) -> "Lotion":
        client = Client(auth=os.getenv("NOTION_SECRET"))
        return Lotion(client, max_retry_count=max_retry_count, logger=logger)

    def retrieve_page(self, page_id: str, cls: Type[T] = BasePage) -> T:
        """指定されたページを取得する"""
        page_entity = self.__retrieve_page(page_id=page_id)
        return self.__convert_page_model(page_entity=page_entity, include_children=True, cls=cls)

    def update_page(self, page_id: str, properties: list[Property] | None = None) -> None:
        """指定されたページを更新する"""
        update_properties = Properties(values=properties or [])
        self.__update(page_id=page_id, properties=update_properties)

    def update(self, page: T) -> T:
        """ページを更新する"""
        if page.is_created():
            self.__update(page_id=page.id, properties=Properties(values=page.properties.values))
            return page
        created_page = self.create_page(page)
        return created_page

    def retrieve_comments(self, page_id: str) -> list[dict]:
        """指定されたページのコメントを取得する"""
        comments = self.client.comments.list(
            block_id=page_id,
        )
        return comments["results"]

    def create_page_in_database(
        self,
        database_id: str,
        cover: Cover | None = None,
        properties: list[Property] | None = None,
        blocks: list[Block] | None = None,
        cls: Type[T] = BasePage,
    ) -> T:
        """データベース上にページを新規作成する"""
        page = self.__create_page(
            database_id=database_id,
            cover=cover.__dict__() if cover is not None else None,
            properties=(
                Properties(values=properties).exclude_for_update().__dict__() if properties is not None else {}
            ),
        )
        if blocks is not None:
            self.append_blocks(block_id=page["id"], blocks=blocks)
        return self.retrieve_page(page_id=page["id"], cls=cls)

    def create_page(self, page: T) -> T:
        """ページを新規作成する"""
        return self.create_page_in_database(
            database_id=page._get_own_database_id(),
            cover=page.cover,
            properties=page.properties.values,
            blocks=page.block_children,
            cls=type(page),
        )

    def retrieve_database(  # noqa: PLR0913
        self,
        database_id: str,
        filter_param: dict | None = None,
        include_children: bool | None = None,
        cls: Type[T] = BasePage,
    ) -> list[T]:
        """指定されたデータベースのページを取得する"""
        results = self._database_query(database_id=database_id, filter_param=filter_param)
        pages: list[T] = []
        for page_entity in results:
            page = self.__convert_page_model(
                page_entity=page_entity,
                include_children=include_children or False,
                cls=cls,
            )
            pages.append(page)
        return pages

    def retrieve_pages(
        self,
        cls: Type[T],
        filter_param: dict | None = None,
        include_children: bool | None = None,
    ) -> list[T]:
        return self.retrieve_database(
            database_id=cls._get_database_id(),
            filter_param=filter_param,
            include_children=include_children,
            cls=cls,
        )

    def find_page_by_title(
        self,
        database_id: str,
        title: str,
        title_key_name: str = "名前",
        cls: Type[T] = BasePage,
    ) -> T | None:
        """タイトルだけをもとにデータベースのページを取得する"""
        filter_param = Builder.create().add(Prop.RICH_TEXT, title_key_name, Cond.EQUALS, title).build()
        results = self.retrieve_database(
            database_id=database_id,
            filter_param=filter_param,
            cls=cls,
        )
        if len(results) == 0:
            return None
        if len(results) > 1:
            warning_message = f"Found multiple pages with the same title: {title}"
            self._logger.warning(warning_message)
        return results[0]

    def find_page_by_unique_id(
        self,
        database_id: str,
        unique_id: int,
        cls: Type[T] = BasePage,
    ) -> T | None:
        """UniqueIdをもとにデータベースのページを取得する"""
        unique_id_prop_name = None
        base_page = self._fetch_sample_page(database_id=database_id, cls=cls)
        for propety in base_page.properties.values:
            if propety.type == "unique_id":
                unique_id_prop_name = propety.name
                break

        if unique_id_prop_name is None:
            raise ValueError("unique_id property is not found")

        # filter_param = FilterBuilder.build_simple_equal_unique_id_condition(name=unique_id_prop_name, number=unique_id)
        filter_param = Builder.create().add(Prop.ID, unique_id_prop_name, Cond.EQUALS, unique_id).build()
        results = self.retrieve_database(
            database_id=database_id,
            filter_param=filter_param,
            cls=cls,
        )
        if len(results) == 0:
            return None
        return results[0]

    def _database_query(
        self,
        database_id: str,
        filter_param: dict | None = None,
        start_cursor: str | None = None,
    ) -> dict:
        if filter_param is None:
            return self._database_query_without_filter(database_id=database_id, start_cursor=start_cursor)
        results = []
        while True:
            data = self.__database_query(
                database_id=database_id,
                filter_param=filter_param,
                start_cursor=start_cursor,
            )
            results += data.get("results")
            if not data.get("has_more"):
                return results
            start_cursor = data.get("next_cursor")

    def _database_query_without_filter(self, database_id: str, start_cursor: str | None = None) -> dict:
        results = []
        while True:
            data = self.__database_query(
                database_id=database_id,
                start_cursor=start_cursor,
            )
            results += data.get("results")
            if not data.get("has_more"):
                return results
            start_cursor = data.get("next_cursor")

    def list_blocks(self, block_id: str) -> list[Block]:
        """指定されたブロックの子ブロックを取得する"""
        return self.__get_block_children(page_id=block_id)

    def append_block(self, block_id: str, block: Block) -> None:
        """指定されたブロックに子ブロックを追加する"""
        return self.append_blocks(block_id=block_id, blocks=[block])

    def append_blocks(self, block_id: str, blocks: list[Block]) -> None:
        """指定されたブロックに子ブロックを追加する"""
        return self.__append_block_children(
            block_id=block_id,
            children=[b.to_dict(for_create=True) for b in blocks],
        )

    def append_comment(self, page_id: str, text: str) -> dict:
        """指定されたページにコメントを追加する"""
        return self.client.comments.create(
            parent={"page_id": page_id},
            rich_text=[{"text": {"content": text}}],
        )

    def clear_page(self, page_id: str) -> None:
        """指定されたページのブロックを削除する"""
        blocks = self.list_blocks(block_id=page_id)
        for block in blocks:
            if block.id is None:
                raise ValueError(f"block_id is None: {block}")
            self.client.blocks.delete(block_id=block.id)

    def remove_page(self, page_id: str) -> None:
        """指定されたページを削除する"""
        self.__archive(page_id=page_id)

    def fetch_select(self, cls: Type[T], prop_type: Type[S], value: str) -> S:
        """指定されたデータベースのセレクトを取得する"""
        pages = self.retrieve_pages(cls)
        selects: list[S] = []
        for page in pages:
            prop = page.get_prop(prop_type)
            selects.append(prop)
        selects = list(set(selects))
        for select in selects:
            print(select.selected_name)
        filtered_selects = [s for s in selects if s.selected_name == value]
        if len(filtered_selects) == 0:
            raise ValueError(f"Select not found in database: cls={cls.__name__}, prop={prop.__name__}, value={value}")
        return filtered_selects[0]

    def fetch_multi_select(self, cls: Type[T], prop_cls: Type[M], value: str | list[str]) -> M:
        """
        指定されたデータベースのマルチセレクトを取得する。
        ただし現在のデータベースで利用されていないマルチセレクトを取得することはできない。
        """
        value = value if isinstance(value, list) else [value]
        pages = self.retrieve_pages(cls)
        elements: list[MultiSelectElement] = []
        for page in pages:
            multi_select = page.get_prop(prop_cls)
            elements.extend(multi_select.values)
        elements = list(set(elements))
        return prop_cls.from_elements(name=prop_cls.PROP_NAME, elements=[e for e in elements if e.name in value])

    def __append_block_children(self, block_id: str, children: list[dict], retry_count: int = 0) -> None:
        try:
            _ = self.client.blocks.children.append(block_id=block_id, children=children)
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__append_block_children(block_id=block_id, children=children, retry_count=retry_count + 1)
            raise NotionApiError(page_id=block_id, e=e) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__append_block_children(block_id=block_id, children=children, retry_count=retry_count + 1)
            raise NotionApiError(page_id=block_id, e=e) from e
        except TypeError as e:
            raise AppendBlockError(block_id=block_id, blocks=children, e=e) from e

    def __convert_page_model(
        self,
        page_entity: dict,
        include_children: bool | None = None,
        cls: Type[T] = BasePage,
    ) -> T:
        include_children = (
            include_children if include_children is not None else True
        )  # 未指定の場合はchildrenを取得する
        id_ = PageId(page_entity["id"])
        block_children = self.__get_block_children(page_id=id_.value) if include_children else []
        return cls.from_data(data=page_entity, block_children=block_children)

    def __retrieve_page(self, page_id: str, retry_count: int = 0) -> dict:
        try:
            return self.client.pages.retrieve(page_id=page_id)
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__retrieve_page(page_id=page_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__retrieve_page(page_id=page_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e) from e

    def __get_block_children(self, page_id: str) -> list[Block]:
        block_entities = self.__list_blocks(block_id=page_id)["results"]
        return [BlockFactory.create(b) for b in block_entities]

    def __list_blocks(self, block_id: str, retry_count: int = 0) -> dict:
        try:
            return self.client.blocks.children.list(block_id=block_id)
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__list_blocks(block_id=block_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=block_id, e=e) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__list_blocks(block_id=block_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=block_id, e=e) from e

    def __archive(self, page_id: str, retry_count: int = 0) -> dict:
        try:
            return self.client.pages.update(
                page_id=page_id,
                archived=True,
            )
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__archive(page_id=page_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__archive(page_id=page_id, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e) from e

    def __update(self, page_id: str, properties: Properties, retry_count: int = 0) -> None:
        try:
            _ = self.client.pages.update(
                page_id=page_id,
                properties=properties.exclude_for_update().__dict__(),
            )
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__update(page_id=page_id, properties=properties, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e, properties=properties) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__update(page_id=page_id, properties=properties, retry_count=retry_count + 1)
            raise NotionApiError(page_id=page_id, e=e, properties=properties) from e

    def __create_page(
        self,
        database_id: str,
        properties: dict,
        cover: dict | None = None,
        retry_count: int = 0,
    ) -> dict:
        try:
            return self.client.pages.create(
                parent={"type": "database_id", "database_id": database_id},
                cover=cover,
                properties=properties,
            )
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                self.__create_page(
                    database_id=database_id,
                    properties=properties,
                    cover=cover,
                    retry_count=retry_count + 1,
                )
            raise NotionApiError(database_id=database_id, e=e, properties=properties) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                self.__create_page(
                    database_id=database_id,
                    properties=properties,
                    cover=cover,
                    retry_count=retry_count + 1,
                )
            raise NotionApiError(database_id=database_id, e=e, properties=properties) from e

    def _fetch_sample_page(self, database_id: str, cls: Type[T] = BasePage) -> T:
        """指定されたデータベースのサンプルページを取得する"""
        data = self.__database_query(database_id=database_id, page_size=1)
        pages: list[dict] = data["results"]
        if len(pages) == 0:
            raise ValueError(f"Database has no page. Please create any page. database_id: {database_id}")
        return self.__convert_page_model(page_entity=pages[0], include_children=False, cls=cls)

    def __database_query(
        self,
        database_id: str,
        start_cursor: str | None = None,
        filter_param: dict | None = None,
        page_size: int = 100,
        retry_count: int = 0,
    ) -> dict:
        try:
            if filter_param is None:
                return self.client.databases.query(
                    database_id=database_id,
                    start_cursor=start_cursor,
                    page_size=page_size,
                )
            return self.client.databases.query(
                database_id=database_id,
                start_cursor=start_cursor,
                filter=filter_param,
                page_size=page_size,
            )
        except APIResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__database_query(
                    database_id=database_id,
                    start_cursor=start_cursor,
                    filter_param=filter_param,
                    retry_count=retry_count + 1,
                )
            raise NotionApiError(database_id=database_id, e=e) from e
        except HTTPResponseError as e:
            if self.__is_able_retry(status=e.status, retry_count=retry_count):
                return self.__database_query(
                    database_id=database_id,
                    start_cursor=start_cursor,
                    filter_param=filter_param,
                    retry_count=retry_count + 1,
                )
            raise NotionApiError(database_id=database_id, e=e) from e

    def __is_able_retry(self, status: int, retry_count: int) -> bool:
        return status == NOTION_API_ERROR_BAD_GATEWAY and retry_count < self.max_retry_count
