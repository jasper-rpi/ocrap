import pygame
from assets import *
import os

import beatmaps

beatmap = beatmaps.parse_beatmap("beatmap.osu")

pygame.init()
pygame.mixer.music.load("song.mp3")

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
pygame.mixer.music.play(1)
timer = 0
objects_to_cull = 0
# Stores circles that need to be drawn with position
loaded_objects = []
while running:
    timer += 1000 / ticks
    # Get hit objects from beatmap, check if timing is correct
    print(beatmap["hitObjects"])
    for i in beatmap["hitObjects"]:
        if i["startTime"] <= timer:
            objects_to_cull += 1
            # Ignoring everything except circles for now
            if i["object_name"] == "circle":
                loaded_objects.append(tuple(i["position"]))
                print(loaded_objects)
        else:
            break
    del beatmap["hitObjects"][0:objects_to_cull]
    objects_to_cull = 0

    screen.fill((0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor = pygame.draw.circle(screen, (255, 255, 51), (mouse_x, mouse_y), 3)

    for i in loaded_objects:
        pygame.draw.circle(screen, (255, 255, 255), i, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in loaded_objects:
                distance = ((mouse_x - i[0]) ** 2 + (mouse_y - i[1]) ** 2) ** 0.5
                if distance <= 60 + 10:
                    print('clicked\n')
                    loaded_objects.remove(i)


    clock.tick(ticks)
    pygame.display.flip()
