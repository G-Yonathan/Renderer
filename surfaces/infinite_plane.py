import numpy as np
from surfaces.surface import Surface


class InfinitePlane(Surface):
    def __init__(self, normal, offset, material_index):
        self.normal = normal
        self.offset = offset
        self.material_index = material_index

    def find_intersection(self, ray, source):
        P_0 = source
        N = self.normal
        V = ray

        t = -(np.dot(P_0, N) + self.offset) / np.dot(V, N)

        return P_0 + t * ray

    def get_normal(self, point):
        return self.normal
