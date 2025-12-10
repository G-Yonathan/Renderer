import numpy as np


class Renderer:

    @staticmethod
    def find_nearest_col(scene, ray, source):
        nearest_surface = None
        nearest_point = None
        min_dist = np.inf

        for surface in scene.surfaces:
            point = surface.find_intersection(ray, source)
            if point is not None:
                dist = np.linalg.norm(point - source)
                if dist < min_dist:
                    min_dist = dist
                    nearest_surface = surface
                    nearest_point = point

        return nearest_surface, nearest_point

    @staticmethod
    def compute_color(scene, ray, source, rec_depth):

        near_col_obj, near_col_point = Renderer.find_nearest_col(scene, ray, source)

        obj_material = scene.materials[near_col_obj.material_index - 1]

        # Direct light
        diffuse_total = np.zeros(3)
        specular_total = np.zeros(3)

        normal = near_col_obj.get_normal(near_col_point)

        # TODO: choose appropriate epsilon
        point_with_epsilon = near_col_point + (normal * 1e-3)

        for light in scene.lights:
            light_vector = light.position - point_with_epsilon
            dist_to_light = np.linalg.norm(light_vector)
            light_vector /= dist_to_light

            to_light_col_obj, to_light_col_point = Renderer.find_nearest_col(
                scene, light_vector, point_with_epsilon
            )

            dist_to_light_col_obj = np.linalg.norm(
                to_light_col_point - point_with_epsilon
            )

            is_shadow = (
                to_light_col_obj is not None and dist_to_light_col_obj < dist_to_light
            )
            intensity = 1.0 - light.shadow_intensity if is_shadow else 1.0

            # Diffuse
            diffuse_total += obj_material.diffuse_color * light.color * intensity

            # Specular
            reflection_vector = np.dot(2 * ray, normal) * normal - ray
            alignment_with_reflection_vector = np.dot(reflection_vector, ray)

            if alignment_with_reflection_vector > 0:
                phong_factor = alignment_with_reflection_vector**obj_material.shininess
                specular_total += (
                    obj_material.specular_color
                    * light.color
                    * light.specular_intensity
                    * phong_factor
                    * intensity
                )

        direct_light_color = diffuse_total + specular_total

        return np.clip(direct_light_color, 0, 1)

        # if rec_depth <= 0:
        #     # TODO: surface.get_color() returns base color of object (or material version)
        #     return near_col_obj.get_color()

        # # TODO: Figure out light and shadow logic and plant here
        # # TODO: calculate_transparent_ray (findnearcol bit w/out current object)
        # # TODO: calculate_reflection_ray (using the slideshow)
        # transparent_color = 0
        # if near_col_obj.transparency > 0:
        #     transparent_ray = Renderer.calculate_transparent_ray(
        #         ray, near_col_obj, near_col_point
        #     )
        #     transparent_color = Renderer.compute_color(
        #         scene, transparent_ray, near_col_point, rec_depth - 1
        #     )

        # reflection_color = 0
        # if near_col_obj.reflect > 0:
        #     reflection_ray = Renderer.calculate_reflection_ray(
        #         ray, near_col_obj, near_col_point
        #     )
        #     reflection_color = (
        #         Renderer.compute_color(
        #             scene, reflection_ray, near_col_point, rec_depth - 1
        #         )
        #         * obj_material.reflection
        #     )

        # # TODO: Not clear how to calculate diffuse and specular color
        # output_color = (
        #     obj_material.transparency * transparent_color
        #     + (1 - obj_material.transparency) * (diffuse_color + specular_color)
        #     + (reflection_color)
        # )

    @staticmethod
    def render(scene, image_width, image_height):
        image = np.zeros((image_width, image_height, 3))

        ray_gen = scene.camera.ray_generator(image_width, image_height)

        for ray, pix_x, pix_y in ray_gen:
            # Yonatan, I know you might not agree to this approach
            # But it's simpler than you think, it's just recursive logic and scalable too.
            # Beseder shichnata
            color = Renderer.compute_color(
                scene, ray, scene.camera.position, scene.scene_set.max_recursions
            )

            image[pix_x][pix_y] = color

        return image
