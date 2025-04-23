import pygame
from assets import *
import os

pygame.init()

pygame.mouse.set_visible(False)
cursor = pygame.image.load(os.path.join('assets', 'cursor.png'))
cursor_rect = cursor.get_rect()

clock = pygame.time.Clock()

resolutions = {1:(1280, 720), 2:(1920, 1080), 3:(2560, 1440)}
resolution_choice = int(input("Choose your resolution:\n1. 1280 x 720\n2. 1920 x 1080\n3. 2560 x 1440\n"))
if resolution_choice not in resolutions.keys():
    exit()
resolution = resolutions[resolution_choice]

#tickrates = (30, 60, 120, 144, 240)
#tick_choice = int(input("Choose your tickrate:\n1. 30\n2. 60\n3. 120\n4. 144\n5. 240\n"))
#if tick_choice not in tickrates:
#    exit()
#ticks = int(tickrates[tick_choice])

screen = pygame.display.set_mode((resolution[0], resolution[1]))

running = True
while running:
    screen.fill((0, 0, 0))
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor, cursor_rect.center)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

    clock.tick(60)
    pygame.display.flip()
