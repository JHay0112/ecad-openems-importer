"""
Abstract base class for shapes.

Author: J. L. Hay
"""


from abc import ABC, abstractmethod



class Shape(ABC):


    @abstractmethod
    def polygon(self) -> list[tuple[float, float]]:
        """
        Returns a list of points describing a polygon of the shape.

        Returns
        -------

        list[tuple[float, float]]
        """
        ...