"""
Shape made of shapes!

Author: J. L. Hay
"""


from src.shapes.shape import Shape



class CompoundShape:


    def __init__(self, shapes: list[Shape]):

        self.shapes: list[Shape] = shapes


    def __iter__(self):

        for shape in self.shapes:
            yield shape