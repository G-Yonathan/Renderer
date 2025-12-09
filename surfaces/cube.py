import numpy as np
from surfaces.surface import Surface
from surfaces.infinite_plane import InfinitePlane


class Cube(Surface):
    def __init__(self, position, scale, material_index):
        self.position = position
        self.scale = scale
        self.material_index = material_index

        self.directions = np.array(
            [
                (1, 0, 0),  # +x (Right)
                (-1, 0, 0),  # -x (Left)
                (0, 1, 0),  # +y (Up)
                (0, -1, 0),  # -y (Down)
                (0, 0, 1),  # +z (Front)
                (0, 0, -1),  # -z (Back)
            ]
        )

        self.faces = position + (scale / 2) * self.directions

    def find_intersection(self, ray, camera_pos):

        def intersect_face(direction, face):
            d = -np.dot(direction, face)
            plane = InfinitePlane(direction, d, None)

            point = plane.find_intersection(ray, camera_pos)
            for i in range(3):
                if direction[i] == 0:
                    if abs(face[i] - point[i]) > self.scale / 2:
                        return None
            return point

        # Find top 3 closest points.
        closest_indices = np.argsort(np.linalg.norm(self.faces - camera_pos, axis=1))[
            :3
        ]

        min_point 
        for idx in closest_indices:
            direction = self.directions[idx]
            face = self.faces[idx]
            point = intersect_face(direction, face)

    def normal(self, point):

        # Find the closest face to the point in terms of norm
        return self.directions[np.argmin(np.linalg.norm(self.faces - point, axis=1))]
