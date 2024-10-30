"""
Circle described by a centre and radius.

Author: J. L. Hay
"""


import numpy as np

from src.shapes.shape import Shape



class Circle(Shape):


    # Number of edges to approximate the circle with
    NUMBER_EDGES = 100


    def __init__(self, centre: tuple[float, float], radius: float):

        self.centre_pos: tuple[float, float] = centre
        self.radius: float = radius

    
    def polygon(self) -> list[tuple[float, float]]:
        
        centre = np.array(self.centre_pos)
        rads = np.linspace(0, 2 * np.pi, self.NUMBER_EDGES)
        xs = self.radius * np.cos(rads) + centre[0]
        ys = self.radius * np.sin(rads) + centre[1]

        return [[x, y] for x, y in zip(xs, ys)]
    

    def centre(self) -> tuple[float, float]:

        return self.centre_pos