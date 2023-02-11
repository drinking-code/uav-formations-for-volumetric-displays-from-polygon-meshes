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
    overlapped_area = 0
    circle_area = math.pi * distance ** 2
    face = recursive_list(face)
    edges = calc_unique_edges([face], True)
    points_on_edges = [
        point
        for points_on_edge in [filter(lambda point: point_is_on_line_segment(point, edge), points) for edge in edges]
        for point in points_on_edge
    ]
    # remove duplicate points (points that were found for two or more sides)
    points_on_edges = list(set(recursive_tuple(points_on_edges)))
    for point in points_on_edges:
        for vertex in face:
            if np.linalg.norm(np.subtract(vertex, point)) < distance / 2:
                overlapped_area += circle_area * .25
            else:
                overlapped_area += circle_area * .5

    return overlapped_area
