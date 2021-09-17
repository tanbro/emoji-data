class BaseDictContainer(type):
    def __new__(cls, name, bases, attrs):
        cls.__data__ = dict()
        return super().__new__(cls, name, bases, attrs)

    def __setitem__(self, key, value):
        self.__data__[key] = value

    def __delitem__(self, key):
        del self.__data__[key]

    def __getitem__(self, key):
        return self.__data__[key]

    def __contains__(self, key):
        return key in self.__data__

    def __iter__(self):
        yield from self.__data__

    def __len__(self):
        return len(self.__data__)
