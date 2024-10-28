"""
Provides a description for pads on a PCB.

Author: J. L. Hay
"""


from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape



class Pad:
    """
    Describes a copper pad on a PCB.
    """
    
    def __init__(self):
        
        self.shape: Shape | CompoundShape = None
        self.net: str = None
        self.layer_id: str = None