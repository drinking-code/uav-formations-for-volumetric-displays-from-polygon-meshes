import numpy as np


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


def recursive_tuple(iterable):
    if not is_iterable(iterable):
        return iterable
    iterable = map(lambda value: recursive_tuple(value), iterable)
    return tuple(iterable)


def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError as te:
        return False


def get_faces_with_vertex_dict(mesh):
    """
    Returns a dictionary with all occurring vertices as keys and a list of faces that include a vertex as values
    :param mesh:
    :return:
    """
    faces_with_vertex = {}
    for face in mesh:
        for vertex in face:
            vertex = tuple(vertex)
            if vertex not in faces_with_vertex:
                faces_with_vertex[vertex] = []
            faces_with_vertex[vertex].append(face)
    return faces_with_vertex


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


def force_get_item(dictionary, key):
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


def triangle_surface_area(face):
    v = np.subtract(face[1], face[0])
    w = np.subtract(face[2], face[0])
    area = 0.5 * np.linalg.norm(np.cross(v, w))
    return area


def find_in_iterable(iterable, is_desired, add_to_found, find_all=False):
    for value in iterable:
        if not is_desired(value):
            continue
        add_to_found(value)
        if not find_all:
            return


def find_one_in_iterable(iterable, is_desired):
    found = []
    find_in_iterable(iterable, is_desired, lambda value: found.append(value))
    return found[0]


def sphere_line_intersection(sphere_center, radius, line):
    x_a, y_a, z_a = line[0]
    x_b, y_b, z_b = line[1]
    x_c, y_c, z_c = sphere_center
    a = (x_b - x_a) ** 2 + (y_b - y_a) ** 2 + (z_b - z_a) ** 2
    b = 2 * ((x_b - x_a) * (x_a - x_c) + (y_b - y_a) * (y_a - y_c) + (z_b - z_a) * (z_a - z_c))
    c = x_c ** 2 + y_c ** 2 + z_c ** 2 + x_a ** 2 + y_a ** 2 + z_a ** 2 - 2 * (x_c * x_a + y_c * y_a + z_c * z_a) - \
        radius ** 2
    expr_under_sqrt = b ** 2 - 4 * a * c
    if expr_under_sqrt < 0:
        return None

    points_of_intersection = []

    for sign in ([+1] if expr_under_sqrt == 0 else [+1, -1]):
        t = (-b + np.sqrt(expr_under_sqrt) * sign) / (2 * a)
        d = np.add(line[0], np.multiply(t, np.subtract(line[1], line[0])))
        points_of_intersection.append(list(d))

    return tuple(points_of_intersection)


def interpolate_vertices(a, b, x):
    return np.average([a, b], axis=0, weights=[1 - x, x])


def point_line_segment_distance(point, line):
    tangent = np.subtract(line[1], line[0])
    norm_tangent = np.divide(tangent, np.linalg.norm(tangent))

    a_parallel_distance = np.dot(np.subtract(line[0], point), norm_tangent)
    b_parallel_distance = np.dot(np.subtract(point, line[1]), norm_tangent)

    parallel_distance_clamped = np.maximum.reduce([a_parallel_distance, b_parallel_distance, 0])
    perpendicular_distance = np.cross(np.subtract(point, line[0]), norm_tangent)

    return np.hypot(parallel_distance_clamped, np.linalg.norm(perpendicular_distance))
