def find_vertex(self, is_desired, find_all=False):
    found = {}
    for vertex_id, vertex in self.vertices_map:
        if not is_desired(vertex):
            continue
        found[vertex_id] = vertex
        if not find_all:
            return found
    return found
