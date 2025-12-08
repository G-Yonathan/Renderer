from Scene import Scene


def main():
    scene = Scene.create_scene_from_txt_file(mashu.csv)
    rendered_image = render(scene)
    write(rendered_image)
