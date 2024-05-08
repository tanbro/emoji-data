from typing import Any, Dict, Generator, Generic, MutableMapping, Tuple, Type, TypeVar

__all__ = ["BaseDictContainer"]

KT = TypeVar("KT")
VT = TypeVar("VT")


class BaseDictContainer(type, Generic[KT, VT]):
    __data__: MutableMapping[KT, VT]

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):
        cls.__data__ = {}
        return super().__new__(cls, name, bases, attrs)

    def __setitem__(self, key: KT, value: VT):
        self.__data__[key] = value

    def __delitem__(self, key: KT):
        del self.__data__[key]

    def __getitem__(self, key: KT) -> VT:
        return self.__data__[key]

    def __contains__(self, key: KT) -> bool:
        return key in self.__data__

    def __iter__(self) -> Generator[KT, None, None]:
        yield from self.__data__

    def __len__(self) -> int:
        return len(self.__data__)
