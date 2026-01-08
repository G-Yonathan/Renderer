import numpy as np


class RayTracerUtils:
    @staticmethod
    def get_orthogonal_vector(v):
        if np.allclose(v, 0):
            return np.array([1, 0, 0])  # No orthogonal vector, return arbitrary vector

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

    @staticmethod
    def ray_generator(
        source,
        width_resolution,
        height_resolution,
        screen_width,
        screen_center,
        up_vector=None,
        randomize=False,
    ):
        n_plane = screen_center - source
        n_plane /= np.linalg.norm(n_plane)

        if up_vector is None:
            v_y = RayTracerUtils.get_orthogonal_vector(n_plane)
        else:
            v_y = up_vector - np.dot(up_vector, n_plane) * n_plane
            if np.linalg.norm(v_y) == 0:
                v_y = RayTracerUtils.get_orthogonal_vector(n_plane)
            else:
                v_y /= np.linalg.norm(v_y)

        v_x = np.cross(v_y, n_plane)
        v_x /= np.linalg.norm(v_x)

        screen_height = (screen_width * height_resolution) / width_resolution

        screen_top_left = (
            screen_center + 0.5 * screen_height * v_y - 0.5 * screen_width * v_x
        )

        pixel_width = screen_width / width_resolution

        p_0 = screen_top_left + (pixel_width / 2) * v_x - (pixel_width / 2) * v_y

        for i in range(height_resolution):
            p_1 = p_0.copy()
            for j in range(width_resolution):
                if randomize:
                    rx = np.random.rand() - 0.5
                    ry = np.random.rand() - 0.5

                    point_in_pixel = (
                        p_1 + rx * pixel_width * v_x - ry * pixel_width * v_y
                    )
                else:
                    point_in_pixel = p_1

                ray = point_in_pixel - source
                ray /= np.linalg.norm(ray)

                yield ray, i, j

                p_1 += pixel_width * v_x
            p_0 -= pixel_width * v_y
