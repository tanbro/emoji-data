class BaseDictContainer(type):
    def __new__(mcs, name, bases, attrs):  # pylint:disable=bad-mcs-classmethod-argument
        mcs._data = dict()
        return super().__new__(mcs, name, bases, attrs)

    def __setitem__(self, key, value):  # pylint: disable=C0203
        self._data[key] = value

    def __delitem__(self, key):  # pylint: disable=C0203
        del self._data[key]

    def __getitem__(self, key):  # pylint: disable=C0203
        return self._data[key]

    def __contains__(self, key):  # pylint: disable=C0203
        return key in self._data

    def __iter__(self):  # pylint: disable=bad-mcs-method-argument
        for k, v in self._data.items():  # pylint: disable=invalid-name
            yield k, v

    def __len__(self):  # pylint: disable=C0203
        return len(self._data)
