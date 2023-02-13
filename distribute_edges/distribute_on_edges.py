from pprint import pprint

import numpy as np

from .path_group import PathGroup
from .path_group_utils.group_connected import group_connected
from .path_group_utils.safe_placement_on_corners import safe_placement_on_corners


def distribute_on_edges(edges, density, min_distance, explicit_terminators=None, new_point=None):
    """
    Calculates points to represent the given edges. It partitions edges into groups which have a terminator placed at
    each end. These terminators are placed where a line does not connect to any other line or connects to more than one
    line. Terminators can also be explicitly set with the `explicit_terminators` parameter.
    :param edges: Edges on which points should be distributed on.
    :param density: Points per unit that should be placed. An edge of length 3 with a density of 1 will have 3 points
    placed. The same edge with a density of 2 will have 6 points placed.
    :param min_distance:
    :param explicit_terminators: Explicitly place a point here. The returned list will not include these points
    :param new_point: Function to be called after the coordinates of a new point are determined
    :return:
    """
    if explicit_terminators is None:
        explicit_terminators = []
    edges = edges.copy()
    groups, definite_terminators, non_terminators = group_connected(edges, explicit_terminators)
    groups = [PathGroup(group) for group in groups]

    target_distance = max(min_distance, 1 / density)
    points = []

    def append_new_point(point):
        points.append(point)
        if new_point:
            new_point(point)

    safe_placement_on_corners(definite_terminators, non_terminators, groups,
                              target_distance, min_distance, append_new_point)

    for path_group in groups:
        if not path_group.points_amount:
            continue
        percentage_steps = list(np.arange(0, 1, 1 / path_group.points_amount))
        del percentage_steps[0]
        if path_group.points_start and percentage_steps:
            del percentage_steps[0]
        if path_group.points_end and percentage_steps:
            del percentage_steps[len(percentage_steps) - 1]

        for percentage in percentage_steps:
            point = path_group.get_point_at_percent(percentage)
            append_new_point(point)

    return points
