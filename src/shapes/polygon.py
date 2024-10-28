"""
A shape defined by a series of points.

Author: J. L. Hay
"""


from src.shapes.shape import Shape 



class Polygon(Shape):


    def __init__(self, points: list[tuple[float, float]]):

        self.points: list[tuple[float, float]] = points 


    def polygon(self) -> list[tuple[float, float]]:
        # Now that's easy isn't it
        return self.points