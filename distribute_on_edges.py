from pprint import pprint

from utils import list_contains


def distribute_on_edges(edges, density, explicit_terminators=None):
    """
    Calculates points to represent the given edges. It partitions edges into groups which have a terminator placed at
    each end. These terminators are placed where a line does not connect to any other line or connects to more than one
    line. Terminators can also be explicitly set with the `explicit_terminators` parameter.
    :param edges: Edges on which points should be distributed on.
    :param density: Points per unit that should be placed. An edge of length 3 with a density of 1 will have 3 points
    placed. The same edge with a density of 2 will have 6 points placed.
    :param explicit_terminators: Explicitly place a point here. The returned list will not include these points
    :return:
    """
    if explicit_terminators is None:
        explicit_terminators = []
    edges = edges.copy()
    groups, definite_terminators = group_connected(edges, explicit_terminators)

    return groups


def group_connected(edges, explicit_terminators):
    groups = []
    edges = edges.copy()

    definite_terminators = []

    while edges:
        def trace(start_trace, direction=True):
            adjacent_edges = []
            target_vertex_index = 1 if direction else 0
            traced_edges = []
            connecting_vertex = start_trace[target_vertex_index]

            if connecting_vertex in explicit_terminators or connecting_vertex in definite_terminators:
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

            return traced_edges

        start_with = edges.pop(0)
        edges_forward = trace(start_with, True)
        edges_backward = trace(start_with, False)
        edges_backward.reverse()
        group = edges_backward + [start_with] + edges_forward
        groups.append(group)

    return groups, definite_terminators
