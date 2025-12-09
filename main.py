from scene import Scene
from renderer import Renderer
import sys


def main():
    scene = Scene.create_scene_from_txt_file(sys.argv[1])
    rendered_image = render(scene)
    write(rendered_image)
