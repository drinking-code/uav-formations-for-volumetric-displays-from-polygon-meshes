from utils import list_contains, force_get_item


class CombinedDicts:
    """
    Multiple values for one key
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
                category: force_get_item(self.data[category], item)
                for category in self.categories
            }
            return TempSubDict(item_values, lambda category, value: self.__setitem__(item, value, category))

    def __setitem__(self, key, value, category=None):
        if category:
            for iter_category in self.categories:
                if category == iter_category:
                    self.data[iter_category][key] = value
                else:
                    force_get_item(self.data[iter_category], key)
        # todo

    def __str__(self):
        categories = [
            '  ' + category + ': ' + self.data[category].__str__()
            for category in self.categories
        ]
        string = "CombinedDicts [\n" + "\n".join(categories) + "\n]"
        return string


class TempSubDict(dict):
    def __init__(self, dictionary, setitem_callback):
        dictionary = super().__init__(dictionary.items())
        self.dictionary = dictionary
        self.setitem_callback = setitem_callback

    def __setitem__(self, key, value):
        return self.setitem_callback(key, value)
