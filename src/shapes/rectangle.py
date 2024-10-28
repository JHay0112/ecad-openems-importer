"""
Rectangle described by two points in opposing corners.

Author: J. L. Hay
"""


from src.shapes.shape import Shape



class Rectangle(Shape):


    def __init__(self, start: tuple[float, float], end: tuple[float, float]):

        self.start: tuple[float, float] = start
        self.end: tuple[float, float] = end 

    
    def polygon(self) -> list[tuple[float, float]]:
        
        points = [
            [self.start[0], self.start[1]],
            [self.start[0], self.end[1]],
            [self.end[0], self.end[1]],
            [self.end[0], self.start[1]]
        ]

        return points