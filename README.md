# Scene Renderer using Ray Tracing

Recursive ray tracer written in Python, implementing phong illumination, reflections, transparency, soft shadows, and proper shadown for transparent objects.

---

## Features

### Geometry

The renderer supports intersection and shading for:

- **Spheres**
- **Infinite planes**
- **Axis-aligned cubes**

### Materials

Each surface is associated with a material defined by diffuse color, specular color, phong coefficient, reflection color, and transparency.

### Lighting

Only point lights are used, with soft-shadow support.

Each light is defined by position color, specular intensity, shadow intensity, and light radius (used for soft shadows).

Soft shadows are computed using stochastic sampling over an **N × N** grid.

### Camera

The camera is defined by position, look-at point, up vector, screen distance, and screen width.

## Scene File Format

Scenes are text files. Each line starts with a 3-letter code.

Lines starting with `#` are comments.

### Camera

```
cam px py pz  lx ly lz  ux uy uz  screen_dist screen_width
```

### Settings

```
set bg_r bg_g bg_b  shadow_rays_root  max_recursion
```

### Material

```
mtl dr dg db  sr sg sb  rr rg rb  phong  transparency
```

### Sphere

```
sph cx cy cz  radius  material_index
```

### Plane

```
pln nx ny nz  offset  material_index
```

### Box

```
box cx cy cz  scale  material_index
```

### Light

```
lgt px py pz  r g b  spec_intensity  shadow_intensity  radius
```

## Usage

```
python raytracer.py scene.txt output.png --width 500 --height 500
```

### Arguments

| Argument    | Description                |
| ----------- | -------------------------- |
| scene file  | Input scene description    |
| output file | Output image (.png)        |
| --width     | Image width (default 500)  |
| --height    | Image height (default 500) |
