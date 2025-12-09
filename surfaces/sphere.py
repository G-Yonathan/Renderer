import numpy as np
from surfaces.surface import Surface


class Sphere(Surface):
    def __init__(self, position, radius, material_index):
        self.position = position
        self.radius = radius
        self.material_index = material_index

    def find_intersection(self, ray, camera_pos):

        L = self.position - camera_pos
        t_ca = np.dot(L, ray)
        if t_ca < 0:
            return None

        d_squared = np.dot(L, L) - t_ca**2
        if d_squared > self.radius**2:
            return None

        t_hc = np.sqrt(self.radius**2 - d_squared)

        t = t_ca - t_hc

        intersection = camera_pos + t * ray
        return intersection

    def get_normal(self, point):
        v = point - self.position
        return v / np.linalg.norm(v)
