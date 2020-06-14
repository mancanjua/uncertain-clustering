import itertools

from Entities import Cluster, Point, Iteration
from math import ceil, sqrt
from statistics import mean
from random import shuffle, randint


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
    d += 0.1
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
        center = Point(randint(min_val, max_val), randint(min_val, max_val))
        radius = randint(min_val + 1, max_val)
        cluster = Cluster(center, radius)
        clusters.append(cluster)

    return clusters


def iterate(iteration):
    ownerships = iteration.ownership
    points = [item[0] for item in ownerships.keys()]
    clusters = iteration.clusters

    # Clave Cluster, Valor [Punto]
    points_by_cluster = {}

    # Dividimos los puntos según el cluster con mayor grado de pertenencia
    for p in points:
        # Clave (Punto, Cluster), Valor Pertenencia
        ownerships_of_p = {item: ownerships[item] for item in ownerships if item[0] == p}

        max_ownership = max(ownerships_of_p.values())

        assigned_cluster = get_key_from_value(max_ownership, ownerships_of_p)[1]

        if assigned_cluster not in points_by_cluster:
            points_by_cluster[assigned_cluster] = []

        points_by_cluster[assigned_cluster].append(p)

    new_clusters = []

    for c in clusters:
        new_cluster = c
        if c in points_by_cluster:
            #new_cluster = approximate_cluster_by_all_possible_combinations(points_by_cluster[c])
            new_cluster = approximate_cluster_by_groups_of_3(points_by_cluster[c])
        new_clusters.append(new_cluster)

    new_ownerships = {}

    for p in points:
        new_ownerships_of_p = ownership_of_point(p, new_clusters)
        new_ownerships.update(new_ownerships_of_p)

    return Iteration(new_clusters, new_ownerships)


def get_key_from_value(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key


def clustering(puntos, number_of_clusters):
    #TODO calcularlos a partir de puntos
    #min_value_cluster = 1
    #max_value_cluster = 2
    #clusters_iniciales = random_clusters(number_of_clusters, min_value_cluster, max_value_cluster)
    clusters_iniciales = heuristic_initial_clusters(puntos, number_of_clusters)
    ownerships_iniciales = {}
    for p in puntos:
        ownerships_iniciales.update(ownership_of_point(p, clusters_iniciales))

    iteracion0 = Iteration(clusters_iniciales, ownerships_iniciales)
    old_clusters = clusters_iniciales
    current_clusters = []
    iteration = iteracion0
    counter = 0
    while True:

        old_clusters = iteration.clusters

        iteration = iterate(iteration)

        current_clusters = iteration.clusters
        print(current_clusters)
        counter+=1
        print(counter)
        if old_clusters == current_clusters or counter == 500:
            break

    return iteration


def heuristic_initial_clusters(points, number_of_clusters):

    all_x = [item.x for item in points]
    all_y = [item.y for item in points]

    max_x = max(all_x)
    min_x = min(all_x)
    max_y = max(all_y)
    min_y = min(all_y)

    range_x = max_x - min_x
    range_y = max_y - min_y

    if range_x > range_y:
        sorted(points, key=lambda point: point.x)
    else:
        sorted(points, key=lambda point: point.y)

    grouped_points = chunkIt(points, number_of_clusters)

    clusters = []

    for group in grouped_points:
        clusters.append(approximate_cluster_by_all_possible_combinations(group))

    return clusters

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out
