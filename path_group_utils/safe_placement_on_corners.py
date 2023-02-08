import numpy as np

from path_group import PathGroup
from utils import find_in_iterable, sphere_line_intersection


def safe_placement_on_corners(corners, non_corners, groups, target_distance, min_distance, append_new_point):
    vertices = []

    for intersection in non_corners:
        pass  # todo

    for terminator in corners:
        path_groups: list[PathGroup] = []
        # indicates if the edge with the terminator is in the first (False) or last (True) edge of the group
        last_vertex_is_terminator = []
        find_in_iterable(
            groups,
            lambda group: any([
                starting_path_group := terminator == group.get_first_vertex(),
                ending_path_group := terminator == group.get_last_vertex(),
                last_vertex_is_terminator.append(ending_path_group)
                if starting_path_group or ending_path_group else None
            ]),
            path_groups.append,
            True
        )

        def point_from_terminator(path_group, reverse, distance):
            return path_group.get_point_at_length(
                distance
                if not reverse else
                path_group.total_length - distance
            )

        # todo: loop for as long as sphere_line_intersections exist for point farthest away from terminator

        vertex_at_min_dist_from_terminator = point_from_terminator(
            path_groups[0],
            last_vertex_is_terminator[0],
            path_groups[0].set_target_distance(target_distance, min_distance)
        )
        append_new_point(vertex_at_min_dist_from_terminator)
        if last_vertex_is_terminator[0]:
            path_groups[0].points_end = vertex_at_min_dist_from_terminator
        else:
            path_groups[0].points_start = vertex_at_min_dist_from_terminator

        for next_path_group, last_vertex_is_terminator in zip(path_groups[1:], last_vertex_is_terminator[1:]):
            next_path_group_touching_edge = next_path_group.paths[len(next_path_group.paths) - 1] \
                if last_vertex_is_terminator else next_path_group.paths[0]

            possible_points = sphere_line_intersection(
                vertex_at_min_dist_from_terminator,
                target_distance,
                next_path_group_touching_edge
            )

            if not next_path_group.target_distance:
                next_path_group.set_target_distance(target_distance, min_distance)

            if not possible_points:
                points = point_from_terminator(
                    next_path_group,
                    last_vertex_is_terminator,
                    next_path_group.target_distance
                )
                append_new_point(points)
                if last_vertex_is_terminator:
                    next_path_group.points_end = points
                else:
                    next_path_group.points_start = points
                continue

            if type(possible_points) is not tuple:
                possible_points = tuple([possible_points])

            possible_points = list(filter(next_path_group.is_on_path, possible_points))
            possible_vertices_distance_from_terminator = list(map(
                lambda vertex: (vertex, np.linalg.norm(np.subtract(terminator, vertex))),
                possible_points
            ))
            possible_vertices_distance_from_terminator = list(filter(
                lambda data: (distance := data[1], distance >= next_path_group.target_distance)[1],
                possible_vertices_distance_from_terminator
            ))
            possible_vertices_distance_from_terminator = list(sorted(
                possible_vertices_distance_from_terminator,
                key=lambda data: (distance := data[1], distance)[1]
            ))
            possible_points = list(map(
                lambda data: (vertex := data[0], vertex)[1],
                possible_vertices_distance_from_terminator
            ))

            if not possible_points:
                # means either:
                # - the point(s) on path of minimum distance to the point on first path is too close to terminator
                # - the points are not actually on the line segment
                points = point_from_terminator(
                    next_path_group,
                    last_vertex_is_terminator,
                    next_path_group.target_distance
                )
                append_new_point(points)
                if last_vertex_is_terminator:
                    next_path_group.points_end = points
                else:
                    next_path_group.points_start = points
            else:
                points = possible_points[0]
                append_new_point(points)
                if last_vertex_is_terminator:
                    next_path_group.points_end = points
                else:
                    next_path_group.points_start = points

    return vertices
