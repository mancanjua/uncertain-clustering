from Entities import Cluster, Point, Iteration
import Methods
from graphics import Circle, GraphWin, Point as GPoint
import itertools
import random
from puntos import *
from math import *
from time import time
from statistics import mean


def create_random_circle(center, radius, quantity, noise):
    points = []

    for i in range(int(quantity)):
        theta = random.random() * 2 * pi
        point = Point(cos(theta) * (radius + (random.random() - 0.5) * noise) + center.x,
                      sin(theta) * (radius + (random.random() - 0.5) * noise) + center.y)
        points.append(point)

    return points


def create_random_point_cloud(number_of_circles, noise, min_val, max_val, max_points_per_circle):
    point_cloud = []
    solutions = []
    val_range = max_val - min_val

    for i in range(number_of_circles):
        random_center_x = random.random() * val_range
        random_center_y = random.random() * val_range
        random_center = Point(random_center_x, random_center_y)
        random_radius = random.random() * val_range
        random_points_per_circle = (random.random() + 0.5) * max_points_per_circle
        current_circle = create_random_circle(random_center, random_radius, random_points_per_circle, noise)

        point_cloud += current_circle
        solutions.append(Cluster(random_center, random_radius))

    res = (point_cloud, solutions)

    return res


def get_method_name(method_number):
    if method_number == 1:
        return "Random Initial Clusters"
    elif method_number == 2:
        return "Heuristic Initial Clusters"
    else:
        return "Heuristic Initial Clusters w/ max distance"


def test(data, max_iterations=100, method=Methods.method_heuristic_initial_clusters_max_dist):
    win = GraphWin("Results", 800, 600)
    displacement = 20

    points = data[0]
    solution = data[1]

    for point in points:
        p = GPoint(point.x * displacement, point.y * displacement)
        p.draw(win)

    iteration_result = Methods.clustering(points, len(points), max_iterations, method)

    clusters = iteration_result.clusters

    for c in clusters:
        c = Circle(GPoint(c.center.x * displacement, c.center.y * displacement), c.radius * displacement)
        c.draw(win)

    print(Methods.compare_results(clusters, solution))

    try:
        win.getMouse()
        win.close()
    except:
        return 0


def test_efficiency(data, max_iterations=100, times=100, method=Methods.method_heuristic_initial_clusters_max_dist):
    error_list = []

    time_start = time()

    points = data[0]
    solution = data[1]

    for i in range(times):
        iteration_result = Methods.clustering(points, len(points), max_iterations, method)

        clusters = iteration_result.clusters

        errors = Methods.compare_results(clusters, solution)

        error_list.append(errors)

    time_end = time()

    time_range = time_end - time_start

    print("-----------------------------")
    print("Method used: " + get_method_name(method))
    print("Results after " + str(max_iterations) + " iterations:")
    print("Total time: " + str(time_range) + " s")
    print("Max error: " + str(max([item[1] for item in error_list])))
    print("Min error: " + str(min([item[2] for item in error_list])))
    print("Median error: " + str(mean([item[0] for item in error_list])))

# PRUEBA
