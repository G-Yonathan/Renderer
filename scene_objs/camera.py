import numpy as np


class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = position
        self.look_at = look_at
        self.up_vector = up_vector
        self.screen_distance = screen_distance
        self.screen_width = screen_width

    def ray_generator(self, image_width, image_height):
        n_plane = self.look_at - self.position
        n_plane /= np.linalg.norm(n_plane)

        d_plane = np.dot(n_plane, (n_plane * self.screen_distance) + self.position)
        d_plane /= np.linalg.norm(d_plane)

        alpha = -(d_plane + np.dot(self.position, n_plane)) / np.dot(n_plane, n_plane)
        screen_center = self.position + alpha * n_plane

        v_y = self.up_vector - np.dot(self.up_vector, n_plane) * n_plane
        v_y /= np.linalg.norm(v_y)

        v_x = np.cross(n_plane, v_y)
        v_x /= np.linalg.norm(v_x)

        screen_height = (self.screen_width * image_height) / image_width

        # TODO: should coefficient of Vx be 0.5 or -0.5 to get left side. Itay thinks -0.5
        screen_top_left = (
            screen_center + 0.5 * screen_height * v_y - 0.5 * self.screen_width * v_x
        )

        pixel_width = self.screen_width / image_width

        p_0 = screen_top_left + (pixel_width / 2) * v_x - (pixel_width / 2) * v_y

        for i in range(image_height):
            p_1 = p_0
            for j in range(image_width):
                ray = p_1 - self.position
                ray /= np.linalg.norm(ray)

                p_1 += pixel_width * v_x

                yield ray, i, j
            p_0 -= pixel_width * v_y
