"""Functions to parse beatmaps."""

import sys

sys.path.append("python_osu_parser")
import python_osu_parser as parse

def parse_beatmap(filename: str):
    parser = parse.beatmapparser.BeatmapParser()
    parser.parseFile(filename)
    parser.build_beatmap()
    return parser.beatmap