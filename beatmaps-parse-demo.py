import os
import pygame
import sys
import zipfile

sys.path.append("python_osu_parser")
import python_osu_parser as parse

for file in [f for f in os.listdir() if os.path.isfile(os.path.join(".", f))]:
    if file.endswith(".osz"):
        beatmap = zipfile.ZipFile(file)
        beatmap.extractall(path=f"beatmaps/{file.strip(".osz")}")

for root, dirs, files in os.walk("beatmaps"):
    for file in files:
        if file.endswith(".osu"):
            parser = parse.beatmapparser.BeatmapParser()
            parser.parseFile(os.path.join(root, file))
            parser.build_beatmap()
            print(parser.beatmap)