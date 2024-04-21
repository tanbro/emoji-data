from typing import Any, Dict, Generator, Generic, MutableMapping, Tuple, Type, TypeVar

__all__ = ["BaseDictContainer"]

TK = TypeVar("TK")
TV = TypeVar("TV")


class BaseDictContainer(type, Generic[TK, TV]):
    __data__: MutableMapping[TK, TV]

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):
        cls.__data__ = {}
        return super().__new__(cls, name, bases, attrs)

    def __setitem__(self, key: TK, value: TV):
        self.__data__[key] = value

    def __delitem__(self, key: TK):
        del self.__data__[key]

    def __getitem__(self, key: TK) -> TV:
        return self.__data__[key]

    def __contains__(self, key: TK) -> bool:
        return key in self.__data__

    def __iter__(self) -> Generator[TK, None, None]:
        yield from self.__data__

    def __len__(self) -> int:
        return len(self.__data__)
