import numpy as np


class Renderer:

    def __init__(self, scene):
        self.scene = scene

        self.surfaces = scene.surfaces

        self.camera_position = scene.camera.position

        self.max_recursions = scene.scene_set.max_recursions
        self.background_color = scene.scene_set.background_color

        self.lights = scene.lights

    def find_nearest_col(self, ray, source):
        nearest_surface = None
        nearest_point = None
        eps = 1e-4  # TODO: choose appropriate epsilon
        min_dist = np.inf

        for i, surface in enumerate(self.surfaces):
            point = surface.find_intersection(ray, source)
            if point is not None:
                dist = np.linalg.norm(point - source)
                if dist < eps:
                    continue

                if dist < min_dist:
                    min_dist = dist
                    nearest_surface = surface
                    nearest_point = point

        return nearest_surface, nearest_point

    def compute_direct_light_color(self, normal, obj_material, near_col_point, ray):
        diffuse_total = np.zeros(3)
        specular_total = np.zeros(3)

        for light in self.lights:
            light_vector = light.position - near_col_point
            dist_to_light = np.linalg.norm(light_vector)
            light_vector /= dist_to_light

            to_light_col_obj, to_light_col_point = self.find_nearest_col(
                light_vector, near_col_point
            )

            if to_light_col_obj is None:
                is_shadow = False
            else:
                to_light_col_obj_material = self.scene.materials[
                    to_light_col_obj.material_index - 1
                ]

                dist_to_light_col_obj = np.linalg.norm(
                    to_light_col_point - near_col_point
                )

                is_shadow = (
                    to_light_col_obj is not None
                    and dist_to_light_col_obj < dist_to_light
                )

            intensity = (
                (
                    (
                        1.0
                        - light.shadow_intensity
                        * (1 - to_light_col_obj_material.transparency)
                    )
                )
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

        return np.clip(direct_light_color, 0, 1)

    def compute_color(self, ray, source, rec_depth):
        near_col_obj, near_col_point = self.find_nearest_col(ray, source)

        if near_col_obj is None:
            return self.background_color

        normal = near_col_obj.get_normal(near_col_point)
        obj_material = self.scene.materials[near_col_obj.material_index - 1]

        ### Direct Light ###
        direct_light_color = self.compute_direct_light_color(
            normal, obj_material, near_col_point, ray
        )

        ### Transparency + Reflection ###
        if rec_depth <= 0:
            return direct_light_color

        # Transparency
        transparent_color = np.zeros(3)

        if obj_material.transparency > 0:
            transparent_color = self.compute_color(ray, near_col_point, rec_depth - 1)

        # Reflection
        reflection_color = np.zeros(3)

        if np.any(obj_material.reflection_color > 0):
            reflection_ray = ray - 2 * np.dot(ray, normal) * normal

            reflection_color = (
                self.compute_color(reflection_ray, near_col_point, rec_depth - 1)
                * obj_material.reflection_color
            )

        ### Final Color ###
        output_color = (
            obj_material.transparency * transparent_color
            + (1 - obj_material.transparency) * (direct_light_color)
            + (reflection_color)
        )
        output_color = np.clip(output_color, 0, 1)

        return output_color

    def render(self, image_width, image_height):
        image = np.zeros((image_width, image_height, 3))

        ray_gen = self.scene.camera.ray_generator(image_width, image_height)

        for ray, pix_x, pix_y in ray_gen:
            color = self.compute_color(ray, self.camera_position, self.max_recursions)

            image[pix_x][pix_y] = color

        return image
