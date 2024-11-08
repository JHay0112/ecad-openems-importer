"""
Provides a description for a PCB layer.

Author: J. L. Hay
"""


class Layer:
    """
    Describes a layer of a PCB.
    """
    
    def __init__(self):
        
        self.id: str = None
        self.name: str = None
        self.depth: float = None
        self.polygon: list[tuple[float, float]] = None


    def __repr__(self):

        return f"Layer(id = {self.id}, name = \"{self.name}\", depth = {self.depth})"