import math

import restrictions


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

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def proection(self, other):
        l = len(other)
        return self / l

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
        self.is_static = False

    def set_pos(self, x, y):
        """
        use this method when you want to move your point
        to some position and terminate it`s moving
        """
        self.pos.x = x
        self.p_pos.x = x
        self.pos.y = y
        self.p_pos.y = y

    def fix(self):
        """
        makes point unmovable,
        gravity and any other interaction would not move it
        """
        self._mass = self.mass
        self.mass = float("inf")
        self.is_static = True

    def unfix(self):
        """
        makes point movable
        """
        if self.is_static:
            self.mass = self._mass
            self.is_static = False


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
        if math.isnan(self._dm1): self._dm1 = k
        if math.isnan(self._dm2): self._dm2 = k


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
    G = Vector2D(0, -9.8)

    def __init__(self, n_pos, ground=restrictions.ground()):
        self.n_pos = n_pos
        self._ground = ground

    def step(self, dt):
        for p in self._points:
            p.pos += self.G * dt * dt
        for i in range(0, self.n_pos):
            for j in self._joints:
                l = Vector2D.distance_to(j.p1.pos, j.p2.pos)
                dl = j.length - l
                r = (j.p1.pos - j.p2.pos) / l * dl
                j.p1.pos += r * j._dm2 / self.n_pos
                j.p2.pos -= r * j._dm1 / self.n_pos

        self.ground()
        for p in self._points:
            if not p.is_static:
                tmp = p.pos
                p.pos += p.pos - p.p_pos
                p.p_pos = tmp
            else:
                p.pos = p.p_pos

    def ground(self, y=0):
        if self._ground:
            self._ground(self._points)

    def add_point(self, point):
        self._points.append(point)

    def add_points(self, points):
        self._points += points

    def add_joint(self, p1, p2, k, length=None):
        self._joints.append(Joint(p1, p2, k, length=length))
