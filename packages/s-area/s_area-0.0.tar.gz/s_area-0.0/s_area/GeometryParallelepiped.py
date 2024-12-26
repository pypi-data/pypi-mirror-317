class Parallelepiped:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def area(self):
        """Вычисляет площадь поверхности параллелепипеда."""
        return 2 * (self.length * self.width + self.width * self.height + self.height * self.length)