class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"


class Cluster:

    def __init__(self, center=Point(), radius=0):
        self.radius = radius
        self.center = center

    def __repr__(self):
        return "{R: "+str(self.radius)+", C: "+str(self.center)+"}"


class Iteration:
    def __init__(self, clusters=[], ownership={}):
        self.clusters = clusters
        self.ownership = ownership

    def __repr__(self):
        return "{Clusters: "+str(self.clusters)+", Ownership: "+str(self.ownership)+"}"
