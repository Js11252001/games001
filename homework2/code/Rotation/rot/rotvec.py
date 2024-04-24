import numpy as np


def rotvec2matrix(vec, degrees=False) -> np.ndarray:
    # TODO: your code here
    # 利用罗德里格旋转公式返回轴角表示对应的旋转矩阵
    if degrees:
        theta = np.linalg.norm(vec) * (np.pi / 180)  # Convert to radians
    else:
        theta = np.linalg.norm(vec)

    if theta != 0:
        vec = vec / theta  # Normalize the rotation vector
    else:
        return np.eye(3)  # If the angle is 0, return the identity matrix

    # Skew-symmetric matrix for vec
    K = np.array([[0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0]])

    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * np.dot(K, K)
    return R


def matrix2rotvec(matrix) -> np.ndarray:
    angle = np.arccos((np.trace(matrix) - 1) / 2)
    u = np.array(
        [
            matrix[2, 1] - matrix[1, 2],
            matrix[0, 2] - matrix[2, 0],
            matrix[1, 0] - matrix[0, 1],
        ]
    ) / (2 * np.sin(angle))
    return u * angle


def direct_lerp(a, b, t) -> np.ndarray:
    # TODO: your code here
    # 返回使用轴角表示直接插值的结果
    result = (1 - t) * a + t * b
    matrix = rotvec2matrix(result)
    return matrix


def rel_lerp(a, b, t) -> np.ndarray:
    # TODO: your code here
    # 返回使用轴角表示相对插值的结果
    R_a = rotvec2matrix(a)
    R_b = rotvec2matrix(b)

    R_delta = np.dot(R_b, np.linalg.inv(R_a))

    axis_angle = matrix2rotvec(R_delta) * t

    R = np.dot(rotvec2matrix(axis_angle), R_a)
    return R