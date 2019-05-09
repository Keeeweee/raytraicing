from Shapes.Shape import *
from pyrr import Vector3 as vec3
from Ray import Ray
from math import sqrt


class Sphere(Shape):
    def __init__(self, center: vec3, radius: float):
        self.center = center
        self.radius = radius

    def _recordHit(self, t: float, ray: Ray, rec: List[HitRecord]):
        rec[0].t = t
        rec[0].p = ray.pointAtParameter(rec[0].t)
        rec[0].normal = (rec[0].p - self.center) / self.radius

    def hit(self, ray: Ray, t_min: float, t_max: float, rec: List[HitRecord]) -> bool:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = oc.dot(ray.direction)
        c = oc.dot(oc) - (self.radius ** 2)
        discriminant = (b ** 2) - (a * c)

        if discriminant > 0:
            temp = (-b - sqrt((b**2) - (a * c))) / a
            if t_min < temp < t_max:
                self._recordHit(temp, ray, rec)
                return True

            temp = (-b + sqrt((b ** 2) - (a * c))) / a
            if t_min < temp < t_max:
                self._recordHit(temp, ray, rec)
                return True

        return False