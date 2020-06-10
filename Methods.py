import itertools
from builtins import print

from Entities import Cluster, Point, Iteration
from math import ceil, sqrt
from statistics import mean
from random import shuffle, randint
import random


def approximate_cluster_by_groups_of_3(point_cloud=[]):
    copied_list = point_cloud.copy()
    list_size = len(copied_list)
    shuffle(copied_list)
    loop_times = ceil(list_size / 3)
    grouped_points = []
    centers = []
    radiuses = []

    for i in range(loop_times):
        grouped_points.append((copied_list[(i * 3) % list_size], copied_list[(1 + i * 3) % list_size],
                               copied_list[(2 + i * 3) % list_size]))

    for y in range(len(grouped_points)):
        current_group = grouped_points[y]
        center_temp = circumcenter(current_group[0], current_group[1], current_group[2])
        centers.append(center_temp)
        radiuses.append(distance_points(center_temp, current_group[0]))

    center = mean_points(centers)
    radius = mean(radiuses)

    return Cluster(center, radius)


def approximate_cluster_by_all_possible_combinations(point_cloud=[]):
    copied_list = point_cloud.copy()
    shuffle(copied_list)
    centers = []
    radiuses = []

    grouped_points = [item for item in itertools.combinations(copied_list, 3)]

    for y in range(len(grouped_points)):
        current_group = grouped_points[y]
        center_temp = circumcenter(current_group[0], current_group[1], current_group[2])
        centers.append(center_temp)
        radiuses.append(distance_points(center_temp, current_group[0]))

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


def distance_points(p1, p2):
    dist = sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def distance_point_cluster(point, cluster):
    dist = distance_points(point, cluster.center)
    return abs(dist - cluster.radius)


def mean_points(points=[]):
    res = Point()

    for p in points:
        res.x += p.x
        res.y += p.y

    res.x /= len(points)
    res.y /= len(points)

    return res


def ownership_of_point(point, clusters=[]):
    belongings_by_cluster = {}

    for c in clusters:
        belongings_by_cluster[(point, c)] = distance_point_cluster(point, c)

    sum_of_belongings = 0
    for i in belongings_by_cluster:
        sum_of_belongings += belongings_by_cluster[i]

    for c in clusters:
        belongings_by_cluster[(point, c)] = belongings_by_cluster[(point, c)] / sum_of_belongings

    return belongings_by_cluster


def random_clusters(size, min_val, max_val):
    clusters = []
    for i in range(size):
        center = Point(randint(min_val, max_val))
        print(center)
        radius = randint(min_val+1, max_val)
        print(radius)
        cluster = Cluster(center, radius)
        print(cluster)
        clusters.append(cluster)

    return clusters

def iterate(iteration):
    ownerships = iteration.ownership
    points = [item[0] for item in ownerships.keys()]
    clusters = iteration.clusters

    #Clave Cluster, Valor [Punto]
    points_by_cluster = {}

    #Dividimos los puntos según el cluster con mayor grado de pertenencia
    for p in points:
        #Clave (Punto, Cluster), Valor Pertenencia
        ownerships_of_p = {item: ownerships[item] for item in ownerships if item[0] == p}

        max_ownership = max(ownerships_of_p.values())

        assigned_cluster = get_key_from_value(max_ownership, ownerships_of_p)[1]

        points_by_cluster[assigned_cluster].append(p)

    new_clusters = []

    for c in clusters:
        new_cluster = approximate_cluster_by_all_possible_combinations(points_by_cluster[c])
        new_clusters.append(new_cluster)

    new_ownerships = {}

    for p in points:
        new_ownerships_of_p = ownership_of_point(p, new_clusters)
        new_ownerships.update(new_ownerships_of_p)

    return Iteration(new_clusters, new_ownerships)


def get_key_from_value(val, dictionary):
    for key,value in dictionary.items():
        if val == value:
            return key
