from pprint import pprint

from utils import replace_values_in_list, recursive_list


def move_vertex(self, vector, target):
    vector_key = self.vertices_map[vector]
    vector_ref = self.vertices_map[vector_key]
    del self.vertices_map[vector_key]
    replace_values_in_list(vector_ref, target)
    # reassign new value
    self.vertices_map[vector_key] = vector_ref


def replace_vertices(self, vectors, target):
    # find and remove edges between given vectors
    # find edges that contain one of the given vectors -> interpolate values
    vectors = recursive_list(vectors)
    edges_in_vector_group = []
    for index, vector_a in enumerate(vectors):
        for vector_b in vectors[index:]:
            edge = None
            if [vector_a, vector_b] in self.edges_map:
                edge = self.edges_map[[vector_a, vector_b]]
            if [vector_b, vector_a] in self.edges_map:
                edge = self.edges_map[[vector_b, vector_a]]
            if edge is None:
                continue
            edges_in_vector_group.append(edge)
            for key in self.edge_data:
                del self.edge_data[key][edge]

    edges_half_in_vector_group = {}
    for edge_id, edge in self.edges_map:
        edge = list(edge)
        edge = self.edges_map[self.edges_map[edge]]
        existing_vector_filter = list(filter(lambda vertex: vertex in vectors, edge))
        if len(existing_vector_filter) != 1:
            continue
        edge_vector_outside_vectors = list(filter(lambda vertex: vertex is not existing_vector_filter[0], edge))[0]
        edge_vector_outside_vectors_tuple = tuple(edge_vector_outside_vectors)
        if edge_vector_outside_vectors_tuple not in edges_half_in_vector_group:
            edges_half_in_vector_group[edge_vector_outside_vectors_tuple] = []
        edges_half_in_vector_group[edge_vector_outside_vectors_tuple].append(edge)

    pprint(edges_half_in_vector_group)

    for vector in vectors:
        self.move_vertex(vector, target)

    pprint(edges_half_in_vector_group)
