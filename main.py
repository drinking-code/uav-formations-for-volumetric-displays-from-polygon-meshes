import numpy
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

from hard_corners import calc_corner_sharpness
from unique_vertices import unique_vertices

"""
1. Load data / convert into standardised format
2. Find hard edges & corners
    - sharpness of corners calculated by taking sum of the angles between all adjacent edges that connect to the vertex.
      deviation of this sum from 360° is the sharpness -> normalised with 0 - 360 => 1 - 0 and 360 - 720 => 0 - 1
3. Reduce hard corners that are too close
4. Distribute points on hard corners (vertices)
4. Distribute points on hard edges _while keeping distance to already generated points_
5. Distribute points on faces including soft edges and corners (vertices) (bluse noise sampling) _while keeping
   distance to already generated points_
6. Map colors to points
7. (Optional) perform checks
"""

mesh = mesh.Mesh.from_file('monkey.stl')
# print(mesh.vectors)

# figure = pyplot.figure()
# axes = figure.add_subplot(projection='3d')

# find vertices by iterating faces (vertices may appear in more than one face)
vertices = unique_vertices(mesh.vectors)

calc_corner_sharpness(mesh.vectors)


# plot faces and vertices
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors, facecolors='w', linewidths=1))
# axes.scatter(
#     list(map(lambda vertex: vertex[0], vertices)),
#     list(map(lambda vertex: vertex[1], vertices)),
#     list(map(lambda vertex: vertex[2], vertices))
# )
# scale = mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)
# pyplot.show()
