"""OOP representations of hit objects (hit circles, sliders, spinners)."""

import pygame
import os
from itertools import chain

class HitCircle:
    def __init__(self, position: tuple[int, int], time, combo_num, radius):
        self.position = position
        self.time = time
        self.x = self.position[0]
        self.y = self.position[1]
        self.combo_num = combo_num
        self.radius = radius

    def draw(self, screen: pygame.surface, progress):
        """
        Draw hit circle on screen.

        Progress is a float that determines the radius of the approach circle (0: fully outside, 1: flush with circle)"""
        size = int(self.radius * 2)
        hitcircle = pygame.image.load(os.path.join('assets', 'circle_pls-work.png'))
        hitcircle = pygame.transform.scale(hitcircle, (size, size))
        screen.blit(hitcircle,
                    (self.position[0] - hitcircle.get_width() / 2, self.position[1] - hitcircle.get_height() / 2))
        # Draw approach circle
        approach_radius = size * 2 - (progress * size)
        if round(approach_radius) == size:
            print("flush")
        pygame.draw.circle(screen, (255, 255, 255), self.position, approach_radius, width=3)


class Slider(HitCircle):
    def __init__(self, time, combo_num, points: list[tuple[int, int]], curve_type: str, length: int, radius, duration):
        self.radius = radius
        super().__init__(points[0], time, combo_num, radius)
        self.points = points
        self.curve_type = curve_type
        self.length = length
        self.duration = duration
        # Track state of movement
        self.state = "unpressed"

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

        # Calculate position on slider for each point
        # Tuples in format ((x, y), progress) where progress is from 0 to 1
        self.slider_points = []
        progress = 0
        length_passed = 0
        combined_points = tuple(enumerate(chain.from_iterable(self.curve_points)))
        for index, point in combined_points:
            if index == len(combined_points) - 1:
                self.slider_points.append((point, 1))
            else:
                x_squared = (point[0] - combined_points[index + 1][1][0]) ** 2
                y_squared = (point[1] - combined_points[index + 1][1][1]) ** 2
                distance = (x_squared - y_squared) ** 0.5
                progress += distance
                slider_progress = progress / self.length
                self.slider_points.append((point, slider_progress))

    def draw(self, screen: pygame.surface, hit_progress, move_progress=0):
        for curve in self.curve_points:
            pygame.draw.lines(screen, (255, 255, 255), False, curve, width=20)
        size = int(self.radius * 2)
        if self.state == "unpressed":
            # Draw start point
            super().draw(screen, hit_progress)
        else:
            point = find_curve_point_by_length(self.slider_points, move_progress)
            pygame.draw.circle(screen, (255, 192, 253), point, size)

        # Draw end point
        hitcircle = pygame.image.load(os.path.join('assets', 'circle_pls-work.png'))
        hitcircle = pygame.transform.scale(hitcircle, (size, size))
        x = self.curve_points[-1][-1][0]
        y = self.curve_points[-1][-1][1]
        screen.blit(hitcircle,
                    (x - hitcircle.get_height() / 2, y - hitcircle.get_width() / 2))


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


def find_curve_point_by_length(points, t: float):
    """
    Find point on compound curve corresponding to ratio t.

    :param points: list of curve points with lengths included
    :param t: ratio from 0 to 1
    :return: tuple with x and y values of needed point
    """
    for index, i in enumerate(points):
        if i[1] > t:
            first_point = points[index - 1][0]
            second_point = i[0]
            t_inbetween = pygame.math.lerp(first_point[1], second_point[1], t)
            x = pygame.math.lerp(first_point[0], second_point[0], t_inbetween)
            y = pygame.math.lerp(first_point[1], second_point[1], t_inbetween)
            return x, y