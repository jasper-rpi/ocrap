import os
import pygame
import zipfile

for file in [f for f in os.listdir() if os.path.isfile(os.path.join(".", f))]:
    if file.endswith(".osz"):
        beatmap = zipfile.ZipFile(file)
        beatmap.extractall()