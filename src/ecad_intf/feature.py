"""
Description of any simple copper feature on a board.

Author: J. L. Hay
"""


from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape



class Feature:

    def __init__(
            self, 
            name: str = None, 
            shape: Shape | CompoundShape = None,
            net: str = None,
            layer_id: str = None
        ):


        self.name: str = None
        self.shape: Shape | CompoundShape = None
        self.net: str = None
        self.layer_id: str = None