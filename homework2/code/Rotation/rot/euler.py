import numpy as np
import re


def euler2matrix(seq, angles, degrees=True) -> np.ndarray:
    num_axes = len(seq)
    if num_axes != 3:
        raise ValueError("Wrong euler sequence")
    if re.match(r"^[xyzXYZ]{3}$", seq) is None:
        raise ValueError("Wrong euler sequence")
    seq = seq.lower()
    if degrees:
        angles = np.deg2rad(angles)

    mat = np.eye(3)
    # TODO: your code here
    # 请将 mat 补全，使得函数返回正确的旋转矩阵
    Rx = lambda theta: np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    Ry = lambda theta: np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    Rz = lambda theta: np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

    for axis, angle in zip(seq, angles):
        if axis == 'x':
            mat = Rx(angle) @ mat
        elif axis == 'y':
            mat = Ry(angle) @ mat
        elif axis == 'z':
            mat = Rz(angle) @ mat

    return mat