import numpy as np

from utils import list_contains, find_one_in_iterable


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
        pass

    def __str__(self):
        return 'PathGroup ' + self.paths.__str__()
