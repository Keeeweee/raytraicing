from Shapes.Shape import Shape
from Shapes.HitRecord import HitRecord
from Shapes.ShapeList import ShapeList
from Shapes.Sphere import Sphere
from Materials.Lambertian import Lambertian
from Materials.Metal import Metal
from Materials.Dielectric import Dielectric
from pyrr import Vector3 as vec3
from PpmDrawer import PpmDrawer
from Ray import Ray
from Camera import Camera
from random import random
from math import pi, cos

MAXFLOAT = 1000000
nx = 200
ny = 100
ns = 100


def blueBlend(ray: Ray) -> vec3:
    t = 0.5 * (ray.direction.y + 1.0)
    return (1.0 - t) * vec3([1.0, 1.0, 1.0]) + t * vec3([0.5, 0.7, 1.0])


def colorRay(ray: Ray, world: Shape, depth: int) -> vec3:
    rec = HitRecord()
    if world.hit(ray, 0.001, MAXFLOAT, rec):
        scattered = Ray(vec3([0.0, 0.0, 0.0]), vec3([0.0, 0.0, 0.0]))
        attenuation = vec3()
        if depth < 50 and rec.material.scatter(ray, rec, attenuation, scattered):
            return attenuation * colorRay(scattered, world, depth + 1)
        else:
            return vec3([0.0, 0.0, 0.0])

    return blueBlend(ray)


def paintWorld():
    ppmDrawer = PpmDrawer("graduation.ppm", nx, ny)

    lookFrom = vec3([3.0, 3.0, 2.0])
    lookAt = vec3([0.0, 0.0, -1.0])
    vUp = vec3([0.0, 1.0, 0.0])
    distToFocus = (lookFrom - lookAt).length
    aperture = 2.0
    camera = Camera(lookFrom, lookAt, vUp, 90.0 / 4.0, float(nx) / float(ny), aperture, distToFocus)

    points = []

    # world = ShapeList()
    # world.append(Sphere(vec3([-R, 0.0, -1.0]),
    #                     R,
    #                     Lambertian(vec3([0.0, 0.0, 1.0]))))
    # world.append(Sphere(vec3([R, 0.0, -1.0]),
    #                     R,
    #                     Lambertian(vec3([1.0, 0.0, 0.0]))))

    # world.append(Sphere(vec3([0.0, 0.0, -1.0]),
    #                     0.5,
    #                     Lambertian(vec3([0.1, 0.2, 0.5]))))
    # world.append(Sphere(vec3([0.0, -100.5, -1.0]),
    #                     100,
    #                     Lambertian(vec3([0.8, 0.8, 0.0]))))
    # world.append(Sphere(vec3([1.0, 0.0, -1.0]),
    #                     0.5,
    #                     Metal(vec3([0.8, 0.6, 0.2]), 0.3)))
    # world.append(Sphere(vec3([-1.0, 0.0, -1.0]),
    #                     0.5,
    #                     Dielectric(1.5)))
    # world.append(Sphere(vec3([-1.0, 0.0, -1.0]),
    #                     -0.45,
    #                     Dielectric(1.5)))

    world = graduation()

    count = 0
    last = 0

    for j in range(ny, 0, -1):
        for i in range(nx):

            new = int((count * 100) / (nx * ny))
            if last != new:
                print("Progress: " + str(last) + "%", end="\n")
                last = new
            count += 1

            col = vec3([0.0, 0.0, 0.0])
            for s in range(ns):
                u = (i + random()) / nx
                v = (j + random()) / ny

                ray = camera.getRay(u, v)
                col += colorRay(ray, world, 0)

            col = col / ns

            points.append(col)

    ppmDrawer.writePpm(points)


def graduation():
    world = ShapeList()
    world.append(Sphere(vec3([0.0, -1000.0, 0]),
                        1000.0,
                        Lambertian(vec3([0.5, 0.5, 0.5]))))
    for a in range(-11, 11):
        for b in range(-11, 11):
            chooseMat = random()
            center = vec3([a + 0.9 * random(), 0.2, b + 0.9 * random()])
            if (center - vec3([4.0, 0.2, 0.0])).length > 0.9:
                if chooseMat < 0.8:  # Lambertian
                    world.append(Sphere(center,
                                        0.2,
                                        Lambertian(
                                            vec3([random() * random(), random() * random(), random() * random()]))))
                elif chooseMat < 0.95:  # Metal
                    world.append(Sphere(center,
                                        0.2,
                                        Metal(
                                            vec3([1+random(), 1+random(), 1+random()]), 0.5*random())))
                else:  # Glass
                    world.append(Sphere(center, 0.2, Dielectric(1.5)))

    world.append(Sphere(vec3([0.0, 1.0, 0.0]), 1.0, Dielectric(1.5)))
    world.append(Sphere(vec3([-4.0, 1.0, 0.0]), 1.0, Lambertian(vec3([0.4, 0.2, 0.1]))))
    world.append(Sphere(vec3([4.0, 1.0, 0.0]), 1.0, Metal(vec3([0.7, 0.6, 0.5]), 0.0)))

    return world


def main():
    paintWorld()


if __name__ == "__main__":
    main()
