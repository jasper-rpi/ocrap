"""OOP representations of hit objects (hit circles, sliders, spinners)."""

import pygame

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
    def __init__(self, position: tuple[int, int], time, combo_num):
        super().__init__(position, time, combo_num)
