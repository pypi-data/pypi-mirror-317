#!/usr/bin/env python3

from scipy.spatial.transform import Rotation
import numpy as np


def rotation_exp_map(axis_angle: np.array) -> np.array:
    return Rotation.from_rotvec(axis_angle.copy()).as_matrix()


def skew(v: np.array) -> np.array:
    return np.array(
        [
            [0.0, -v[2], v[1]],
            [v[2], 0.0, -v[0]],
            [-v[1], v[0], 0.0],
        ]
    )


def unskew(m: np.array) -> np.array:
    return np.array([m[2][1], m[0][2], m[1][0]])


def expMapJacobian(axis_angle: np.array) -> np.array:
    angle = np.linalg.norm(axis_angle)
    return (
        np.identity(3)
        + (1 - np.cos(angle)) / angle**2 * skew(axis_angle)
        - (angle - np.sin(angle)) / angle**3 * skew(axis_angle) @ skew(axis_angle)
    )
