import numpy as np


def angle_between_vectors_anchor(vector_u, vector_v, vector_anchor=None):
    """
    Calculates the angle between vector_u and vector_v, taking vector_anchor as the origin
    :returns: angle θ
    """
    if vector_anchor is None:
        vector_anchor = [0, 0, 0]
    vector_u, vector_v, vector_anchor = np.array(vector_u), np.array(vector_v), np.array(vector_anchor)
    vector_u -= vector_anchor
    vector_v -= vector_anchor
    cos_θ = np.dot(vector_u, vector_v) / (np.linalg.norm(vector_u) * np.linalg.norm(vector_v))
    # clip to mitigate floating-point computation errors
    cos_θ = np.clip(cos_θ, -1, 1)
    θ_rad = np.arccos(cos_θ)
    θ = np.degrees(θ_rad)
    if θ > 180:
        θ = 180 * 2 - θ
    return θ


def vectors_plane_angle(vector, plane):
    normal = np.cross(np.subtract(plane[1], plane[0]), np.subtract(plane[2], plane[0]))
    θ = angle_between_vectors_anchor(normal, vector)
    if θ > 90:
        θ = 90 * 2 - θ
    return θ


def triangle_surface_area(face):
    v = np.subtract(face[1], face[0])
    w = np.subtract(face[2], face[0])
    area = 0.5 * np.linalg.norm(np.cross(v, w))
    return area


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


def point_is_on_line_segment(point, line, error=1e-06):
    return point_line_segment_distance(point, line) <= error


def project_point_onto_plane(point, face):
    normal = np.cross(np.subtract(face[1], face[0]), np.subtract(face[2], face[0]))
    normal = np.divide(normal, np.linalg.norm(normal))

    t = np.subtract(np.dot(normal, face[0]), np.dot(normal, point))
    return np.add(point, t * normal)


def point_plane_distance(point, face):
    return np.linalg.norm(np.subtract(project_point_onto_plane(point, face), point))


def point_is_on_face(point, face, error=1e-06):
    if point_plane_distance(point, face) > error:
        return False

    point = project_point_onto_plane(point, face)
    v0 = np.subtract(face[2], face[0])
    v1 = np.subtract(face[1], face[0])
    v2 = np.subtract(point, face[0])

    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)

    inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return u >= 0 and v >= 0 and u + v < 1
