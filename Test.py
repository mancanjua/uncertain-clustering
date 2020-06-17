from Entities import Cluster, Point, Iteration
import Methods
from graphics import Circle, GraphWin, Point as GPoint
import itertools
import random
from puntos import *
from math import *

"""

p = Point()

print(p)

c1 = Cluster()
print(c1)

p = Point(1, 2)

print(p)

cluster1 = Cluster(radius=5, center=Point(1, 2))
cluster2 = Cluster(radius=2, center=Point(6, 9))

clusters = [cluster1, cluster2]
ownership = {(Point(4, 7), cluster1): 5, (Point(4, 7), cluster2): 3, (Point(2, 3), cluster1): 2,
             (Point(2, 3), cluster2): 10}

i = Iteration(clusters=clusters, ownership=ownership)

print(i)

asd = (Point(1, 2), Point(1, 6), Point(6, 9))
asd2 = [Point(1, 2), Point(1, 6), Point(6, 9)]

print(asd)
print(asd[2])

print(asd2[1])

nube_puntos = [Point(1, 1), Point(1, -1), Point(-1, 1), Point(-1, -1)]

print(Methods.approximate_cluster_by_groups_of_3(nube_puntos))

print(Methods.approximate_cluster_by_all_possible_combinations(nube_puntos))

print("patata")
print(Methods.distance_point_cluster(p, cluster1))
print(Methods.distance_point_cluster(p, cluster2))
print(Methods.ownership_of_point(p, clusters))

print("patta2")
print(Methods.random_clusters(3, 0, 5))

print("patata3")
ownerships_of_p = {item: ownership[item] for item in ownership if item[0] == Point(4, 7)}
print(ownerships_of_p)


# TODO (test shit)
# Crear una iteration por los jajas
# Y testearla con Methods.iterate()

"""


def create_random_circle(center, radius, quantity, noise):
    points = []

    for i in range(int(quantity)):
        theta = random.random() * 2 * pi
        noise_x = (random.random() - 0.5) * noise
        noise_y = (random.random() - 0.5) * noise
        point = Point(cos(theta) * radius + noise_x + center.x, sin(theta) * radius + noise_y + center.y)
        points.append(point)

    return points


def create_random_point_cloud(number_of_circles, noise, min_val, max_val, max_points_per_circle):
    point_cloud = []
    val_range = max_val - min_val

    for i in range(number_of_circles):
        random_center_x = random.random() * val_range
        random_center_y = random.random() * val_range
        random_center = Point(random_center_x, random_center_y)
        random_radius = random.random() * val_range
        random_points_per_circle = (random.random() + 0.5) * max_points_per_circle
        current_circle = create_random_circle(random_center, random_radius, random_points_per_circle, noise)

        point_cloud += current_circle

    return point_cloud


def main():
    win = GraphWin("Results", 1400, 800)
    displacement = 20
    puntos_random = create_random_point_cloud(2, 0.2, 200, 250, 50)

    #Puntos elegidos
    chosen_points = puntos4
    for punto in chosen_points:
        p = GPoint(punto.x * displacement, punto.y * displacement)
        p.draw(win)

    iteration_result = Methods.clustering(chosen_points, 6, 200)

    clusters = iteration_result.clusters

    for c in clusters:
        c = Circle(GPoint(c.center.x * displacement, c.center.y * displacement), c.radius * displacement)
        c.draw(win)

    try:
        win.getMouse()
        win.close()
    except:
        return 0


main()
