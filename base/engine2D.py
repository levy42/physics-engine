import math


class Vector2D(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __int__(self):
        return type(self)(int(self.x), int(self.y))

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return type(self)(self.x * other, self.y * other)

    def __div__(self, other):
        return type(self)(self.x / other, self.y / other)

    def __str__(self):
        return str((self.x, self.y))

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def distance_to(self, other):
        """ uses the Euclidean norm to calculate the distance """
        return math.sqrt((self.x - other.x) * (self.x - other.x)
                         + (self.y - other.y) * (self.y - other.y))

class Point2D(object):
    """
    mass - mass of point
    pos :Vector2D(x,y) - current position
    ppos :Vector2D(x,y) - previous position
    Represent a simple point with position and mass
    """
    def __init__(self, x, y, mass):
        """
        (float x, float y, float mass)
        """
        self.pos = Vector2D(x, y)
        self.p_pos = Vector2D(x, y)
        self.mass = float(mass)

class Joint(object):
    """
    Represent a simple joint of 2 points that restrict distance between them
    """
    def __init__(self, p1, p2, k, length=None):
        self.p1 = p1
        self.p2 = p2
        self.k = k
        self.length = length if length else Vector2D.distance_to(p1.pos, p2.pos)
        # dm{1,2} uses for joint calculations
        self._dm1 = p1.mass / (p1.mass + p2.mass) * k
        self._dm2 = p2.mass / (p1.mass + p2.mass) * k


class World(object):
    """
    points - all points
    joints - all joints
    G - gravity
    n_pos - count of position calculations
    _ground - True if ground is enabled
    """
    _points = []
    _joints = []
    G = Vector2D(0, 0)

    def __init__(self, n_pos, ground=True):
        self.n_pos = n_pos
        if ground:
            self._ground = True

    def step(self, dt):
        for p in self._points:
            p.pos += self.G * dt * dt

        for i in range(0, self.n_pos):
            for j in self._joints:
                l = Vector2D.distance_to(j.p1.pos, j.p2.pos)
                dl = j.length - l
                r = (j.p1.pos - j.p2.pos) / l * dl
                j.p1.pos -= r * j._dm2 / self.n_pos
                j.p2.pos += r * j._dm1 / self.n_pos

        for p in self._points:
            tmp = p.pos
            p.pos += p.pos - p.p_pos
            p.p_pos = tmp

    def add_point(self, point):
        self._points.append(point)

    def add_points(self, points):
        self._points += points

    def add_joint(self, p1, p2, k, length=None):
        self._joints.append(Joint(p1, p2, k, length=length))


world = World(2)
points = [Point2D(0,0,1),Point2D(0,10,1)]
world.add_points(points)
world.add_joint(points[0], points[1],0.1, length=20)
for i in range(0, 100):
    world.step(1.0 / 60)
    print('==========')
    for p in points:
        print(p.pos)



