import numpy as np
from surfaces.surface import Surface


class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        self.normal = normal
        self.offset = -offset
        self.material_index = material_index

    def find_intersection(self, ray, source):
        P_0 = source
        N = self.normal
        V = ray

        denom = np.dot(V, N)

        if abs(denom) < 1e-4:
            return None

        t = -(np.dot(P_0, N) + self.offset) / denom

        # Not looking in direction of plane
        if t < 0:
            return None

        return P_0 + t * ray

    def get_normal(self, point):
        return self.normal
