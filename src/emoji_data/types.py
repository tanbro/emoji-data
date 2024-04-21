from typing import Generic, TypeVar, Generator, MutableMapping

__all__ = ["BaseDictContainer"]

TK = TypeVar("TK")
TV = TypeVar("TV")


class BaseDictContainer(Generic[TK, TV], type):
    def __new__(cls, name, bases, attrs):
        cls.__data__: MutableMapping[TK, TV] = {}  # type:ignore[annotation-unchecked]
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
