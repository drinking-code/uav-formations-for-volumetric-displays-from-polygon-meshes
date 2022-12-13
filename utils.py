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
    :param lists_subject: list of lists of vectors
    :param value: vector to find
    :return: list of lists of vectors that contain the vector
    """
    return list(filter(lambda subject: list_contains(subject, value), lists_subject))


def recursive_list(iterable):
    if not is_iterable(iterable):
        return iterable
    iterable = map(lambda value: recursive_list(value), iterable)
    return list(iterable)


def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError as te:
        return False


def get_faces_with_vertex_dict(mesh):
    faces_with_vertex = {}
    for face in mesh:
        for vertex in face:
            vertex = tuple(vertex)
            if vertex not in faces_with_vertex:
                faces_with_vertex[vertex] = []
            faces_with_vertex[vertex].append(face)
    return faces_with_vertex


def replace_values_in_list(target, replacement):
    for index in enumerate(target):
        if type(target[index]) is list:
            replace_values_in_list(target[index], replacement[index])
        target[index] = replacement[index]
