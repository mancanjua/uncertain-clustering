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
        point = Point(cos(theta) * (radius + (random.random() - 0.5) * noise) + center.x, sin(theta) * (radius + (random.random() - 0.5) * noise) + center.y)
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


def get_method_name (method_number):
    if method_number == 1:
        return "Random Initial Clusters"
    elif method_number == 2:
        return "Heuristic Initial Clusters"
    else:
        return "Heuristic Initial Clusters w/ max distance"


def main():
    win = GraphWin("Results", 800, 600)
    displacement = 20
    puntos_random = create_random_point_cloud(3, 0.1, 1, 10, 20)

    #Puntos elegidos
    chosen_points = puntos_random
    method = Methods.method_heuristic_initial_clusters_max_dist

    points = chosen_points[0]
    solution = chosen_points[1]
    for punto in points:
        p = GPoint(punto.x * displacement, punto.y * displacement)
        p.draw(win)

    iteration_result = Methods.clustering(chosen_points, len(chosen_points[1]), 100, method)

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

def main_iterable ():
    number_of_tries = 100
    error_list = []

    time_start = time()

    # Puntos elegidos
    puntos_random = create_random_point_cloud(3, 1, 1, 10, 20)
    chosen_points = puntos_random
    method = Methods.method_random_initial_clusters

    for i in range(number_of_tries):
        solution = chosen_points[1]

        iteration_result = Methods.clustering(chosen_points, len(chosen_points[1]), 50, method)

        clusters = iteration_result.clusters

        errors = Methods.compare_results(clusters, solution)

        error_list.append(errors)

    time_end = time()

    time_range = time_end-time_start

    print("-----------------------------")
    print("Method used: "+get_method_name(method))
    print("Results after "+str(number_of_tries)+" iterations:")
    print("Total time: "+str(time_range)+" s")
    print("Max error: "+str(max([item[1] for item in error_list])))
    print("Min error: "+str(min([item[2] for item in error_list])))
    print("Median error: "+str(mean([item[0] for item in error_list])))

main()

#main_iterable()
