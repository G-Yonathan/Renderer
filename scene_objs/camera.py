class Camera:
    def __init__(self, position, look_at, up_vector, screen_distance, screen_width):
        self.position = position
        self.look_at = look_at
        self.up_vector = up_vector
        self.screen_distance = screen_distance
        self.screen_width = screen_width

    def ray_generator():
        for i in range(screen_width):
            for j in range(screen_length):
                # Calculate ray
                yield ray
