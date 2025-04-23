import pygame
from assets import *
import os

pygame.init()

pygame.mouse.set_visible(False)
pygame.display.set_caption('ocrap!')

button_pos = 600, 600

clock = pygame.time.Clock()

resolutions = {1:(1280, 720), 2:(1920, 1080), 3:(2560, 1440)}
resolution_choice = int(input("Choose your resolution:\n1. 1280 x 720\n2. 1920 x 1080\n3. 2560 x 1440\n"))
if resolution_choice not in resolutions.keys():
    exit()
resolution = resolutions[resolution_choice]

tickrates = {1: 30, 2: 60, 3: 120, 4: 144, 5: 240}
tick_choice = int(input("Choose your tickrate:\n1. 30\n2. 60\n3. 120\n4. 144\n5. 240\n"))
if tick_choice not in tickrates.keys():
    exit()
ticks = int(tickrates[tick_choice])

screen = pygame.display.set_mode(resolution)

running = True
while running:
    screen.fill((0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button = pygame.draw.circle(screen, (255, 255, 255), button_pos, 60)
    cursor = pygame.draw.circle(screen, (255, 255, 51), (mouse_x, mouse_y), 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance = ((mouse_x - button_pos[0]) ** 2 + (mouse_y - button_pos[1]) ** 2) ** 0.5

            if distance <= 60 + 10:
                print('clicked\n')

    clock.tick(ticks)
    pygame.display.flip()
