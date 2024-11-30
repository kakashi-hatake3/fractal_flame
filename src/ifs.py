import math
import random

from src.pixel import Pixel
from src.transformation import Transformation


class IFS:
    """Класс реализации СИФ."""

    def __init__(self, width: int, height: int, symmetry: int = 1):
        self.width = width
        self.height = height
        self.symmetry = symmetry
        self.transformations: list[Transformation] = []

    def add_transformation(self, transformation: Transformation) -> None:
        """Добавление преобразования."""
        self.transformations.append(transformation)

    def generate_points(self, new_points: int) -> list[Pixel]:
        """Генерация точек."""
        points = []
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)

        for _ in range(new_points):
            transformation = random.choice(self.transformations)
            x, y = transformation.apply(x, y)

            for i in range(self.symmetry):
                angle = (2 * math.pi * i) / self.symmetry
                x_sym = x * math.cos(angle) - y * math.sin(angle)
                y_sym = x * math.sin(angle) + y * math.cos(angle)
                screen_x = int(self.width / 2 + x_sym * self.width / 4)
                screen_y = int(self.height / 2 - y_sym * self.height / 4)
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    points.append(Pixel(screen_x, screen_y, transformation.color))

        return points
