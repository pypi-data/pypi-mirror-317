import math


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        """Вычисляет площадь круга."""
        return math.pi * self.radius ** 2