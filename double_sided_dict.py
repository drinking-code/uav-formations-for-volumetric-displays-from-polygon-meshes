from pprint import pprint

from utils import find_in_iterable


class DoubleSidedMap:
    def __init__(self, dictionary, make_hashable):
        self.make_hashable = make_hashable
        self.key_value = dictionary
        self.value_key = {}
        for key, value in dictionary.items():
            self.value_key[make_hashable(value)] = key
        self.key_value_pointers = {}
        self.value_key_pointers = {}

    def __iter__(self):
        yield from self.key_value.items()

    def clear(self, make_hashable=None):
        if make_hashable is not None:
            self.make_hashable = make_hashable
        self.key_value.clear()
        self.value_key.clear()

    def find_by_value(self, is_desired, find_all=False):
        found = {}

        def add_to_found(value):
            found[self[value]] = self[self[value]]

        find_in_iterable(self.key_value.values(), is_desired, add_to_found, find_all)
        return found

    def __contains__(self, other):
        other_hashable = self.make_hashable(other)
        return other_hashable in self.value_key or other_hashable in self.key_value

    def __getitem__(self, key):
        key_hashable = try_to_otherwise_return_value(self.make_hashable, key)
        if key_hashable in self.key_value:
            return (self.key_value_pointers[key_hashable]
                    if key_hashable in self.key_value_pointers
                    else self.key_value[key_hashable])
        elif key_hashable in self.value_key:
            return (self.value_key_pointers[key_hashable]
                    if key_hashable in self.value_key_pointers
                    else self.value_key[key_hashable])
        else:
            return None

    def __setitem__(self, key, value):
        if key in self.key_value:
            del self[key]
        self.key_value[key] = value
        self.value_key[self.make_hashable(value)] = key

    def __delitem__(self, key):
        key_hashable = try_to_otherwise_return_value(self.make_hashable, key)
        original_value = self.key_value[key_hashable]
        del self.value_key[self.make_hashable(original_value)]
        del self.key_value[key_hashable]

    def point_key_to(self, key, key_of_value):
        """
        Points key to other (existing) value and deletes current value.
        Also points the old hashable value to the new key.
        :param key:
        :param key_of_value:
        :return:
        """
        old_value_hashable = try_to_otherwise_return_value(self.make_hashable, self.key_value[key])
        del self[key]
        self.value_key_pointers[old_value_hashable] = key_of_value
        self.key_value_pointers[key] = self.key_value[key_of_value]

    def __ior__(self, other):
        for key, value in other:
            self.value_key[self.make_hashable(value)] = key
            self.key_value[key] = value


def try_to_otherwise_return_value(function, value):
    try:
        value = function(value)
    finally:
        return value
