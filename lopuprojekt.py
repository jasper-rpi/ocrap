import pygame
import os
import time

import beatmaps
from assets import *
from HitObjects import HitCircle, Slider

pygame.init()
pygame.mixer.music.load("song.mp3")

# Initialize font for health display
pygame.font.init()
health_font = pygame.font.SysFont('Arial', 36)  # You can change the font and size as needed

pygame.mouse.set_visible(False)
pygame.display.set_caption('ocrap!')

cursor = pygame.image.load(os.path.join('assets', 'cursor.png'))
cursor_rect = cursor.get_rect()

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

# https://osu.ppy.sh/wiki/en/Client/Playfield
playfield_x = 512
playfield_y = 384
res_multiplier = 4
# Scale playfield with resolution
while playfield_x <= resolution[0] and playfield_y <= resolution[1]:
    playfield_x += 512
    playfield_y += 384
    res_multiplier += 1

playfield_x -= 512
playfield_y -= 384
res_multiplier -= 1

playfield_x_offset = (resolution[0] - playfield_x) // 2
playfield_y_offset = (resolution[1] - playfield_y) // 2

beatmap = beatmaps.parse_beatmap("beatmap.osu")
slider_multiplier = float(beatmap["SliderMultiplier"])

approach_rate = float(beatmap["ApproachRate"])
# time to start fading in at: https://osu.ppy.sh/wiki/en/Beatmap/Approach_rate
if approach_rate < 5:
    preempt = 1200 + 600 * (5 - approach_rate) / 5
elif approach_rate == 5:
    preempt = 1200
else:
    preempt = 1200 - 750 * (approach_rate - 5) / 5
print(f"Preempt: {preempt}")

circle_size_multiplier = float(beatmap["CircleSize"])
# https://osu.ppy.sh/wiki/en/Beatmap/Circle_size
r = 54.4 - 4.48 * circle_size_multiplier
r *= res_multiplier / 4

# Convert hit objects into OOP representations
hit_objects = []
combo_num = 1
# Current slider beat length in ms
beat_length = 0
for i in beatmap["hitObjects"]:
    if i["newCombo"]:
        combo_num = 1
    else:
        combo_num += 1
    if i["object_name"] == "circle":
        x = i["position"][0] + playfield_x_offset
        y = i["position"][1] + playfield_y_offset
        hit_objects.append(HitCircle((x, y), i["startTime"], combo_num, r))
    elif i["object_name"] == "slider":
        if i["beatLength"] > 0:
            beat_length = i["beatLength"]
            velocity = 1
        else:
            velocity = abs(i["beatLength"])
        points = []
        for point in i["points"]:
            x = point[0] + playfield_x_offset
            y = point[1] + playfield_y_offset
            points.append((x, y))
        hit_objects.append(Slider(i["startTime"], combo_num, points, i["curveType"], i["pixelLength"], r, beat_length,
                                  velocity, i["repeatCount"]))

health = 100

running = True
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(1)
objects_to_cull = 0
# Stores circles that need to be drawn with position
loaded_objects = []
start_time = time.monotonic()
while running:
    timer = (time.monotonic() - start_time) * 1000
    # Get hit objects from beatmap, check if timing is correct
    for i in hit_objects:
        if (i.time - timer) <= preempt:
            loaded_objects.append(i)
            objects_to_cull += 1
        else:
            break
    del hit_objects[0:objects_to_cull]
    objects_to_cull = 0

    screen.fill((0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Render and display health
    health_text = health_font.render(f'{health * "l"}', True, (255, 255, 255))
    screen.blit(health_text, (20, 20))  # Position in top left corner with 20px padding

    missed = 0
    for i in loaded_objects:
        progress = 1 - (i.time - timer) / preempt
        i.draw(screen, progress)

    # Miss/slider checking
    if loaded_objects:
        first = loaded_objects[0]
        if type(first) == HitCircle:
            if (first.time - timer) < -200:
                print("missed")
                missed += 1
                del loaded_objects[0]
        elif type(first) == Slider:
            if first.state == "unpressed" and (first.time - timer) < -200:
                print("missed")
                missed += 1
                del loaded_objects[0]
            else:
                duration = first.length / (slider_multiplier * 100 * first.velocity) * first.beatlength
                move_progress = (timer - first.time) / duration
                if move_progress > 1:
                    del loaded_objects[0]

    screen.blit(cursor, (mouse_x - cursor_rect.width // 2, mouse_y - cursor_rect.height // 2))
    hit_radius = r + 13 * (res_multiplier / 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Mouse: {mouse_x}, {mouse_y}")
            # Process first object
            x = loaded_objects[0].x
            y = loaded_objects[0].y
            distance = ((mouse_x - x) ** 2 + (mouse_y - y) ** 2) ** 0.5
            if type(first) == HitCircle:
                if distance <= 60 + 10:
                    print('clicked\n')
                    print(isinstance(first, HitCircle))
                    del loaded_objects[0]
            elif type(first) == Slider:
                if loaded_objects[0].state == "unpressed":
                    if distance <= 60 + 10:
                        print('clicked\n')
                        first.state = "forwards"


    if health <= 0:
        print("You're dead!")
        running = False


    clock.tick(ticks)
    pygame.display.flip()
