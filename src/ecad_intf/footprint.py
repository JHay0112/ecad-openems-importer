"""
Provides a description for footprints on a PCB.

Author: J. L. Hay
"""


from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape



class Footprint:
    """
    Describes a copper footprint on a PCB.
    """
    
    def __init__(self):
        
        self.shape: Shape | CompoundShape = None
        self.reference: str = None
        self.layer_id: str = None
        self.pads 