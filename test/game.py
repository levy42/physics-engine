import math
import pygame

import base.engine2D as engine

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)

SIZE = (600, 600)
ZOOM = 20
D = 20
B_D = 20
X = 300
Y = 300


def draw_world(world, screen):
    def trans(x, y):
        return [int(x * ZOOM) + X, SIZE[1] - (int(y * ZOOM) + Y)]

    def draw_layout():
        pygame.draw.line(screen, WHITE, [0, SIZE[0] - Y],
                         [SIZE[0], SIZE[0] - Y], 2)
        pygame.draw.line(screen, WHITE, [X, 0], [X, SIZE[1]], 2)
        d = D
        n = SIZE[0] / d
        for i in range(0, n / 2):
            pygame.draw.line(screen, GRAY, [0, SIZE[0] - Y + i * d],
                             [SIZE[0], SIZE[0] - Y + i * d], 1)
            pygame.draw.line(screen, GRAY, [X + i * d, 0],
                             [X + i * d, SIZE[1]], 1)

    screen.fill(BLACK)
    draw_layout()
    for p in world._points:
        pygame.draw.circle(screen, GREEN, trans(p.pos.x, p.pos.y), 3)
    for j in world._joints:
        pygame.draw.line(screen, GREEN, trans(j.p1.pos.x, j.p1.pos.y),
                         trans(j.p2.pos.x, j.p2.pos.y), 1)


pygame.init()
gameDisplay = pygame.display.set_mode(SIZE)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

crashed = False

# ini section
# =============================================================================
world = engine.World(2)
for i in range(0, 100, 10):
    points = [engine.Point2D(0, 10 + i, 1), engine.Point2D(1, 20 + i, 1),
              engine.Point2D(10, 10 + i, 1)]
    world.add_points(points)
    world.add_joint(points[0], points[1], 1)
    world.add_joint(points[0], points[2], 1)
    world.add_joint(points[1], points[2], 1)
# =============================================================================

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X += 10
            if event.key == pygame.K_RIGHT:
                X -= 10
            if event.key == pygame.K_UP:
                Y -= 10
            if event.key == pygame.K_DOWN:
                Y += 10
            if event.key == pygame.K_KP_PLUS:
                if ZOOM > B_D:
                    ZOOM += ZOOM / B_D
                else:
                    ZOOM += 1
                D += 1
                if D == 40:
                    D = 20
            if event.key == pygame.K_KP_MINUS:
                if ZOOM > B_D:
                    ZOOM -= ZOOM / B_D
                else:
                    ZOOM -= 1
                D -= 1
                if D == 19:
                    D = 40

    world.step(1.0 / 60)
    draw_world(world, gameDisplay)
    pygame.display.update()
    clock.tick(60)
