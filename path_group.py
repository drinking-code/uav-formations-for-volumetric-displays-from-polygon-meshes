import numpy as np

from utils import list_contains, find_one_in_iterable, interpolate_vertices, point_line_segment_distance


class PathGroup:
    """
    Group of connected paths (each a line between two points).
    """

    def __init__(self, paths):
        self.paths = paths
        paths_vectors = [np.subtract(path[0], path[1]) for path in self.paths]
        self.lengths = [np.linalg.norm(vector) for vector in paths_vectors]
        self.total_length = np.sum(self.lengths)
        self.percentages = []
        for index, length in enumerate(self.lengths):
            last_percentage = self.percentages[index - 1] if index > 0 else 0
            self.percentages.append(min(1.0, (length / self.total_length) + last_percentage))

    def get_first_vertex(self):
        first_path = self.paths[0]
        second_path = self.paths[1]
        return find_one_in_iterable(first_path, lambda vertex: not list_contains(second_path, vertex))

    def get_last_vertex(self):
        last_path = self.paths[len(self.paths) - 1]
        second_last_path = self.paths[len(self.paths) - 2]
        return find_one_in_iterable(last_path, lambda vertex: not list_contains(second_last_path, vertex))

    def get_point_at_percent(self, percentage):
        pass

    def get_point_at_length(self, length):
        length_copy = length
        path_index = 0
        for path_length in self.lengths:
            if length_copy < path_length:
                break
            length_copy -= path_length
            path_index += 1
        path = self.paths[path_index]
        is_reversed = (not list_contains(self.paths[path_index + 1], path[1])) \
            if path_index + 1 < len(self.paths) \
            else (not list_contains(self.paths[path_index - 1], path[0]))
        first_vertex = path[0] if not is_reversed else path[1]
        last_vertex = path[1] if not is_reversed else path[0]
        vertex = interpolate_vertices(first_vertex, last_vertex, length_copy / self.lengths[path_index])
        return list(vertex)

    def is_on_path(self, point, error=1e-06):
        distance = np.amin([point_line_segment_distance(point, line_seg) for line_seg in self.paths])
        return distance <= error

    def __str__(self):
        return 'PathGroup ' + self.paths.__str__()
