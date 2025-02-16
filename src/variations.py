import math

from src.enums import FunctionNames


class Variations:
    """Класс математических функций."""

    @staticmethod
    def linear(x, y):
        return x, y

    @staticmethod
    def sinusoidal(x, y):
        return math.sin(x), math.sin(y)

    @staticmethod
    def spherical(x, y):
        r2 = x**2 + y**2
        return x / r2, y / r2 if r2 != 0 else (0, 0)

    @staticmethod
    def swirl(x, y):
        r2 = x**2 + y**2
        return (
            x * math.sin(r2) - y * math.cos(r2),
            x * math.cos(r2) + y * math.sin(r2),
        )

    @staticmethod
    def polar(x, y):
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        return theta / math.pi, r - 1

    @staticmethod
    def heart(x, y):
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        return r * math.sin(theta), -r * math.cos(theta)

    @staticmethod
    def disk(x, y):
        r = math.sqrt(x**2 + y**2)
        return math.sin(math.pi * r), math.cos(math.pi * r)

    @staticmethod
    def cosine(x, y):
        max_value = 100
        y = max(-max_value, min(y, max_value))
        return math.cos(math.pi * x) * math.cosh(y), -math.sin(math.pi * x) * math.sinh(
            y
        )

    @staticmethod
    def fan(x, y):
        t = math.pi * (x + y)
        return math.sin(t), math.cos(t)


class VariationList:
    """Список доступных функций."""

    values = [
        (FunctionNames.LINEAR, Variations.linear),
        (FunctionNames.SINUSOIDAL, Variations.sinusoidal),
        (FunctionNames.SPHERICAL, Variations.spherical),
        (FunctionNames.SWIRL, Variations.swirl),
        (FunctionNames.POLAR, Variations.polar),
        (FunctionNames.HEART, Variations.heart),
        (FunctionNames.DISK, Variations.disk),
        (FunctionNames.COSINE, Variations.cosine),
        (FunctionNames.FAN, Variations.fan),
    ]
