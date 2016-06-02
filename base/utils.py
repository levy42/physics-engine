from base.engine2D import Vector2D


def vector_point_position(p1, p2, p):
    """Returns True if point is upon vector and False if point is under."""
    k = (p1.y - p2.y) / (p1.x - p2.x)
    b = p1.y - p.x * k
    return p.y - k * p.x - b >= 0


def line_intersection(p1, p2, p3, p4):
    """Returns Vectror2D. or None"""
    dx = (p1.x - p2.x)
    if dx == 0:
        dx += 0.001
    k = (p1.y - p2.y) / dx
    b = p1.y - p3.x * k
    position1 = p3.y - k * p3.x - b >= 0
    position2 = p4.y - k * p4.x - b >= 0
    if position1 == position2:
        return
    _dx = (p3.x - p4.x)
    if _dx == 0:
        _dx += 0.001
    _k = (p3.y - p4.y) / _dx
    _b = p3.y - p3.x * _k
    x = (_b - b) / (k - _k)
    y = _k * x + _b
    if (x < p1.x and x < p2.x) or (x > p1.x and x > p2.x):
        return
    return Vector2D(x, y)
#
# p1 = Vector2D(0, 0)
# p2 = Vector2D(4, 4)
# p3 = Vector2D(0, 4)
# p4 = Vector2D(4, 0)
# print line_intersection(p1, p2, p3, p4)
# import time
#
# t1 = time.time()
# for i in range(0, 1000):
#     line_intersection(p1, p2, p3, p4)
# t2 = time.time()
# print t2 - t1
