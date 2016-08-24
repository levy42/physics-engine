"""Simple debug test for human run only"""

from base.engine2D import World, Point2D, Vector2D

world = World(10, gravity=Vector2D(0,-0.1), debug=True)
points = [Point2D(0, 1, 1), Point2D(1, 1, 1)]
world.add_points(points)
world.add_joint(points[0], points[1], 1)
print(f"init joint length: {world._joints[0].length}")
points[0].pos.x += 0.1

for i in range(1):
    world.step(0.01)