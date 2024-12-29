from typing import Type, Any, TypeVar, cast

from ..properties.property import Property
from ..lotion import Lotion

P = TypeVar("P", bound=Property)


def notion_database(database_id: str):
    """
    クラスデコレータ: データベースIDを引数として受け取り、
    自動的に BasePage を継承させ、アノテーションの属性をプロパティ化する。
    """

    def decorator(cls):
        # 元の初期化をオーバーライドしてアノテーション属性をプロパティ化
        original_init = getattr(cls, "__init__", lambda self: None)

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            # クラスアノテーションに基づいてプロパティを設定
            for attr_name, attr_type in cls.__annotations__.items():

                def make_getter(name, typ: Type[P]):
                    def getter(self) -> Any:
                        # print(typ, name)  # デバッグ出力
                        result = self.get_prop(typ)  # `self.get()` は任意の実装
                        return cast(typ, result)

                    return getter

                def make_setter(name, typ):
                    def setter(self, value: Any):
                        if not isinstance(value, typ):
                            raise TypeError(f"Expected {typ} for {name}, got {type(value)}")
                        # print(f"Setting {name} of type {typ} to {value}")  # デバッグ出力
                        self.set_prop(value)  # `set` メソッドを直接呼び出す

                    return setter

                # プロパティを作成してクラスに設定
                setattr(cls, attr_name, property(make_getter(attr_name, attr_type), make_setter(attr_name, attr_type)))

        # デコレータ引数で渡された database_id をクラス属性として設定
        setattr(cls, "DATABASE_ID", database_id)

        cls.__init__ = new_init
        cls.__module__ = cls.__module__

        return cls

    return decorator
