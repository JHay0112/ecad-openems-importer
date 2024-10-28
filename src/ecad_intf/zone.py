"""
Provides a description for copper zones on a PCB.

Author: J. L. Hay
"""



class Zone:
    """
    Describes a copper zone of a PCB.
    """
    
    def __init__(self):
        
        self.points: list[tuple[float, float]] = None
        self.net: str = None
        self.layer_id: str = None

    def __repr__(self):

        return f"Zone(points = {self.points}, net = {self.net}, layer_id = {self.layer_id})"