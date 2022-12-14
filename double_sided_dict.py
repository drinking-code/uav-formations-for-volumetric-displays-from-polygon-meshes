class DoubleSidedMap:
    def __init__(self, dictionary, make_hashable):
        self.make_hashable = make_hashable
        self.key_value = dictionary
        self.value_key = {}
        for key, value in dictionary.items():
            self.value_key[make_hashable(value)] = key

    def __iter__(self):
        yield from self.key_value.items()

    def clear(self, make_hashable=None):
        if make_hashable is not None:
            self.make_hashable = make_hashable
        self.key_value.clear()
        self.value_key.clear()

    def __contains__(self, other):
        other_hashable = self.make_hashable(other)
        return other_hashable in self.value_key or other_hashable in self.key_value

    def __getitem__(self, key):
        key_hashable = self.make_hashable(key)
        if key_hashable in self.key_value:
            return self.key_value[key_hashable]
        elif key_hashable in self.value_key:
            return self.value_key[key_hashable]
        else:
            return None

    def __setitem__(self, key, value):
        del self[key]
        self.key_value[key] = value
        self.value_key[self.make_hashable(value)] = key

    def __delitem__(self, key):
        key_hashable = self.make_hashable(key)
        original_value = self.key_value[key_hashable]
        del self.value_key[self.make_hashable(original_value)]
        del self.key_value[key_hashable]

    def __ior__(self, other):
        for key, value in other:
            self.value_key[self.make_hashable(value)] = key
            self.key_value[key] = value
