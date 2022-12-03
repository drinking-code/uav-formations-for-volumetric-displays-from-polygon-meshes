from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

from corners_sharpness import calc_corner_sharpness
from edges_sharpness import calc_edge_sharpness
from pyplot_draw_mesh import draw_corner_sharpness, draw_edge_sharpness, draw_mesh_faces
from unique_vertices import unique_vertices, unique_edges
from utils import recursive_list

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

figure = plt.figure()
axes = figure.add_subplot(projection='3d', computed_zorder=False)

# find vertices by iterating faces (vertices may appear in more than one face)
vectors_list = recursive_list(mesh.vectors)
vertices = unique_vertices(vectors_list)
edges = unique_edges(vectors_list)

sharpness_corners = calc_corner_sharpness(mesh.vectors)
sharpness_edges = calc_edge_sharpness(mesh.vectors, mesh.normals)

# plot faces and vertices
# draw_mesh_faces(mesh.vectors, axes)
# draw_corner_sharpness(sharpness_corners, axes)
draw_edge_sharpness(sharpness_edges, axes)

scale = mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
plt.show()
