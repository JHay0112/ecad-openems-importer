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
    

    def centre(self) -> tuple[float, float]:

        sum_x = 0
        sum_y = 0

        for point in self.points:
            sum_x += point[0]
            sum_y += point[1]

        n = len(self.points)
        return (sum_x/n, sum_y/n)
