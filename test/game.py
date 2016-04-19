import pygame
import base.engine2D as engine

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SIZE = (600, 600)


def draw_world(world, screen):
    ZOOM = 10
    X = 300
    Y = 300

    def trans(x, y):
        return [int(x * ZOOM) + X, SIZE[1] - (int(y * ZOOM) + Y)]


    def draw_layout():
        pygame.draw.line(screen, WHITE, [Y, 0], [Y, SIZE[0]], 2)
        pygame.draw.line(screen, WHITE, [0, X], [SIZE[1], X], 2)

    screen.fill(BLACK)
    for p in world._points:
        pygame.draw.circle(screen, GREEN, trans(p.pos.x, p.pos.y), 3)
    for j in world._joints:
        pygame.draw.line(screen, GREEN, trans(j.p1.pos.x, j.p1.pos.y),
                         trans(j.p2.pos.x, j.p2.pos.y), 1)

    draw_layout()


pygame.init()
gameDisplay = pygame.display.set_mode(SIZE)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

crashed = False

# ini section
# =============================================================================
world = engine.World(2)
for i in range(0, 100):
    points = [engine.Point2D(0, 10 + i, 1), engine.Point2D(1, 20 + i, 1), engine.Point2D(10, 10 + i, 1)]
    world.add_points(points)
    world.add_joint(points[0], points[1], 1)
    world.add_joint(points[0], points[2], 1)
    world.add_joint(points[1], points[2], 1)
# =============================================================================

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    world.step(1.0 / 60)
    draw_world(world, gameDisplay)
    pygame.display.update()
    clock.tick(60)
