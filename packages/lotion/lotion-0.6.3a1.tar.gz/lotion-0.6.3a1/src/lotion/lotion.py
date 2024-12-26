import os
from logging import Logger, getLogger

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

    def retrieve_page(self, page_id: str) -> BasePage:
        """指定されたページを取得する"""
        page_entity = self.__retrieve_page(page_id=page_id)
        return self.__convert_page_model(page_entity=page_entity, include_children=True)

    def update_page(self, page_id: str, properties: list[Property] | None = None) -> None:
        """指定されたページを更新する"""
        update_properties = Properties(values=properties or [])
        self.__update(page_id=page_id, properties=update_properties)

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
    ) -> BasePage:
        """データベース上にページを新規作成する"""
        page = self.__create_page(
            database_id=database_id,
            cover=cover.__dict__() if cover is not None else None,
            properties=(Properties(values=properties).__dict__() if properties is not None else {}),
        )
        if blocks is not None:
            self.append_blocks(block_id=page["id"], blocks=blocks)
        return self.retrieve_page(page_id=page["id"])

    def retrieve_database(  # noqa: PLR0913
        self,
        database_id: str,
        filter_param: dict | None = None,
        include_children: bool | None = None,
    ) -> list[BasePage]:
        """指定されたデータベースのページを取得する"""
        results = self._database_query(database_id=database_id, filter_param=filter_param)
        pages: list[BasePage] = []
        for page_entity in results:
            page = self.__convert_page_model(
                page_entity=page_entity,
                include_children=include_children or False,
            )
            pages.append(page)
        return pages

    def find_page_by_title(
        self,
        database_id: str,
        title: str,
        title_key_name: str = "名前",
    ) -> BasePage | None:
        """タイトルだけをもとにデータベースのページを取得する"""
        filter_param = Builder.create().add(Prop.RICH_TEXT, title_key_name, Cond.EQUALS, title).build()
        results = self.retrieve_database(
            database_id=database_id,
            filter_param=filter_param,
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
    ) -> BasePage | None:
        """UniqueIdをもとにデータベースのページを取得する"""
        unique_id_prop_name = None
        base_page = self._fetch_sample_page(database_id=database_id)
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

    def fetch_all_selects(self, database_id: str, name: str) -> Selects:
        """指定されたデータベースのセレクト一覧を取得する"""
        results = self.retrieve_database(database_id=database_id)
        selects = []
        for page in results:
            for prop in page.properties.values:
                if isinstance(prop, Select) and prop.name == name and not prop.is_empty():
                    selects.append(prop)
        return Selects(list(set(selects)))

    def fetch_select(self, database_id: str, name: str, status_name: str) -> Select:
        """
        指定されたデータベースのセレクトを取得する。
        ただし現在のデータベースで利用されていないセレクトを取得することはできない。
        """
        selects = self.fetch_all_selects(database_id=database_id, name=name)
        return selects.get(status_name)

    def fetch_all_multi_select_elements(self, database_id: str, name: str) -> MultiSelectElements:
        """指定されたデータベースのマルチセレクト一覧を取得する"""
        pages = self.retrieve_database(database_id=database_id)
        results: list[MultiSelectElement] = []
        for page in pages:
            for prop in page.properties.values:
                if isinstance(prop, MultiSelect) and prop.name == name:
                    results.extend(prop.values)
        return MultiSelectElements(list(set(results)))

    def fetch_multi_select(self, database_id: str, name: str, multi_select_names: list[str]) -> MultiSelect:
        """
        指定されたデータベースのマルチセレクトを取得する。
        ただし現在のデータベースで利用されていないマルチセレクトを取得することはできない。
        """
        all_elements = self.fetch_all_multi_select_elements(database_id=database_id, name=name)
        multi_element_list = all_elements.get(multi_select_names)
        return MultiSelect(name=name, values=multi_element_list)

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
    ) -> BasePage:
        include_children = (
            include_children if include_children is not None else True
        )  # 未指定の場合はchildrenを取得する
        id_ = PageId(page_entity["id"])
        block_children = self.__get_block_children(page_id=id_.value) if include_children else []
        return BasePage.from_data(data=page_entity, block_children=block_children)

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

    def _fetch_sample_page(self, database_id: str) -> BasePage:
        """指定されたデータベースのサンプルページを取得する"""
        data = self.__database_query(database_id=database_id, page_size=1)
        pages: list[dict] = data.get("results")
        if len(pages) == 0:
            raise ValueError(f"Database has no page. Please create any page. database_id: {database_id}")
        return self.__convert_page_model(page_entity=pages[0], include_children=False)

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
