import numpy as np

from utils import list_contains, find_one_in_iterable, interpolate_vertices, point_is_on_line_segment


class PathGroup:
    """
    Group of connected paths (each a line between two points).
    """

    def __init__(self, paths):
        self.paths = paths
        paths_vectors = [np.subtract(path[0], path[1]) for path in self.paths]
        self.lengths = [np.linalg.norm(vector) for vector in paths_vectors]
        self.total_length = np.sum(self.lengths)
        self.points_amount = None
        self.density = None
        self.target_distance = None
        self.percentages = []
        for index, length in enumerate(self.lengths):
            last_percentage = self.percentages[index - 1] if index > 0 else 0
            self.percentages.append(min(1.0, (length / self.total_length) + last_percentage))

        self.points_start = None
        self.points_end = None

    def set_density(self, density, min_distance):
        self.density = 1 / self.set_target_distance(1 / density, min_distance)
        return self.density

    def set_target_distance(self, target_distance, min_distance):
        self.points_amount = int(np.round(self.total_length / target_distance))
        self.target_distance = self.total_length / self.points_amount
        while self.target_distance < min_distance:
            self.points_amount -= 1
            self.target_distance = self.total_length / self.points_amount
        return target_distance

    def get_first_vertex(self):
        if len(self.paths) == 1:
            return self.paths[0][0]
        else:
            first_path = self.paths[0]
            second_path = self.paths[1]
            return find_one_in_iterable(first_path, lambda vertex: not list_contains(second_path, vertex))

    def get_last_vertex(self):
        if len(self.paths) == 1:
            return self.paths[0][1]
        else:
            last_path = self.paths[len(self.paths) - 1]
            second_last_path = self.paths[len(self.paths) - 2]
            return find_one_in_iterable(last_path, lambda vertex: not list_contains(second_last_path, vertex))

    def get_point_at_percent(self, percentage):
        return self.get_point_at_length(self.total_length * percentage)

    def get_point_at_length(self, length):
        length_copy = length
        path_index = 0
        for path_length in self.lengths:
            if length_copy < path_length:
                break
            length_copy -= path_length
            path_index += 1
        path_index = min(path_index, len(self.paths) - 1)
        path = self.paths[path_index]
        is_reversed = (not list_contains(self.paths[path_index + 1], path[1])) \
            if path_index + 1 < len(self.paths) \
            else (not list_contains(self.paths[path_index - 1], path[0]))
        first_vertex = path[0] if not is_reversed else path[1]
        last_vertex = path[1] if not is_reversed else path[0]
        vertex = interpolate_vertices(first_vertex, last_vertex, length_copy / self.lengths[path_index])
        return list(vertex)

    def is_on_path(self, point):
        return any([point_is_on_line_segment(point, line_seg) for line_seg in self.paths])

    def __str__(self):
        return 'PathGroup ' + self.paths.__str__()
