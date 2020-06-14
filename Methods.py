import itertools

from Entities import Cluster, Point, Iteration
from math import ceil, sqrt
from statistics import mean
from random import shuffle, randint


def approximate_cluster_by_groups_of_3(point_cloud=[]):
    """From a point cloud assumed to belong to a single cluster, group the points by 3, for each group calculate the
    cluster that contains all 3 points, and get the medium of all clusters """

    # First, we copy the point cloud to avoid modyfing the original one
    copied_list = point_cloud.copy()

    # We obtain the number of points
    list_size = len(copied_list)

    # We shuffle the list to randomize the result
    shuffle(copied_list)

    # We calculate the number of groups of 3 points
    loop_times = ceil(list_size / 3)

    # We instantiate all lists
    grouped_points = []
    centers = []
    radiuses = []

    # For each group, we add a tuple of the 3 next points in the cloud, wrapping around if the number of points is
    # not divisible by 3
    for i in range(loop_times):
        grouped_points.append((copied_list[(i * 3) % list_size], copied_list[(1 + i * 3) % list_size],
                               copied_list[(2 + i * 3) % list_size]))

    # For each tuple of grouped points, we calculate the circumcenter and the radius and add them to their
    # corresponding lists
    for y in range(len(grouped_points)):
        current_group = grouped_points[y]
        center_temp = circumcenter(current_group[0], current_group[1], current_group[2])
        centers.append(center_temp)
        radiuses.append(distance_points(center_temp, current_group[0]))

    # We calculate the mean center and radius for the result
    center = mean_points(centers)
    radius = mean(radiuses)

    return Cluster(center, radius)


def approximate_cluster_by_all_possible_combinations(point_cloud=[]):
    """From a point cloud assumed to belong to a single cluster, get all possible combinations of 3 points, for each"""
    """combination calculate the cluster that contains all 3 points, and get the medium of all clusters"""

    # First, we copy the point cloud to avoid modyfing the original one
    copied_list = point_cloud.copy()

    # We shuffle the list to randomize the result
    shuffle(copied_list)

    # We instantiate all lists
    centers = []
    radiuses = []

    # We instantiate the list with all possible combination of 3 points from the point cloud
    grouped_points = [item for item in itertools.combinations(copied_list, 3)]

    # For each tuple of grouped points, we calculate the circumcenter and the radius and add them to their
    # corresponding lists
    for y in range(len(grouped_points)):
        current_group = grouped_points[y]
        center_temp = circumcenter(current_group[0], current_group[1], current_group[2])
        centers.append(center_temp)
        radiuses.append(distance_points(center_temp, current_group[0]))

    # We calculate the mean center and radius for the result
    center = mean_points(centers)
    radius = mean(radiuses)

    return Cluster(center, radius)


def circumcenter(point_a, point_b, point_c):
    """From three points, calculate the circumcenter"""

    ax = point_a.x
    ay = point_a.y
    bx = point_b.x
    by = point_b.y
    cx = point_c.x
    cy = point_c.y
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        d = 0.1
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return Point(ux, uy)


def distance_points(p1, p2):
    """From two points, calculate the distance between them"""

    dist = sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def distance_point_cluster(point, cluster):
    """From a point and a cluster, calculate the distance between them"""
    dist = distance_points(point, cluster.center)
    return abs(dist - cluster.radius)


def mean_points(points=[]):
    """From a point cloud, calculate the mean point of them all"""
    res = Point()

    for p in points:
        res.x += p.x
        res.y += p.y

    res.x /= len(points)
    res.y /= len(points)

    return res


def belonging_of_point(point, clusters=[]):
    """From a point and a list of clusters, return a dictionary with tuples of (Point, Cluster) as keys and
    the belonging of the point to the cluster as values"""

    # We instantiate the dictionary
    belongings_by_cluster = {}

    # For each cluster, we add the belonging of the point to the cluster to the dictionary
    for c in clusters:
        belongings_by_cluster[(point, c)] = distance_point_cluster(point, c)

    # We instantiate and calculate the sum of all the belongings
    sum_of_belongings = 0
    for i in belongings_by_cluster:
        sum_of_belongings += belongings_by_cluster[i]

    # We normalise the all the belongings
    for c in clusters:
        belongings_by_cluster[(point, c)] = 1 - belongings_by_cluster[(point, c)] / sum_of_belongings

    return belongings_by_cluster


def random_clusters(size, min_val, max_val):
    """From a size number, a minimum and a maximum, return a list of \"size\" clusters with values randomized between
    the min and the max"""

    # We instantiate the list of clusters
    clusters = []

    # For each randomized cluster, we create a random center and a random radius, and add the new cluster to the list
    for i in range(size):
        center = Point(randint(min_val, max_val), randint(min_val, max_val))
        radius = randint(min_val, max_val)
        cluster = Cluster(center, radius)
        clusters.append(cluster)

    return clusters


def iterate(iteration):
    """From an iteration, execute and return the next iteration"""

    # We obtain the dictionary of all the previous belongings
    belongings = iteration.belonging

    # From it, we obtain the point cloud and the previous cluster list
    points = [item[0] for item in belongings.keys()]
    clusters = iteration.clusters

    # We instantiante a dictionary with each cluster as the key, and the list of points that belong to it as value
    points_by_cluster = {}

    # For each point, we assign it in the dictionary to the cluster with max belonging
    for p in points:

        # We extract the belongings of p to each cluster from all the list of all belongings
        belongings_of_p = {item: belongings[item] for item in belongings if item[0] == p}

        # We calculate the max belonging to assign p to the corresponding cluster
        max_belonging = max(belongings_of_p.values())
        assigned_cluster = get_key_from_value(max_belonging, belongings_of_p)[1]

        # We assign the point to the cluster by adding it to the dictionary
        if assigned_cluster not in points_by_cluster:
            points_by_cluster[assigned_cluster] = []
        points_by_cluster[assigned_cluster].append(p)

    # We instantiate the list of updated clusters
    new_clusters = []

    # For each outdated cluster, we
    for c in clusters:
        new_cluster = c
        if c in points_by_cluster:
            # new_cluster = approximate_cluster_by_all_possible_combinations(points_by_cluster[c])
            new_cluster = approximate_cluster_by_groups_of_3(points_by_cluster[c])
        new_clusters.append(new_cluster)

    new_belongings = {}

    for p in points:
        new_belongings_of_p = belonging_of_point(p, new_clusters)
        new_belongings.update(new_belongings_of_p)

    return Iteration(new_clusters, new_belongings)


def get_key_from_value(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key


def clustering(puntos, number_of_clusters):
    # TODO calcularlos a partir de puntos
    # min_value_cluster = 1
    # max_value_cluster = 2
    # clusters_iniciales = random_clusters(number_of_clusters, min_value_cluster, max_value_cluster)
    clusters_iniciales = heuristic_initial_clusters(puntos, number_of_clusters)
    belongings_iniciales = {}
    for p in puntos:
        belongings_iniciales.update(belonging_of_point(p, clusters_iniciales))

    iteracion0 = Iteration(clusters_iniciales, belongings_iniciales)
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
        if old_clusters == current_clusters or counter == 2000:
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
