import numpy as np
from ray_tracer_utils import RayTracerUtils


class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = position
        self.look_at = look_at
        self.up_vector = up_vector
        self.screen_distance = screen_distance
        self.screen_width = screen_width

    def ray_generator(self, image_width, image_height):
        look_at_ray = self.look_at - self.position
        look_at_ray /= np.linalg.norm(look_at_ray)
        screen_center = self.position + self.screen_distance * look_at_ray

        return RayTracerUtils.ray_generator(
            self.position,
            image_width,
            image_height,
            self.screen_width,
            screen_center,
            up_vector=self.up_vector,
        )
