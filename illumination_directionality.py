import io
import json
import re
import sys
from collections import Counter
from sys import argv, stdin, stdout

import math
import numpy as np
from stl import mesh as np_stl

from mesh import Mesh
from normals import run_normals_make_consistent_37
from utils import point_is_on_face, point_is_on_line_segment, list_contains, angle_between_vectors_anchor, \
    find_one_in_iterable, barycenter_point_set, vectors_plane_angle, dihedral_angle_and_spines

stl_contents = argv[1]
options = json.loads(argv[2])

mesh = np_stl.Mesh.from_file('', fh=io.StringIO(stl_contents))
mesh = Mesh(mesh)

normals = run_normals_make_consistent_37(mesh.faces)

newline_regex = re.compile(r"\n")
for point_data in stdin:
    point_data = newline_regex.sub('', point_data)
    if point_data == 'EXIT':
        sys.exit(0)
    point_data_list = point_data.split(' ')
    if len(point_data_list) != 5:
        continue

    ident = point_data_list.pop(0)
    position = point_data_list.pop(0)
    point = list(map(lambda value: float(value), point_data_list))
    if position == 'f':
        face = mesh.find_face(lambda face: point_is_on_face(point, face))
        if not face:
            break
        face = face[0]
        direction = normals[mesh.faces.index(face)]
        α = β = 180
    elif position == 'e':
        edge = mesh.find_edge(lambda edge: point_is_on_line_segment(point, edge))
        if not edge:
            break
        edge = edge[0]
        adjacent_faces = mesh.find_face(lambda face: all(map(lambda vertex: list_contains(face, vertex), edge)), True)
        direction = np.average([normals[mesh.faces.index(face)] for face in adjacent_faces], axis=0)
        direction = np.divide(direction, np.linalg.norm(direction))
        γ, spines = dihedral_angle_and_spines(adjacent_faces[0], adjacent_faces[1], edge)
        spine_mean = np.mean(spines, axis=0)
        if list(spine_mean) == [0, 0, 0]:  # γ is 180°
            γ = γ
        else:
            spine_mean = np.divide(spine_mean, np.linalg.norm(spine_mean))
            is_flipped_list = np.divide(spine_mean, direction)
            is_flipped_list_no_nan = list(filter(lambda value: not math.isnan(value), is_flipped_list))
            is_flipped = Counter(is_flipped_list_no_nan).most_common() == -1
            if not is_flipped:
                γ = 360 - γ
        face_on_p = [point, np.add(point, direction), np.add(point, [0, 0, 1])]
        edge_vector = np.subtract(edge[1], edge[0])
        δ = vectors_plane_angle(edge_vector, face_on_p)
        if δ > 90:
            δ = 90 * 2 - δ
        if δ < 45:
            α, β = 180, γ
        else:
            α, β = γ, 180
    elif position == 'c':
        faces = mesh.find_face(lambda face: list_contains(face, point), True)
        direction = barycenter_point_set([normals[mesh.faces.index(face)] for face in faces])
        if str(direction) == 'nan':  # isnan raises when ndarray is given
            continue
        edges = mesh.find_edge(lambda edge: list_contains(edge, point), True)
        s = [np.subtract(find_one_in_iterable(edge, lambda vertex: vertex != point), point) for edge in edges]
        face_on_p = [point, np.add(point, direction), np.add(point, [0, 0, 1])]
        normal_p = np.cross(np.subtract(face_on_p[1], face_on_p[0]), np.subtract(face_on_p[2], face_on_p[0]))
        face_on_q = [point, np.add(point, direction), np.add(point, normal_p)]
        normal_q = np.cross(np.subtract(face_on_q[1], face_on_q[0]), np.subtract(face_on_q[2], face_on_q[0]))


        def split_along_plane(vectors, face_normal):
            split1, split2 = [], []
            for vector in vectors:
                vertex = np.add(point, vector)
                point_on_side_1 = np.add(point, face_normal)
                point_on_side_2 = np.add(point, np.multiply(face_normal, -1))
                distance_n = np.linalg.norm(np.subtract(point_on_side_1, vertex))
                distance_n_neg = np.linalg.norm(np.subtract(point_on_side_2, vertex))
                if distance_n > distance_n_neg:
                    split1.append(vector)
                else:
                    split2.append(vector)
            return split1, split2


        t1, t2 = split_along_plane(s, normal_q)
        u1, u2 = split_along_plane(s, normal_p)


        def smallest_angle_to_plane(vectors, plane):
            sorted_vectors = list(sorted(
                [(vector, vectors_plane_angle(vector, plane)) for vector in vectors],
                key=lambda data: (angle := data[1], angle)[1]
            ))
            if not sorted_vectors:
                return None
            vector, angle = sorted_vectors[0]
            return vector


        t1_smallest = smallest_angle_to_plane(t1, face_on_p)
        t2_smallest = smallest_angle_to_plane(t2, face_on_p)
        α = angle_between_vectors_anchor(t1_smallest, t2_smallest) \
            if t1_smallest is not None and t2_smallest is not None else 360 - 120
        α = 360 - α
        u1_smallest = smallest_angle_to_plane(u1, face_on_q)
        u2_smallest = smallest_angle_to_plane(u2, face_on_q)
        β = angle_between_vectors_anchor(u1_smallest, t2_smallest) \
            if u1_smallest is not None and u2_smallest is not None else 360 - 120
        β = 360 - β
    else:
        continue

    stdout.write(f'{ident} {" ".join([str(value) for value in direction])} {α} {β}')
    stdout.write("\n")
    stdout.flush()
