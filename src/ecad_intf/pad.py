"""
Provides a description for a pad on a PCB.

Author: J. L. Hay
"""


class Pad:
    """
    Describes a pad of a PCB.
    """
    
    def __init__(self):
        
        self.id: str = None
        self.name: str = None
        self.layer_id: str = None
        self.position: tuple[float, float] = None