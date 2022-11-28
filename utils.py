def return_value(value):
    return value


def list_contains(list_subject, value, transform=return_value):
    return list(map(lambda subject: transform(subject) == value, list_subject))


def lists_list_filter_contains(lists_subject, value):
    """
    Finds all lists (of vectors) that contain a list (vector) in a list (list of lists of vectors)
    :param lists_subject: list of lists of vectors
    :param value: vector to find
    :return: list of lists of vectors that contain the vector
    """
    return list(filter(lambda subject: any(list_contains(subject, value)), lists_subject))


def recursive_list(iterable):
    if not is_iterable(iterable):
        return iterable
    iterable = map(lambda value: recursive_list(value), iterable)
    return list(iterable)


def is_iterable(value):
    try:
        value_iterator = iter(value)
        return True
    except TypeError as te:
        return False
