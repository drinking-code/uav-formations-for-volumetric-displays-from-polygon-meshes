import math
from pprint import pprint

import numpy as np

from utils import recursive_list, point_is_on_line_segment, recursive_tuple
from unique_vertices import unique_edges as calc_unique_edges


def is_not_near_points(point, points, distance):
    if list(point) == [False, False, False]:
        return False
    for subject in points:
        if np.linalg.norm(np.subtract(subject, point)) < distance:
            return False
    return True


def excluded_area_on_face(face, points, distance):  # Estimates area (likely overestimates)
    area = 0
    overlapped_area = 0
    circle_area = math.pi * distance ** 2
    face = recursive_list(face)
    edges = calc_unique_edges([face], True)
    points_on_edges = list(filter(lambda point: any([point_is_on_line_segment(point, edge) for edge in edges]), points))
    # remove duplicate points (points that were found for two or more sides)
    points_on_edges = list(set(recursive_tuple(points_on_edges)))
    for index, point in enumerate(points_on_edges):
        for vertex in face:
            is_corner = np.linalg.norm(np.subtract(vertex, point)) < distance / 2
            area += circle_area * (.25 if is_corner else .5)
            for point_b in points_on_edges[index + 1:]:
                overlapped_area += overlap_area(point_b, point, distance)  # shouldn't be this much, maybe divide by 2
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
