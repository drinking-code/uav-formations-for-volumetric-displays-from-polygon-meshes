# https://github.com/marmakoide/mesh-blue-noise-sampling
import numpy

from scipy.spatial.distance import pdist, squareform
from scipy.spatial import KDTree

import matplotlib.pyplot as plot


def mesh_area(triangle_list):
    N = numpy.cross(triangle_list[:, 1] - triangle_list[:, 0], triangle_list[:, 2] - triangle_list[:, 0], axis=1)
    N_norm = numpy.sqrt(numpy.sum(N ** 2, axis=1))
    N_norm *= .5
    return N_norm


reflection = numpy.array([[0., -1.], [-1., 0.]])


def triangle_point_picking(triangle_list):
    # Compute uniform distribution over [0, 1]x[0, 1] lower triangle
    X = numpy.random.random((triangle_list.shape[0], 2))
    t = numpy.sum(X, axis=1) > 1
    X[t] = numpy.dot(X[t], reflection) + 1.

    # Map the [0, 1]x[0, 1] lower triangle to the actual triangles
    ret = numpy.einsum('ijk,ij->ik', triangle_list[:, 1:] - triangle_list[:, 0, None], X)
    ret += triangle_list[:, 0]
    return ret


def uniform_sample_mesh(triangle_list, triangle_area_list, sample_count):
    # Normalize the sum of area of each triangle to 1
    triangle_area = triangle_area_list / numpy.sum(triangle_area_list)

    '''
    For each sample
      * Pick a triangle with probability proportional to its surface area
      * pick a point on that triangle with uniform probability
    '''

    triangle_id_list = numpy.random.choice(triangle_list.shape[0], size=sample_count, p=triangle_area)
    return triangle_point_picking(triangle_list[triangle_id_list])


def blue_noise_sample_elimination(point_list, mesh_surface_area, sample_count):
    # Parameters
    alpha = 8
    rmax = numpy.sqrt(mesh_surface_area / ((2 * sample_count) * numpy.sqrt(3.)))

    # Compute a KD-tree of the input point list
    kdtree = KDTree(point_list)

    # Compute the weight for each sample
    D = numpy.minimum(squareform(pdist(point_list)), 2 * rmax)
    D = (1. - (D / (2 * rmax))) ** alpha

    W = numpy.zeros(point_list.shape[0])
    for i in range(point_list.shape[0]):
        W[i] = sum(D[i, j] for j in kdtree.query_ball_point(point_list[i], 2 * rmax) if i != j)

    # Pick the samples we need
    heap = sorted((w, i) for i, w in enumerate(W))

    id_set = set(range(point_list.shape[0]))
    while len(id_set) > sample_count:
        # Pick the sample with the highest weight
        w, i = heap.pop()
        id_set.remove(i)

        neighbor_set = set(kdtree.query_ball_point(point_list[i], 2 * rmax))
        neighbor_set.remove(i)
        heap = [(w - D[i, j], j) if j in neighbor_set else (w, j) for w, j in heap]
        heap.sort()

    # Job done
    return point_list[sorted(id_set)]


def surface_sampling(triangle_list, sample_count):
    # Compute surface area of each triangle
    tri_area = mesh_area(triangle_list)

    # Compute a uniform sampling of the input mesh
    point_list = uniform_sample_mesh(triangle_list, tri_area, 4 * sample_count)

    # Compute a blue noise sampling of the input mesh, seeded by the previous sampling
    point_list = blue_noise_sample_elimination(point_list, numpy.sum(tri_area), sample_count)

    return point_list