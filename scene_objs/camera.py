import numpy as np


class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = position
        self.look_at = look_at
        self.up_vector = up_vector
        self.screen_distance = screen_distance
        self.screen_width = screen_width

    @staticmethod
    def get_orthogonal_vector(v):
        if np.allclose(v, 0):
            raise ValueError("Zero vector has no defined orthogonal vector.")

        if abs(v[0]) < abs(v[1]):
            if abs(v[0]) < abs(v[2]):
                other = np.array([1, 0, 0])
            else:
                other = np.array([0, 0, 1])
        else:
            if abs(v[1]) < abs(v[2]):
                other = np.array([0, 1, 0])
            else:
                other = np.array([0, 0, 1])

        ortho = np.cross(v, other)
        return ortho / np.linalg.norm(ortho)

    def ray_generator(self, image_width, image_height):
        n_plane = self.look_at - self.position
        n_plane /= np.linalg.norm(n_plane)

        # d_plane = np.dot(n_plane, (n_plane * self.screen_distance) + self.position)

        screen_center = self.position + self.screen_distance * n_plane

        v_y = self.up_vector - np.dot(self.up_vector, n_plane) * n_plane
        if (
            np.linalg.norm(v_y) == 0
        ):  # v_y is perpendicular to screen, choose arbitrary vy direction
            v_y = self.get_orthogonal_vector(n_plane)
        else:
            v_y /= np.linalg.norm(v_y)

        v_x = np.cross(v_y, n_plane)
        v_x /= np.linalg.norm(v_x)

        screen_height = (self.screen_width * image_height) / image_width

        screen_top_left = (
            screen_center + 0.5 * screen_height * v_y - 0.5 * self.screen_width * v_x
        )

        pixel_width = self.screen_width / image_width

        p_0 = screen_top_left + (pixel_width / 2) * v_x - (pixel_width / 2) * v_y

        for i in range(image_height):
            p_1 = p_0.copy()
            for j in range(image_width):
                ray = p_1 - self.position
                ray /= np.linalg.norm(ray)

                p_1 += pixel_width * v_x

                yield ray, i, j
            p_0 -= pixel_width * v_y
