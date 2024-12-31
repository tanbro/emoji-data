from typing import Any, Dict, Generic, Iterator, MutableMapping, Tuple, Type, TypeVar

__all__ = ["BaseDictContainer"]

KT = TypeVar("KT")
VT = TypeVar("VT")


class BaseDictContainer(type, Generic[KT, VT]):
    __data_dict__: MutableMapping[KT, VT]

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):
        cls.__data_dict__ = {}
        return super().__new__(cls, name, bases, attrs)

    def __setitem__(self, key: KT, value: VT):
        self.__data_dict__[key] = value

    def __delitem__(self, key: KT):
        del self.__data_dict__[key]

    def __getitem__(self, key: KT) -> VT:
        return self.__data_dict__[key]

    def __contains__(self, key: KT) -> bool:
        return key in self.__data_dict__

    def __iter__(self) -> Iterator[KT]:
        yield from self.__data_dict__

    def __len__(self) -> int:
        return len(self.__data_dict__)
