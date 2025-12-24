from ray_tracer_utils import RayTracerUtils


class Light:
    def __init__(self, position, color, specular_intensity, shadow_intensity, radius):
        self.position = position
        self.color = color
        self.specular_intensity = specular_intensity
        self.shadow_intensity = shadow_intensity
        self.radius = radius

    def ray_generator(self, source, shadow_rays):
        return RayTracerUtils.ray_generator(
            source,
            shadow_rays,
            shadow_rays,
            self.radius,  # TODO: light.radius or light.radius * 2?
            self.position,
            randomize=True,
        )
