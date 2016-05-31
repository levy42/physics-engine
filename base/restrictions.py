import engine2D as eng


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
            dl = l - p.pos.y
            if dl > 0:
                k = (l - func(p.pos.x + 0.01)) / 0.01
                _k = -1 / k
                p.pos.x += dl * k
                x_v = p.pos - p.p_pos
                p.pos -= eng.Vector2D.proection(x_v, eng.Vector2D(1,_k))
                p.pos.y = l

    return _restriction
