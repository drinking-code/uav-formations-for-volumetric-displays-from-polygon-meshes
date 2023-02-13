def get_item_or_return_none(dictionary, key):
    """
    Creates an entry with value key if key does not yet exist and returns value (None, or the pre-existing value).
    It is guaranteed that the dictionary has the key after calling this function.
    :param dictionary:
    :param key:
    :return:
    """
    if key not in dictionary:
        dictionary[key] = None
    return dictionary[key]
