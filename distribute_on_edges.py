from pprint import pprint

import numpy as np

from path_group import PathGroup
from path_group_utils.group_connected import group_connected
from path_group_utils.safe_placement_on_corners import safe_placement_on_corners


def distribute_on_edges(edges, density, min_distance, explicit_terminators=None):
    """
    Calculates points to represent the given edges. It partitions edges into groups which have a terminator placed at
    each end. These terminators are placed where a line does not connect to any other line or connects to more than one
    line. Terminators can also be explicitly set with the `explicit_terminators` parameter.
    :param edges: Edges on which points should be distributed on.
    :param density: Points per unit that should be placed. An edge of length 3 with a density of 1 will have 3 points
    placed. The same edge with a density of 2 will have 6 points placed.
    :param min_distance:
    :param explicit_terminators: Explicitly place a point here. The returned list will not include these points
    :return:
    """
    if explicit_terminators is None:
        explicit_terminators = []
    edges = edges.copy()
    groups, definite_terminators, non_terminators = group_connected(edges, explicit_terminators)
    groups = [PathGroup(group) for group in groups]

    target_distance = max(min_distance, 1 / density)
    vertices = safe_placement_on_corners(definite_terminators, non_terminators, groups, target_distance, min_distance)

    for path_group in groups:
        print(path_group.points_amount, path_group.points_start, path_group.points_end)

    return vertices