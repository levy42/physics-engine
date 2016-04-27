def ground(y=0, k=1):
    def _ground(points):
        for p in points:
            if p.pos.y < y:
                p.pos.y = y
                p.pos.x -= (p.pos.x - p.p_pos.x) * k

    return _ground


def function(func):
    def _restriction(points):
        for p in points:
            l = func(p.pos.x)
            if l > p.pos.y:
                p.pos.y = l
    return _restriction
