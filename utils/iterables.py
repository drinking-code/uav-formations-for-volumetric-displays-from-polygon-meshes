def return_value(value):
    return value


def list_contains(list_subject, value, transform=return_value):
    for subject in list_subject:
        if transform(subject) == value:
            return True
    return False


def lists_list_filter_contains(lists_subject, value):
    """
    Finds all lists (of vectors) that contain a list (vector) in a list (list of lists of vectors)
    :param lists_subject: list of lists of vectors (list of faces)
    :param value: vector to find
    :return: list of lists of vectors that contain the vector
    """
    return list(filter(lambda subject: list_contains(subject, value), lists_subject))


def recursive_list(iterable):
    if not is_iterable(iterable):
        return iterable
    iterable = map(lambda value: recursive_list(value), iterable)
    return list(iterable)


def recursive_tuple(iterable):
    if not is_iterable(iterable):
        return iterable
    iterable = map(lambda value: recursive_tuple(value), iterable)
    return tuple(iterable)


def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False


def replace_values_in_list(target, replacement):
    for index, value in enumerate(target):
        if type(value) is list:
            replace_values_in_list(value, replacement[index])
        target[index] = replacement[index]


def zip_common(*dicts):
    if not dicts:
        return
    for i in set(dicts[0]).intersection(*dicts[1:]):
        yield (i,) + tuple(d[i] for d in dicts)


def find_in_iterable(iterable, is_desired, add_to_found, find_all=False):
    for value in iterable:
        if not is_desired(value):
            continue
        add_to_found(value)
        if not find_all:
            return


def find_one_in_iterable(iterable, is_desired):
    found = []
    find_in_iterable(iterable, is_desired, found.append)
    return found[0]
