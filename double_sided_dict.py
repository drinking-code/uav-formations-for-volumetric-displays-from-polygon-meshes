class DoubleSidedMap:
    def __init__(self, dictionary, make_hashable):
        self.make_hashable = make_hashable
        self.key_value = dictionary
        self.value_key = {}
        for key, value in dictionary:
            self.value_key[make_hashable(value)] = key

    def clear(self, make_hashable=None):
        if make_hashable is not None:
            self.make_hashable = make_hashable
        self.key_value.clear()
        self.value_key.clear()

    def __getitem__(self, key):
        if key in self.key_value:
            return self.key_value[key]
        elif key in self.value_key:
            return self.value_key[key]
        else:
            return None

    def __setitem__(self, key, value):
        del self[key]
        self.key_value[key] = value
        self.value_key[self.make_hashable(value)] = key

    def __delitem__(self, key):
        original_value = self.key_value[key]
        del self.value_key[self.make_hashable(original_value)]
        del self.key_value[key]

    def __ior__(self, other):
        for key, value in other:
            self.value_key[self.make_hashable(value)] = key
            self.key_value[key] = value
