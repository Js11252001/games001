from locale import normalize
import numpy as np


class Quaternion:
    # (w, ix, jy, kz)
    def __init__(self, quat=[0, 1, 0, 0]) -> None:
        self.quat = self.normalize(quat)

    def normalize(self, quat) -> np.ndarray:
        return quat / np.linalg.norm(quat)

    def to_matrix(self) -> np.ndarray:
        w, x, y, z = self.quat
        return np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ]
        )

    def from_rotvec(self, vec):
        vec = np.array(vec)
        angle = np.linalg.norm(vec)
        self.quat = np.array([np.cos(angle / 2), *np.sin(angle / 2) * vec / angle])
        return self

    def __mul__(self, other):
        # TODO: your code here
        # 返回两个四元数的乘积
        w1, x1, y1, z1 = self.quat
        w2, x2, y2, z2 = other.quat
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        return Quaternion([w, x, y, z])

    @staticmethod
    def Nlerp(a, b, t) -> "Quaternion":
        # TODO: your code here
        # 返回 Nlerp 插值结果
        interp_quat = ((1 - t) * a.quat + t * b.quat)
        q = Quaternion(interp_quat)
        quat_lerp = q.normalize(interp_quat)
        # Normalizing
        return Quaternion(quat_lerp)

    @staticmethod
    def Slerp(a, b, t, short_path=True) -> "Quaternion":
        # TODO: your code here
        # short_path 为 True 时，返回最小弧的 Slerp 插值结果
        # 返回 Slerp 插值结果
        dot = np.dot(a.quat, b.quat)
        if short_path and dot < 0:
            # Take the shortest path
            b_quat = -b.quat
            dot = -dot
        else:
            b_quat = b.quat

        theta_0 = np.arccos(dot)  # angle between input vectors
        sin_theta_0 = np.sin(theta_0)

        theta = theta_0 * t  # angle between a.quat and result
        sin_theta = np.sin(theta)

        s0 = np.sin(theta_0 - theta) / sin_theta_0
        s1 = sin_theta / sin_theta_0

        return Quaternion(s0 * a.quat + s1 * b_quat)