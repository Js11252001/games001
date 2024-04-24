import numpy as np
import matplotlib.pyplot as plt
import pywavefront

def get_obb_from_points(points):
    # TODO: your code here
    # 请使用 PCA 实现对 points 的包围盒的构建，需要返回包围盒的顶点 corners 和中心 center 
    # 其中包围盒顶点顺序如下所示：
    #     3-----2
    #    /|    /|
    #   0 --- 1 |
    #   | 7 - | 6
    #   |/    |/
    #   4 --- 5

    center = np.mean(points, axis=0)
    
    centered_points = points - center
    
    cov_matrix = np.cov(centered_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    
    order = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, order]
    
    transformed_points = np.dot(centered_points, eigenvectors)
    
    min_point = np.min(transformed_points, axis=0)
    max_point = np.max(transformed_points, axis=0)

    corners = np.array([
        [min_point[0], min_point[1], min_point[2]],
        [max_point[0], min_point[1], min_point[2]],
        [max_point[0], max_point[1], min_point[2]],
        [min_point[0], max_point[1], min_point[2]],
        [min_point[0], min_point[1], max_point[2]],
        [max_point[0], min_point[1], max_point[2]],
        [max_point[0], max_point[1], max_point[2]],
        [min_point[0], max_point[1], max_point[2]],
    ])
    
    corners = np.dot(corners, eigenvectors.T) + center

    return corners, center

scene = pywavefront.Wavefront('stanford-bunny.obj')
points = np.array(scene.vertices, dtype=np.float32)

corners, center = get_obb_from_points(points)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

ax.scatter(points[:,0], points[:,1], points[:,2], s=0.01, c='r', marker='o')
ax.scatter(corners[:,0], corners[:,1], corners[:,2], s=10, c='b', marker='o')
ax.scatter(center[0], center[1], center[2], s=10, c='b', marker='o')

indice = [0, 1, 2, 3, 0, 4, 5, 6, 7, 4, 5, 1, 2, 6, 7, 3]
new_corners = corners[indice]
ax.plot(new_corners[:,0], new_corners[:,1], new_corners[:,2], c='b')

plt.show()