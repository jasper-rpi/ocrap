"""OOP representations of hit objects (hit circles, sliders, spinners)."""

import pygame
from python_osu_parser.curve import Bezier

class HitCircle:
    def __init__(self, position: tuple[int, int], time, combo_num):
        self.position = position
        self.time = time
        self.x = self.position[0]
        self.y = self.position[1]
        self.combo_num = combo_num

    def draw(self, screen: pygame.surface, size, progress):
        """
        Draw hit circle on screen.

        Progress is a float that determines the radius of the approach circle (0: fully outside, 1: flush with circle)"""
        pygame.draw.circle(screen, (255, 255, 255), self.position, size)
        # Draw approach circle
        approach_radius = size * 2 - (progress * size)
        pygame.draw.circle(screen, (255, 255, 255), self.position, approach_radius, width=3)


class Slider(HitCircle):
    def __init__(self, time, combo_num, points: list[tuple[int, int]], curve_type: str):
        super().__init__(points[0], time, combo_num)
        self.points = points
        self.curve_type = curve_type

        self.curves = []
        # Split up compound curves
        index = 0
        previous = None
        for i in self.points:
            if not previous:
                self.curves.append([i])
                previous = i
            elif previous == i:
                index += 1
                self.curves.append([i])
            else:
                self.curves[index].append(i)
                previous = i

        # Calculate points for bezier curve
        step = 0.01
        # List of lists, every list contains points corresponding to curve in curves
        self.curve_points = []
        index = 0
        for curve in self.curves:
            t = 0
            while t < 1:
                point = get_curve_point(curve, t)
                try:
                    self.curve_points[index].append(point)
                except IndexError:
                    self.curve_points.append([point])
                t += step
            index += 1

    def draw(self, screen: pygame.surface, size, progress):
        for curve in self.curve_points:
            pygame.draw.lines(screen, (255, 255, 255), False, curve)


def get_curve_point(points, t: float):
    """
    Find Bezier curve point at ratio t using De Casteljau's algorithm
    https://pomax.github.io/bezierinfo/#decasteljau
    :param points: list of control points
    :param t: ratio from 0 to 1
    :return: tuple with x and y values of the curve point at ratio t
    """
    # We recurse until there's only one point provided in the list
    if len(points) == 1:
        return points[0]
    new_points = [None] * (len(points) - 1)
    for i in range(len(new_points)):
        x = (1 - t) * points[i][0] + t * points[i + 1][0]
        y = (1 - t) * points[i][1] + t * points[i + 1][1]
        new_points[i] = (x, y)
    return get_curve_point(new_points, t)