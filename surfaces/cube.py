import numpy as np
from surfaces.surface import Surface
from surfaces.infinite_plane import InfinitePlane


class Cube(Surface):
    def __init__(self, position, scale, material_index):
        super().__init__(material_index)
        self.position = position
        self.scale = scale
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

        self.min_bound = self.position - (self.scale / 2)
        self.max_bound = self.position + (self.scale / 2)

    def find_intersection(self, ray_dir, source):
        # Slab method
        parallel = ray_dir == 0.0

        ray_dir[parallel] += 1e-9

        inv_dir = 1.0 / ray_dir

        t1 = (self.min_bound - source) * inv_dir
        t2 = (self.max_bound - source) * inv_dir

        t_min = np.minimum(t1, t2)
        t_max = np.maximum(t1, t2)

        t_enter = np.max(t_min)
        t_exit = np.min(t_max)

        if t_exit >= t_enter and t_exit > 0:
            t_hit = t_enter if t_enter > 0 else t_exit
            return source + (ray_dir * t_hit)

        return None

    def get_normal(self, point):
        # Find the closest face to the point in terms of norm
        return self.directions[np.argmin(np.linalg.norm(self.faces - point, axis=1))]
