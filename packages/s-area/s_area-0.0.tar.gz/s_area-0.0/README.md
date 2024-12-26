# s_area

Библиотека Python для вычисления площадей геометрических фигур, включая:
- Круги
- Треугольники
- Параллелепипеды

## Установка
Установите через pip:
```bash
pip install s_area
```

## Использование
```python
from s_area.GeometryCircle import Circle
from s_area.GeometryTriangle import Triangle
from s_area.GeometryParallelepiped import Parallelepiped

circle = Circle(5)
print(circle.area())  # Вывод: 78.53981633974483

triangle = Triangle(6, 4)
print(triangle.area())  # Вывод: 12

parallelepiped = Parallelepiped(3, 4, 5)
print(parallelepiped.area())  # Вывод: 94
```

## Тестирование
Запустите тесты с помощью команды:
```bash
python -m unittest discover tests
```