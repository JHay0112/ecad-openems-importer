"""
Provides a description for a PCB via.

Author: J. L. Hay
"""


class Via:
    """
    Describes a via of a PCB.
    """

    def __init__(self):

        self.position: tuple[float, float] = None
        self.net: str = None 
        self.inner_diameter: float = None
        self.outer_diameter: float = None
