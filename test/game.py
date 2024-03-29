import math
import time

import pygame
import pygame.camera

import base.engine2D as engine
from base.engine2D import Vector2D

FPS = 30
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GROUND = (234, 45, 35)
SIZE = (700, 700)
ZOOM = 100
MAX_ZOOM = 500
X = 350
Y = 350


def ground(x):
    return math.sin(x)


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


def draw_ground(screen, func):
    pc = trans_out(0, 0)
    for i in range(1, 1000):
        x = float(i - X) / ZOOM
        p = trans(x, func(x))
        pygame.draw.line(screen, GROUND, pc, p, 2)
        pc = p


def draw_world(world, screen):
    def draw_layout():
        pygame.draw.line(screen, WHITE, [0, SIZE[0] - Y],
                         [SIZE[0], SIZE[0] - Y], 2)
        pygame.draw.line(screen, WHITE, [X, 0], [X, SIZE[1]], 2)
        n = int(SIZE[0] // ZOOM)
        for i in range(0, n):
            pygame.draw.line(screen, GRAY, [0, (SIZE[1] - Y) % ZOOM + i * ZOOM],
                             [SIZE[0], (SIZE[1] - Y) % ZOOM + i * ZOOM], 1)
            pygame.draw.line(screen, GRAY, [X % ZOOM + i * ZOOM, 0],
                             [X % ZOOM + i * ZOOM, SIZE[1]], 1)

    screen.fill(BLACK)
    draw_layout()
    draw_ground(screen, ground)
    for p in world._points:
        pygame.draw.circle(screen, GREEN, trans(p.pos.x, p.pos.y), 3)
    for j in world._joints:
        pygame.draw.line(screen, GREEN, trans(j.p1.pos.x, j.p1.pos.y),
                         trans(j.p2.pos.x, j.p2.pos.y), 1)

def create_circle(world, x:float, y:float, n: int, r: float=1, k=1):
    center = engine.Point2D(x, y, 1)
    world.add_point(center)
    angle_step = 2 * math.pi/n
    prev = None
    points = []
    for i in range(n):
        angle = angle_step * i
        point = engine.Point2D(x + r * math.cos(angle), y + r*math.sin(angle), 1)
        points.append(point)
        world.add_point(point)
        world.add_joint(center, point, k)
        if prev:
            world.add_joint(prev, point, k)
        prev = point
    world.add_joint(prev, points[0], k)

# =============================================================================
# run
pygame.init()
gameDisplay = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

crashed = False
# Physic settings
point_mass = 1
joint_k = 1
# ==============================================================================
# ini section
# =============================================================================
import base.restrictions as restrct

world = engine.World(30, ground=restrct.function(ground), gravity=Vector2D(0,-9.8),)
create_circle(world, 0.9, 2, 10, r=0.5)


# =============================================================================
# contollers
# =============================


def zoom_in():
    global ZOOM, X, Y
    if ZOOM < MAX_ZOOM:
        tmp_zoom = ZOOM
        diff = ZOOM / 10 + 1
        ZOOM += diff
        X = SIZE[0] / 2 - (SIZE[0] / 2 - X) * ZOOM / tmp_zoom
        Y = SIZE[0] / 2 - (SIZE[1] / 2 - Y) * ZOOM / tmp_zoom


def zoom_out():
    global ZOOM, X, Y
    if ZOOM > 4:
        tmp_zoom = ZOOM
        diff = ZOOM / 10 + 1
        ZOOM -= diff
        X = SIZE[0] / 2 - (SIZE[0] / 2 - X) * ZOOM / tmp_zoom
        Y = SIZE[0] / 2 - (SIZE[1] / 2 - Y) * ZOOM / tmp_zoom



pressed = None  # None, 'point', 'field', 'joint'
selected_point = None  # clicked point
selected_joint = None  # clicked joint
joint_point = None
move = None
pause = False
last_click = time.time()
x, y = 0, 0  # coordinates of field touch
frame_num = 0

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
            if event.key == pygame.K_n:
                world.step(1.0)
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
                current_time = time.time()
                delay = current_time - last_click
                last_click = current_time
                if delay < 0.2:
                    pos = pygame.mouse.get_pos()
                    pressed = 'field'
                    x, y = trans_out(pos[0], pos[1])
                    world.add_point(engine.Point2D(x, y, point_mass))
                else:
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
        world.step(1/FPS)
    draw_world(world, gameDisplay)
    if selected_point:
        mark_point(gameDisplay, selected_point, RED)
    if joint_point:
        mark_point(gameDisplay, joint_point, YELLOW)
    pygame.display.update()
    clock.tick(FPS)
    pygame.image.save(gameDisplay, f'/Users/vitali/PycharmProjects/physics-engine/video/{frame_num:0{3}}.png')
    frame_num += 1
