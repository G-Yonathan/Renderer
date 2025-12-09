import numpy as np
from scene_objs.camera import Camera
from surfaces import *


class Scene:
    def __init__(self, camera, scene_set, materials, planes, spheres, boxes, lights):
        self.camera = camera
        self.scene_set = scene_set
        self.materials = materials
        self.planes = planes
        self.spheres = spheres
        self.boxes = boxes
        self.lights = lights

    @staticmethod
    def create_scene_from_txt_file(filename):
        camera = None
        scene_set = None
        materials = []
        planes = []
        spheres = []
        boxes = []
        lights = []

        with open(filename) as file:
            for line in file:
                line = line.rstrip()
                if line and line[0] != "#":
                    split_line = line.split(line)
                    obj_code = split_line[0]

                    if obj_code == "cam":
                        camera = Camera(
                            position=np.array(
                                [
                                    float(split_line[1]),
                                    float(split_line[2]),
                                    float(split_line[3]),
                                ]
                            ),
                            look_at=np.array(
                                [
                                    float(split_line[4]),
                                    float(split_line[5]),
                                    float(split_line[6]),
                                ]
                            ),
                            up=np.array(
                                [
                                    float(split_line[7]),
                                    float(split_line[8]),
                                    float(split_line[9]),
                                ]
                            ),
                            sc_dist=float(split_line[10]),
                            sc_width=float(split_line[11]),
                        )
                    elif obj_code == "set":
                        scene_set = {
                            "bg_color": np.array(
                                [
                                    float(split_line[1]),
                                    float(split_line[2]),
                                    float(split_line[3]),
                                ]
                            ),
                            "sh_rays": int(split_line[4]),
                            "max_rec": int(split_line[5]),
                        }
                    elif obj_code == "mtl":
                        materials.append(
                            {
                                "diffuse_color": np.array(
                                    [
                                        float(split_line[1]),
                                        float(split_line[2]),
                                        float(split_line[3]),
                                    ]
                                ),
                                "specular_color": np.array(
                                    [
                                        float(split_line[4]),
                                        float(split_line[5]),
                                        float(split_line[6]),
                                    ]
                                ),
                                "reflect_color": np.array(
                                    [
                                        float(split_line[7]),
                                        float(split_line[8]),
                                        float(split_line[9]),
                                    ]
                                ),
                                "phong": float(split_line[10]),
                                "transparency": float(split_line[11]),
                            }
                        )
                    elif obj_code == "pln":
                        planes.append(
                            Plane(
                                normal=np.array(
                                    [
                                        float(split_line[1]),
                                        float(split_line[2]),
                                        float(split_line[3]),
                                    ]
                                ),
                                offset=float(split_line[4]),
                                material_idx=int(split_line[5]),
                            )
                        )
                    elif obj_code == "sph":
                        spheres.append(
                            Sphere(
                                center=np.array(
                                    [
                                        float(split_line[1]),
                                        float(split_line[2]),
                                        float(split_line[3]),
                                    ]
                                ),
                                radius=float(split_line[4]),
                                mat_idx=int(split_line[5]),
                            )
                        )
                    elif obj_code == "box":
                        boxes.append(
                            Box(
                                center=np.array(
                                    [
                                        float(split_line[1]),
                                        float(split_line[2]),
                                        float(split_line[3]),
                                    ]
                                ),
                                edge_length=float(split_line[4]),
                                mat_idx=int(split_line[5]),
                            )
                        )
                    elif obj_code == "lgt":
                        lights.append(
                            {
                                "position": np.array(
                                    [
                                        float(split_line[1]),
                                        float(split_line[2]),
                                        float(split_line[3]),
                                    ]
                                ),
                                "color": np.array(
                                    [
                                        float(split_line[4]),
                                        float(split_line[5]),
                                        float(split_line[6]),
                                    ]
                                ),
                                "spec": float(split_line[7]),
                                "shadow": float(split_line[8]),
                                "width": float(split_line[9]),
                            }
                        )

        return Scene(camera, scene_set, materials, planes, spheres, boxes, lights)
