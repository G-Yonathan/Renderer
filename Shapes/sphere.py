from shape import Shape


class Sphere(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def find_itersection(self, ray, camera_pos):

        L = self.center - camera_pos
        t_ca = np.dot(L, ray)
        if t_ca < 0:
            return None

        d_squared = np.dot(L, L) - t_ca**2
        if d_squared > self.radius**2:
            return None

        t_hc = np.sqrt(self.radius**2 - d_squared)

        t = t_ca - t_hc

        intersection = camera_pos + t * ray
