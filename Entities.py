class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + 31 ** 2 * hash(self.y)


class Cluster:

    def __init__(self, center=Point(), radius=0):
        self.radius = radius
        self.center = center

    def __repr__(self):
        return "{R: " + str(self.radius) + ", C: " + str(self.center) + "}"

    def __hash__(self):
        return 31 * hash(self.radius) + 31 ** 2 * hash(self.center)

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius


class Iteration:
    def __init__(self, clusters=[], ownership={}):
        self.clusters = clusters
        self.ownership = ownership

    def __repr__(self):
        return "{Clusters: " + str(self.clusters) + ", Ownership: " + str(self.ownership) + "}"
