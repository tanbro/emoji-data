class BaseDictContainer(type):
    def __new__(cls, name, bases, attrs):
        cls._data = dict()
        return super().__new__(cls, name, bases, attrs)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        for k, v in self._data.items():
            yield k, v

    def __len__(self):
        return len(self._data)
