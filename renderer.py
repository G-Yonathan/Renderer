import numpy as np
from surfaces.sphere import Sphere


class Renderer:

    @staticmethod
    def find_nearest_col(scene, ray, source, exclude=None):
        nearest_surface = None
        nearest_point = None
        nearest_index = None
        min_dist = np.inf

        for i, surface in enumerate(scene.surfaces):
            if exclude != None and exclude == surface:
                continue
            point = surface.find_intersection(ray, source)
            if point is not None:
                dist = np.linalg.norm(point - source)
                if dist < min_dist:
                    min_dist = dist
                    nearest_surface = surface
                    nearest_point = point
                    nearest_index = i

        return nearest_surface, nearest_point, nearest_index

    @staticmethod
    def compute_color(
        scene, ray, source, rec_depth, exclude=None, exclude_transparency=1
    ):

        eps = 1e-5
        near_col_obj, near_col_point, nearest_index = Renderer.find_nearest_col(
            scene, ray, source, exclude=exclude
        )

        if near_col_obj is None:
            return scene.scene_set.background_color

        obj_material = scene.materials[near_col_obj.material_index - 1]

        # Direct light
        diffuse_total = np.zeros(3)
        specular_total = np.zeros(3)

        normal = near_col_obj.get_normal(near_col_point)

        # TODO: choose appropriate epsilon
        point_with_epsilon = near_col_point + (normal * eps)

        for light in scene.lights:
            light_vector = light.position - point_with_epsilon
            dist_to_light = np.linalg.norm(light_vector)
            light_vector /= dist_to_light

            to_light_col_obj, to_light_col_point, _ = Renderer.find_nearest_col(
                scene, light_vector, point_with_epsilon
            )

            if to_light_col_obj is None:
                is_shadow = False
            else:
                dist_to_light_col_obj = np.linalg.norm(
                    to_light_col_point - point_with_epsilon
                )

                is_shadow = (
                    to_light_col_obj is not None
                    and dist_to_light_col_obj < dist_to_light
                )

            intensity = (
                (1.0 - light.shadow_intensity * exclude_transparency)
                if is_shadow
                else 1.0
            )

            # Diffuse
            diffuse_total += (
                obj_material.diffuse_color
                * max(0, np.dot(normal, light_vector))
                * light.color
                * intensity
            )

            # Specular
            reflection_vector = 2 * np.dot(light_vector, normal) * normal - light_vector

            alignment_with_reflection_vector = np.dot(reflection_vector, -ray)

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

        direct_light_color = np.clip(direct_light_color, 0, 1)

        if rec_depth <= 0:
            return direct_light_color

        transparent_color = 0

        if obj_material.transparency > 0:
            transparent_color = Renderer.compute_color(
                scene,
                ray,
                point_with_epsilon,
                rec_depth - 1,
                exclude=near_col_obj,
                exclude_transparency=obj_material.transparency,
            )

        reflection_color = 0

        if obj_material.reflection_color.any() > 0:
            reflection_ray = -(2 * np.dot(ray, normal) * normal - ray)

            reflection_color = (
                Renderer.compute_color(
                    scene,
                    reflection_ray,
                    point_with_epsilon,
                    rec_depth - 1,
                    exclude=near_col_obj,
                    exclude_transparency=obj_material.transparency,
                )
                * obj_material.reflection_color
            )

        output_color = (
            obj_material.transparency * transparent_color
            + (1 - obj_material.transparency) * (direct_light_color)
            + (reflection_color)
        )
        output_color = np.clip(output_color, 0, 1)

        return output_color

    @staticmethod
    def render(scene, image_width, image_height):
        image = np.zeros((image_width, image_height, 3))

        ray_gen = scene.camera.ray_generator(image_width, image_height)

        for ray, pix_x, pix_y in ray_gen:

            color = Renderer.compute_color(
                scene, ray, scene.camera.position, scene.scene_set.max_recursions
            )

            image[pix_x][pix_y] = color

        return image
