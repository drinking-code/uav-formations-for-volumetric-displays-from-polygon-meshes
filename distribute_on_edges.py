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
    groups = []
    edges = edges.copy()

    definite_terminators = []

    while edges:
        start_trace = edges.pop(0)

        def trace(start_trace, edges, direction=True):
            print(start_trace)
            adjacent_edges = []
            connecting_vertex = start_trace[1 if direction else 0]
            print(connecting_vertex)
            group = []

            for edge in edges:
                if list_contains(edge, connecting_vertex):
                    adjacent_edges.append(edge)

            print(adjacent_edges)
            if len(adjacent_edges) == 1:
                adjacent_edge = adjacent_edges[0]
                if direction:
                    group.append(adjacent_edge)
                else:
                    group.insert(0, adjacent_edge)

                del edges[edges.index(adjacent_edge)]
                print(adjacent_edges)
                group.extend(trace(adjacent_edge, edges, direction))
            else:
                definite_terminators.append(connecting_vertex)
                return group

        print(trace(start_trace, edges, True))
        print(trace(start_trace, edges, False))

        break
