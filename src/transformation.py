from dataclasses import dataclass


@dataclass
class Transformation:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    variation: callable
    color: tuple[int, int, int]

    def apply(self, x, y):
        x_new = self.a * x + self.b * y + self.c
        y_new = self.d * x + self.e * y + self.f
        return self.variation(x_new, y_new)
