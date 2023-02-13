from pprint import pprint

from utils import list_contains


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
