from builtins import print

from Entities import Cluster, Point
from math import ceil, sqrt
from statistics import mean
from random import shuffle


def approximate_cluster(point_cloud=[]):
    copied_list = point_cloud.copy()
    list_size = len(copied_list)
    shuffle(copied_list)
    loop_times = ceil(list_size / 3)
    grouped_points = []
    centers = []
    radiuses = []

    for i in range(loop_times):
        print(i)
        grouped_points.append([copied_list[(i * 3) % 3], copied_list[(1 + i * 3) % 3], copied_list[(2 + i * 3) % 3]])

    for y in range(len(grouped_points)):
        current_group = grouped_points[y]
        print("Current group: " + str(current_group))
        center_temp = circumcenter(current_group[0], current_group[1], current_group[2])
        centers.append(center_temp)
        radiuses.append(distance(center_temp, current_group[0]))

    center = mean_points(centers)
    radius = mean(radiuses)

    return Cluster(center, radius)


def circumcenter(point_a, point_b, point_c):
    ax = point_a.x
    ay = point_a.y
    bx = point_b.x
    by = point_b.y
    cx = point_c.x
    cy = point_c.y
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return Point(ux, uy)


def distance(p1, p2):
    dist = sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def mean_points(points=[]):
    res = Point()

    for p in points:
        res.x += p.x
        res.y += p.y

    res.x /= len(points)
    res.y /= len(points)

    return res
