class Triangle:
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        """Вычисляет площадь треугольника."""
        return 0.5 * self.base * self.height