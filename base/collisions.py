import utils as u


class CollisionLine(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


class StaticCollisionLine(object):
    def __init__(self, location1, location2):
        self.l1 = location1
        self.l2 = location2


class StaticCollisionStrip(object):
    def __init__(self, points):
        self.points = points


class CollisionSolver():
    def __init__(self, collision_bodies):
        self.collision_bodies = list()
        self.collision_bodies += collision_bodies

    def step(self):
        pass

    def solve_l_p(self, line, point):
        intersection = u.line_intersection(line.p1.pos, line.p2.pos, point.pos,
                                           point.p_pos)
        if not intersection:
            return
        k = (intersection.x - line.p1.pos.x) / (line.p1.pos.x - line.p12.pos.x)
        k1 = k
        k2 = 1 - k
