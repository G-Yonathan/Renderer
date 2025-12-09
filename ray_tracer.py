import argparse
from PIL import Image
import numpy as np

from scene_objs.camera import Camera
from scene_objs.light import Light
from scene_objs.material import Material
from scene_objs.scene_settings import SceneSettings
from surfaces.cube import Cube
from surfaces.infinite_plane import InfinitePlane
from surfaces.sphere import Sphere





def save_image(image_array):
    image = Image.fromarray(np.uint8(image_array))

    # Save the image to a file
    image.save("scenes/Spheres.png")


def main():
    parser = argparse.ArgumentParser(description='Python Ray Tracer')
    parser.add_argument('scene_file', type=str, help='Path to the scene file')
    parser.add_argument('output_image', type=str, help='Name of the output image file')
    parser.add_argument('--width', type=int, default=500, help='Image width')
    parser.add_argument('--height', type=int, default=500, help='Image height')
    args = parser.parse_args()

    # Parse the scene file
    scene = Scene.create_scene_from_txt_file(args.scene_file)

    rendered_image_array = render(scene)

    # Dummy result
    # image_array = np.zeros((500, 500, 3))

    # Save the output image
    save_image(rendered_image_array)


if __name__ == '__main__':
    main()
