class Camera:

    def __init__(self, position, look_at, up, sc_dist, sc_width):
        self.position = position
        self.look_at = look_at
        self.up = up
        self.sc_dist = sc_dist
        self.sc_width = sc_width

    def ray_generator():
        for i in range(screen_width):
            for j in range(screen_length):
                # Calculate ray
                yield ray
