#!/usr/bin/env python3

import numpy as np
from scipy.spatial.transform import Rotation

def parallel_transport(v1 : np.array, v2 : np.array) -> np.array:
    """
    Compute the parallel transport rotation matrix

    The parallel transport matrix is the minimum rotation that aligns v1 and v2

    Parameters:
    v1 (np.array): The initial 3d vector
    v2 (np.array): The final 3d vector

    Returns:
    np.array: The 3x3 parallel transport rotation matrix
    """
    cross = np.cross(v1, v2)
    cross_norm = np.linalg.norm(cross)
    if cross_norm < 1e-7:
        return np.identity(3)
    axis = cross / cross_norm
    angle = np.atan2(cross_norm, np.dot(v1, v2))
    return Rotation.from_rotvec(axis * angle).as_matrix()

def normalize(a : np.array) -> np.array:
    return a / np.linalg.norm(a)

def compute_rotation_matrix_from_direction(direction: np.array) -> np.array:
    initial_dir = np.array((0.0, 0.0, 1.0))
    return parallel_transport(initial_dir, normalize(direction))

def compute_rotations_parallel_transport(positions : np.array) -> np.array:
    """
    Compute the rotation vectors necessary so that the z director is following the centreline of the curve.

    Parameters:
    positions (np.array): An Nx3 shaped array containing the positions of the centreline.

    Returns:
    np.array: An array of equal shape as the positions array with the rotation vectors
    """
    rotvecs = [(0.0, 0.0, 0.0)] * positions.size

    # Compute first rotation
    direction0 = positions[1] - positions[0]
    R0 = compute_rotation_matrix_from_direction(direction0)

    rotvecs[0] = Rotation.from_matrix(R0).as_rotvec()

    last_direction = normalize(direction0)
    last_rotation = R0

    for i in range(1,len(positions)):
        vA = positions[i-1]
        vB = positions[i]

        AB = vB - vA

        direction = normalize(AB)
        rotation = parallel_transport(last_direction, direction) @ last_rotation

        rotvecs[i] = Rotation.from_matrix(rotation).as_rotvec();

        last_rotation = rotation
        last_direction = direction

    return np.array(rotvecs)
