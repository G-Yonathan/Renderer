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

    def find_intersection(self, ray, source):  # TODO: change to slab method?

        def find_intersection_with_face(direction, face):
            # Construct plane containing face
            d = -np.dot(direction, face)
            plane = InfinitePlane(direction, d, None)
            point = plane.find_intersection(ray, source)

            # Check if intersection with plane is within the face
            for i in range(3):
                if direction[i] == 0 and abs(face[i] - point[i]) > self.scale / 2:
                    return None
            return point

        # Consider only three closest faces
        closest_indices = np.argsort(np.linalg.norm(self.faces - source, axis=1))[:3]

        closest_point = None
        min_dist_to_source = np.inf

        # Find closest intersection
        for idx in closest_indices:
            direction = self.directions[idx]
            face = self.faces[idx]
            point = find_intersection_with_face(direction, face)
            if point is not None:
                dist_to_source = np.linalg.norm(point - source)
                if dist_to_source < min_dist_to_source:
                    min_dist_to_source = dist_to_source
                    closest_point = point

        return closest_point

    def normal(self, point):
        # Find the closest face to the point in terms of norm
        return self.directions[np.argmin(np.linalg.norm(self.faces - point, axis=1))]
