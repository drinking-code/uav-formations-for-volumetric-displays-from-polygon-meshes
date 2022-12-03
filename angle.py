import numpy as np


def angle_between_vectors_anchor(vector_u, vector_v, vector_anchor=None):
    """
    Calculates the angle between vector_u and vector_v, taking vector_anchor as the origin
    :returns: angle θ
    """
    if vector_anchor is None:
        vector_anchor = [0, 0, 0]
    vector_u, vector_v, vector_anchor = np.array(vector_u), np.array(vector_v), np.array(vector_anchor)
    vector_u -= vector_anchor
    vector_v -= vector_anchor
    cos_θ = np.dot(vector_u, vector_v) / (np.linalg.norm(vector_u) * np.linalg.norm(vector_v))
    # clip to mitigate floating-point computation errors
    cos_θ = np.clip(cos_θ, -1, 1)
    θ_rad = np.arccos(cos_θ)
    θ = np.degrees(θ_rad)
    while θ > 90:
        θ -= 90
    return θ
