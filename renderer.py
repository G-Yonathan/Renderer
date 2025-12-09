import numpy as np


class Renderer:

    @staticmethod
    def find_nearest_col(scene, ray, source):
        nearest_surface = None
        nearest_point = None
        min_dist = np.inf

        for surface in scene.get_surfaces():
            point = surface.find_intersection(ray, source)
            if point is not None:
                dist = np.linalg.norm(point - source)
                if dist < min_dist:
                    min_dist = dist
                    nearest_surface = surface
                    nearest_point = point

        return nearest_surface, nearest_point

    @staticmethod
    def compute_color(scene, obj, point):
        pass
        # will send rays to all light sources

    @staticmethod
    def render(scene, image_width, image_height):
        image = np.zeros((image_width, image_height, 3))

        ray_gen = scene.camera.ray_generator

        for ray, pix_x, pix_y in ray_gen:
            near_col_obj, near_col_point = find_nearest_col(scene, ray)
            color = compute_color(scene, near_col_obj, near_col_point)

            image[pix_x][pix_y] = color

        return image
