from utils import list_contains, get_item_or_return_none


class CombinedDict:
    """
    Multiple values for one key.
    Each key has (the same) categories of values, which are set when calling __init__().
    Each category has an entry for each existing key (can be None if no value was set for key-category combination)
    Get and set with syntax `my_combined_dict[<key>][<category>]` or `my_combined_dict[<category>][<key>]`
    """

    def __init__(self, categories):
        self.categories = categories
        self.data = {}
        for category in self.categories:
            self.data[category] = {}

    def __getitem__(self, item):
        if list_contains(self.categories, item):
            return TempSubDict(self.data[item], lambda key, value: self.__setitem__(key, value, item))
        else:
            item_values = {
                category: get_item_or_return_none(self.data[category], item)
                for category in self.categories
            }
            return TempSubDict(item_values, lambda category, value: self.__setitem__(item, value, category))

    def __setitem__(self, key, value, category=None):
        if category:
            for iter_category in self.categories:
                if category == iter_category:
                    self.data[iter_category][key] = value
                else:
                    get_item_or_return_none(self.data[iter_category], key)
        # todo

    def __str__(self):
        categories = [
            '  ' + category + ': ' + self.data[category].__str__()
            for category in self.categories
        ]
        string = "CombinedDicts [\n" + "\n".join(categories) + "\n]"
        return string

    def __len__(self):
        return self.data[self.categories[0]].values().__len__()


class TempSubDict(dict):
    def __init__(self, dictionary, setitem_callback):
        dictionary = super().__init__(dictionary.items())
        self.dictionary = dictionary
        self.setitem_callback = setitem_callback

    def __setitem__(self, key, value):
        return self.setitem_callback(key, value)
