def ground(y=0, k=1):
    def _ground(points):
        for p in points:
            if p.pos.y < y:
                p.pos.y = y
                p.pos.x -= (p.pos.x - p.p_pos.x) * k
    return _ground

def function(points, func):
    def _restriction(points):
        pass


print 'hey' in 'hed ey gt\n ergrt'