import pygame
import robot
import sys
import math
import numpy as np

# End condition
game_loop = True

# Setting up screen
SIZE_X, SIZE_Y = 1000, 500
pygame.init()
screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
my_font1 = pygame.font.SysFont("monospace", 30)

robot = robot.Robot(25, 100)
robot.center_coord['x'] = float(SIZE_X / 8)
robot.center_coord['y'] = float(SIZE_Y / 2)
robot.phi = - np.pi / 2

clock = pygame.time.get_ticks()
prev_clock = clock

# Game Loop
while game_loop:
    clock = pygame.time.get_ticks()
    screen.fill('white')

    clock = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        key_input = pygame.key.get_pressed()

        # pouzivaju sa rovnake vypocty ako pre matplotlib a kedze matplotlib ma kladne y smerom hore a pygame ma kladne
        # y smerom dole, je tu v pygame hre potrebne uvazovat presne opacne, tj dolava je doprava a doprava je dolava
        if key_input[pygame.K_UP]:
            robot.vl = 0.1
            robot.vr = 0.1
        elif key_input[pygame.K_LEFT]:
            robot.vl = -0.1
            robot.vr = 0.1
        elif key_input[pygame.K_RIGHT]:
            robot.vl = 0.1
            robot.vr = -0.1
        elif key_input[pygame.K_DOWN]:
            robot.vl = -0.1
            robot.vr = -0.1
        else:
            robot.vl = 0
            robot.vr = 0

    elaps = clock - prev_clock
    robot.run(elaps)

    x = robot.center_coord['x']
    y = robot.center_coord['y']
    length = 30

    # find the end point
    endy = y + length * math.cos((np.pi/2) - robot.phi)
    endx = x + length * math.sin((np.pi/2) - robot.phi)

    # Draw left wheel
    pygame.draw.circle(screen, 'black', (robot.left_wheel_cord['x'], robot.left_wheel_cord['y']), 10)
    # Draw right wheel
    pygame.draw.circle(screen, 'black', (robot.right_wheel_cord['x'], robot.right_wheel_cord['y']), 10)
    # Draw line between left and right wheel
    pygame.draw.line(screen, 'black', (robot.left_wheel_cord['x'], robot.left_wheel_cord['y']),
                     (robot.right_wheel_cord['x'], robot.right_wheel_cord['y']), 4)
    # Draw directional vector
    pygame.draw.line(screen, 'black', (x, y), (endx, endy))

    # Draw points of center and wheel
    pygame.draw.circle(screen, 'red', (robot.center_coord['x'], robot.center_coord['y']), 4)

    prev_clock = clock

    x_l = [cord[0] for cord in robot.trajectory_left_wheel]
    y_l = [cord[1] for cord in robot.trajectory_left_wheel]

    x_r = [cord[0] for cord in robot.trajectory_right_wheel]
    y_r = [cord[1] for cord in robot.trajectory_right_wheel]

    for lx, ly, rx, ry in zip(x_l, y_l, x_r, y_r):
        pygame.draw.circle(screen, 'blue', (lx, ly), 1)
        pygame.draw.circle(screen, 'blue', (rx, ry), 1)

    pygame.display.update()