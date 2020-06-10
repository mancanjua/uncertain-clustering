from Entities import Cluster, Point, Iteration
import Methods
import itertools

p = Point()

print(p)

c1 = Cluster()
print(c1)

p = Point(1, 2)

print(p)

cluster1 = Cluster(radius=5, center=Point(1, 2))
cluster2 = Cluster(radius=2, center=Point(6, 9))

clusters = [cluster1, cluster2]
ownership = {(Point(4, 7), cluster1): 5, (Point(4, 7), cluster2): 3, (Point(2, 3), cluster1): 2, (Point(2, 3), cluster2): 10}

i = Iteration(clusters=clusters, ownership=ownership)

print(i)

asd = (Point(1, 2), Point(1, 6), Point(6, 9))
asd2 = [Point(1, 2), Point(1, 6), Point(6, 9)]

print(asd)
print(asd[2])

print(asd2[1])

nube_puntos = [Point(1, 1), Point (1, -1), Point (-1, 1), Point (-1, -1)]

print(Methods.approximate_cluster_by_groups_of_3(nube_puntos))

print(Methods.approximate_cluster_by_all_possible_combinations(nube_puntos))

print ("patata")
print (Methods.distance_point_cluster(p, cluster1))
print (Methods.distance_point_cluster(p, cluster2))
print (Methods.ownership_of_point(p, clusters))

print ("patta2")
print (Methods.random_clusters(3, 0, 5))

print("patata3")
ownerships_of_p = {item: ownership[item] for item in ownership if item[0] == Point(4, 7)}
print(ownerships_of_p)

#TODO (test shit)
#Crear una iteration por los jajas
#Y testearla con Methods.iterate()