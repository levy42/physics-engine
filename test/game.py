import math
import pygame
import random

import base.engine2D as engine

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SIZE = (700, 700)
ZOOM = 20
MAX_ZOOM = 100
X = 350
Y = 350


# utils
# ==============================================================================
def trans(x, y):
    return [int(x * ZOOM) + X, SIZE[1] - (int(y * ZOOM) + Y)]


def trans_out(x, y):
    return [float(x - X) / ZOOM, float(SIZE[1] - (y + Y)) / ZOOM]


def catch_point(x, y, world):
    for p in world._points:
        if engine.Vector2D.distance_to(p.pos,
                                       engine.Vector2D(x, y)) < 10.0 / ZOOM:
            return p
    return None


def mark_point(screen, p, color):
    pygame.draw.circle(screen, color, trans(p.pos.x, p.pos.y), 4)


def draw_world(world, screen):
    def draw_layout():
        pygame.draw.line(screen, WHITE, [0, SIZE[0] - Y],
                         [SIZE[0], SIZE[0] - Y], 2)
        pygame.draw.line(screen, WHITE, [X, 0], [X, SIZE[1]], 2)
        n = SIZE[0] / ZOOM
        for i in range(0, n):
            pygame.draw.line(screen, GRAY, [0, (SIZE[1] - Y) % ZOOM + i * ZOOM],
                             [SIZE[0], (SIZE[1] - Y) % ZOOM + i * ZOOM], 1)
            pygame.draw.line(screen, GRAY, [X % ZOOM + i * ZOOM, 0],
                             [X % ZOOM + i * ZOOM, SIZE[1]], 1)

    screen.fill(BLACK)
    draw_layout()
    for p in world._points:
        pygame.draw.circle(screen, GREEN, trans(p.pos.x, p.pos.y), 3)
    for j in world._joints:
        pygame.draw.line(screen, GREEN, trans(j.p1.pos.x, j.p1.pos.y),
                         trans(j.p2.pos.x, j.p2.pos.y), 1)


# =============================================================================
# run
pygame.init()
gameDisplay = pygame.display.set_mode(SIZE)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

crashed = False
# Physic settings
point_mass = 1
joint_k = 0.02
# ==============================================================================
# ini section
# =============================================================================
world = engine.World(2)
for i in range(0, 1, 10):
    points = [engine.Point2D(0, 10 + i, 1), engine.Point2D(1, 20 + i, 1),
              engine.Point2D(10, 10 + i, 1)]
    world.add_points(points)
    world.add_joint(points[0], points[1], 1)
    world.add_joint(points[0], points[2], 1)
    world.add_joint(points[1], points[2], 1)


# =============================================================================
# contollers
# =============================


def zoom_in():
    global ZOOM, X, Y
    if ZOOM < MAX_ZOOM:
        tmp_zoom = ZOOM
        diff = ZOOM / 10 + 1
        ZOOM += diff
        X = SIZE[0] - int((SIZE[0] / 2 - X) * float(ZOOM / tmp_zoom))
        Y = SIZE[1] - int((SIZE[1] / 2 - Y) * float(ZOOM / tmp_zoom))


def zoom_out():
    global ZOOM, X, Y
    if ZOOM > 4:
        tmp_zoom = ZOOM
        diff = ZOOM / 10 + 1
        ZOOM -= diff
        X = SIZE[0] - int((SIZE[0] / 2 - X) * float(ZOOM / tmp_zoom))
        Y = SIZE[1] - int((SIZE[1] / 2 - Y) * float(ZOOM / tmp_zoom))


pressed = None  # None, 'point', 'field', 'joint'
selected_point = None  # clicked point
selected_joint = None  # clicked joint
joint_point = None
move = None
pause = False
x, y = 0, 0  # coordinates of field touch

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
                zoom_in()
            if event.key == pygame.K_KP_MINUS:
                zoom_out()
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_s:
                if selected_point:
                    if not selected_point.is_static:
                        selected_point.fix()
                    else:
                        selected_point.unfix()
        if event.type == pygame.MOUSEMOTION:
            if pressed:
                if move:
                    move = pygame.mouse.get_rel()
                    if pressed == 'field':
                        X += move[0]
                        Y -= move[1]
                else:
                    move = pygame.mouse.get_rel()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                zoom_in()
            if event.button == 5:
                zoom_out()
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                pressed = 'field'
                x, y = trans_out(pos[0], pos[1])
                selected_point = catch_point(x, y, world)
                if selected_point:
                    pressed = 'point'
            if event.button == 2:
                pos = pygame.mouse.get_pos()
                pressed = 'field'
                x, y = trans_out(pos[0], pos[1])
                world.add_point(engine.Point2D(x, y, point_mass))

            if event.button == 3:
                pos = pygame.mouse.get_pos()
                pressed = 'field'
                x, y = trans_out(pos[0], pos[1])
                current_selected_point = catch_point(x, y, world)
                if not current_selected_point:
                    joint_point = None
                else:
                    if joint_point:
                        world.add_joint(joint_point, current_selected_point,
                                        joint_k)
                        joint_point = None
                    else:
                        joint_point = current_selected_point

        if event.type == pygame.MOUSEBUTTONUP:
            move = None
            pressed = None
            selected_point = None

    if selected_point:
        pos = pygame.mouse.get_pos()
        pos = trans_out(pos[0], pos[1])
        selected_point.pos.x = pos[0]
        selected_point.pos.y = pos[1]
        if pause:
            selected_point.p_pos.x = pos[0]
            selected_point.p_pos.y = pos[1]


    if not pause:
        world.step(1.0 / 60)
    draw_world(world, gameDisplay)
    if selected_point:
        mark_point(gameDisplay, selected_point, RED)
    if joint_point:
        mark_point(gameDisplay, joint_point, YELLOW)
    pygame.display.update()
    clock.tick(60)
