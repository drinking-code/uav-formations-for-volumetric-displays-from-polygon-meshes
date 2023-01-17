import math
from pprint import pprint

import numpy as np

from angle import angle_between_vectors_anchor
from utils import list_contains, find_in_iterable


def is_not_near_points(point, points, distance):
    if list(point) == [False, False, False]:
        return False
    for subject in points:
        if np.linalg.norm(np.subtract(subject, point)) < distance:
            return False
    return True


def area_of_radii_on_surface(corner_points, edge_points, distance, faces):  # Estimates area (likely overestimates)
    area = 0
    overlapped_area = 0
    # assume every point on edge adds a half circle area
    for index, point_a in enumerate(edge_points):
        area += (math.pi * distance ** 2) / 2
        for point_b in edge_points[index + 1:]:
            overlapped_area += overlap_area(point_b, point_a, distance) / 2

    for index, point_a in enumerate(corner_points):
        faces_with_point = []
        find_in_iterable(faces, lambda face: list_contains(face, point_a), faces_with_point.append, True)
        for face in faces_with_point:
            other_points = list(filter(lambda vertex: point_a != vertex, face))
            angle = angle_between_vectors_anchor(other_points[0], other_points[1], point_a)
            area += (math.pi * distance ** 2) * (angle / 360)
            for point_b in corner_points[index + 1:]:
                overlapped_area += overlap_area(point_b, point_a, distance) * (angle / 360)
    return area - overlapped_area


def overlap_area(p1, p2, r):
    distance = np.linalg.norm(np.subtract(p2, p1))
    if distance > 2 * r:
        return 0
    elif distance == 0:
        return math.pi * r ** 2
    else:
        d = distance
        part1 = r ** 2 * math.acos((d ** 2) / (2 * d * r))
        part3 = 0.5 * math.sqrt((-d + 2 * r) * (d + 2 * r) * d ** 2)
        return part1 * 2 - part3
