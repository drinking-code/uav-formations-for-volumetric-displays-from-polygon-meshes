from pprint import pprint

from path_group import PathGroup
from utils import list_contains, find_one_in_iterable, find_in_iterable


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
    vertices = []

    for intersection in non_terminators:
        pass  # todo
    for terminator in definite_terminators:
        path_groups: list[PathGroup] = []
        # indicates if the edge with the terminator is in the first (False) or last (True) edge of the group
        path_group_is_reversed = []
        find_in_iterable(
            groups,
            lambda group: any([
                starting_path_group := terminator == group.get_first_vertex(),
                ending_path_group := terminator == group.get_last_vertex(),
                path_group_is_reversed.append(ending_path_group)
                if starting_path_group or ending_path_group else None
            ]),
            path_groups.append,
            True
        )
        first_path_group = path_groups[0]
        vertex_at_min_dist_from_terminator = first_path_group.get_point_at_length(
            target_distance
            if not path_group_is_reversed[0] else
            first_path_group.total_length - target_distance
        )
        vertices.append(vertex_at_min_dist_from_terminator)
        # print(path_groups, path_group_is_reversed)
        # print(terminator)
    return vertices


def group_connected(edges, explicit_terminators):
    groups = []
    edges = edges.copy()

    definite_terminators = []
    non_terminators = []

    while edges:
        def trace(start_trace, direction=True):
            adjacent_edges = []
            target_vertex_index = 1 if direction else 0
            traced_edges = []
            connecting_vertex = start_trace[target_vertex_index]

            if connecting_vertex in explicit_terminators or connecting_vertex in definite_terminators:
                if connecting_vertex not in definite_terminators:
                    definite_terminators.append(connecting_vertex)
                return traced_edges

            for edge in edges:
                if list_contains(edge, connecting_vertex):
                    adjacent_edges.append(edge)

            if len(adjacent_edges) == 1:
                adjacent_edge = adjacent_edges[0]
                if direction:
                    traced_edges.append(adjacent_edge)
                else:
                    traced_edges.insert(0, adjacent_edge)

                # flip the next edge if it has the connecting vertex on the "wrong" direction
                if adjacent_edge[target_vertex_index] == connecting_vertex:
                    adjacent_edge.reverse()

                del edges[edges.index(adjacent_edge)]
                traced_edges.extend(trace(adjacent_edge, direction))
            elif len(adjacent_edges) == 0:
                if connecting_vertex not in definite_terminators:
                    definite_terminators.append(connecting_vertex)
            else:  # if len(adjacent_edges) > 1:
                if connecting_vertex not in definite_terminators and connecting_vertex not in explicit_terminators:
                    non_terminators.append(connecting_vertex)

            return traced_edges

        start_with = edges.pop(0)
        edges_forward = trace(start_with, True)
        edges_backward = trace(start_with, False)
        edges_backward.reverse()
        group = edges_backward + [start_with] + edges_forward
        groups.append(group)

    return groups, definite_terminators, non_terminators
