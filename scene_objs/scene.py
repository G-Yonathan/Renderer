import numpy as np

from scene_objs.camera import Camera
from scene_objs.light import Light
from scene_objs.scene_settings import SceneSettings
from scene_objs.material import Material

from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere
from surfaces.cube import Cube


class Scene:
    def __init__(self, camera, scene_set, materials, planes, spheres, cubes, lights):
        self.camera = camera
        self.scene_set = scene_set
        self.materials = materials
        self.planes = planes
        self.spheres = spheres
        self.cubes = cubes
        self.lights = lights

    def get_surfaces(self):
        return self.planes + self.spheres + self.cubes

    @staticmethod
    def create_scene_from_txt_file(filename):
        camera = None
        scene_set = None
        materials = []
        planes = []
        spheres = []
        cubes = []
        lights = []

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                obj_type = parts[0]
                params = [float(p) for p in parts[1:]]

                if obj_type == "cam":
                    camera = Camera(
                        position=np.array(params[0:3]),
                        look_at=np.array(params[3:6]),
                        up_vector=np.array(params[6:9]),
                        screen_distance=params[9],
                        screen_width=params[10],
                    )
                elif obj_type == "set":
                    scene_set = SceneSettings(
                        background_color=np.array(params[0:3]),
                        root_number_shadow_rays=int(params[3]),
                        max_recursions=int(params[4]),
                    )
                elif obj_type == "mtl":
                    materials.append(
                        Material(
                            diffuse_color=np.array(params[0:3]),
                            specular_color=np.array(params[3:6]),
                            reflection_color=np.array(params[6:9]),
                            shininess=params[9],
                            transparency=params[10],
                        )
                    )
                elif obj_type == "pln":
                    planes.append(
                        InfinitePlane(
                            normal=np.array(params[0:3]),
                            offset=params[3],
                            material_idx=int(params[4]),
                        )
                    )
                elif obj_type == "sph":
                    spheres.append(
                        Sphere(
                            center=np.array(params[0:3]),
                            radius=params[3],
                            mat_idx=int(params[4]),
                        )
                    )
                elif obj_type == "box":
                    cubes.append(
                        Cube(
                            center=np.array(params[0:3]),
                            edge_length=params[3],
                            mat_idx=int(params[4]),
                        )
                    )
                elif obj_type == "lgt":
                    lights.append(
                        Light(
                            position=np.array(params[0:3]),
                            color=np.array(params[3:6]),
                            specular_intensity=params[6],
                            shadow_intensity=params[7],
                            radius=params[8],
                        )
                    )

        return Scene(camera, scene_set, materials, planes, spheres, cubes, lights)
