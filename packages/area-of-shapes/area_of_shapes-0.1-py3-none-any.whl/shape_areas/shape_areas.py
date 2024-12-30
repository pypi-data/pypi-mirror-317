
class ShapeArea:
    def __init__(self) -> None:
        return
    
    def square(self, side: float) -> float:
        output = side * side
        return round(output, 2)
    
    def rectangle(self, length: float, width: float) -> float:
        output = length * width
        return round(output, 2)
    
    def circle(self, radius: float) -> float:
        output = 3.14159 * radius * radius
        return round(output, 2)
    
    def triangle(self, base: float, height: float) -> float:
        output = 0.5 * base * height
        return round(output, 2)
    
    def trapezoid(self, base1: float, base2: float, height: float) -> float:
        output = 0.5 * (base1 + base2) * height
        return round(output, 2)
    
    def parallelogram(self, base: float, height: float) -> float:
        output = base * height
        return round(output, 2)
    
    def rhombus(self, diagonal1: float, diagonal2: float) -> float:
        output = 0.5 * diagonal1 * diagonal2
        return round(output, 2)
