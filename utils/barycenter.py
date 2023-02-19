import copy

import numpy as np
from panda3d.core import Triangulator3

from utils import triangle_surface_area, angle_between_vectors_anchor


def barycenter_point_set(points):
    sorted_points = simple_polygon_from_points(points)
    triangles = triangulate(sorted_points)
    triangle_centers = [np.average(points, axis=0) for points in triangles]
    triangle_areas = [triangle_surface_area(triangle) for triangle in triangles]
    return np.divide(np.sum(np.multiply(triangle_centers, triangle_areas), axis=0), np.sum(triangle_areas))


def triangulate(points):
    triangulator = Triangulator3()
    points_indices = [triangulator.addVertex(point[0], point[1], point[2]) for point in points]
    for index in points_indices:
        triangulator.addPolygonVertex(index)
    triangulator.triangulate()
    triangles = []
    for i in range(triangulator.getNumTriangles()):
        a, b, c = triangulator.getTriangleV0(i), triangulator.getTriangleV1(i), triangulator.getTriangleV2(i)
        triangles.append([points[a], points[b], points[c]])
    return triangles


# https://stackoverflow.com/a/59293807/10256886
def simple_polygon_from_points(points: list[list]):
    points = copy.deepcopy(points)

    # Get "centre of mass"
    centre = np.average(points, axis=0)

    def spherical(point, centre):
        point = np.subtract(point, centre)
        projected_vector = point.copy()
        projected_vector[2] = 0
        φ = 90 - angle_between_vectors_anchor(projected_vector, point)
        θ = 90 - angle_between_vectors_anchor(projected_vector, [1, 0, 0])
        r = np.linalg.norm(point)
        return φ, θ, r

    # Sort by polar angle and distance, centered at this centre of mass.
    for point in points:
        φ, θ, r = spherical(point, centre)
        point.append(φ)
        point.append(θ)
        point.append(r)
    points = sorted(points, key=lambda point: point[3] * 1e10 + point[4] * 1e5 + point[5])
    # Throw away the temporary polar coordinates
    points = [point[:3] for point in points]

    return points
