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
        # Pre-calculate the min and max corners of the box (AABB)
        # min_bound = bottom-left-back, max_bound = top-right-front
        half_scale = self.scale / 2
        self.min_bound = self.position - half_scale
        self.max_bound = self.position + half_scale

    def find_intersection(self, ray_dir, source):
        # 1. Calculate intersection t-values for all 3 axes at once.
        #    We add a tiny epsilon (1e-9) to ray_dir to prevent DivisionByZero errors
        #    if the ray is perfectly parallel to an axis.
        inv_dir = 1.0 / (ray_dir + 1e-9)

        t1 = (self.min_bound - source) * inv_dir
        t2 = (self.max_bound - source) * inv_dir

        # 2. For each axis, t1 might be the entry or the exit depending on direction.
        #    We force t_min to be the entry and t_max to be the exit.
        t_min = np.minimum(t1, t2)
        t_max = np.maximum(t1, t2)

        # 3. Find the actual intersection interval.
        #    The ray enters the CUBE only after it has entered ALL three slabs.
        #    The ray exits the CUBE as soon as it leaves ANY of the three slabs.
        t_enter = np.max(t_min)
        t_exit = np.min(t_max)

        # 4. Check if the hit is valid
        #    t_exit >= t_enter: The intervals overlap (we hit the volume)
        #    t_exit > 0: The cube is not fully behind us
        if t_exit >= t_enter and t_exit > 0:
            # If t_enter is negative, we are inside the cube -> hit is t_exit
            # Otherwise, we are outside -> hit is t_enter
            t_hit = t_enter if t_enter > 0 else t_exit
            return source + (ray_dir * t_hit)

        return None

    def get_normal(self, point):
        # Find the closest face to the point in terms of norm
        return self.directions[np.argmin(np.linalg.norm(self.faces - point, axis=1))]
