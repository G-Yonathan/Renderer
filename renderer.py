import numpy as np


class Renderer:

    @staticmethod
    def find_nearest_col_from_camera(scene, ray):
        pass

    @staticmethod
    def compute_color(scene, obj, point):
        pass
        # will send rays to all light sources

    @staticmethod
    def render(scene, image_width, image_height):
        # Create image

        ray_gen = scene.camera.ray_generator

        for ray, pix_x, pix_y in ray_gen:
            near_col_obj, near_col_point = find_nearest_col(scene, ray)
            color = compute_color(scene, near_col_obj, near_col_point)

            image[pix_x][pix_y] = color

        return image
