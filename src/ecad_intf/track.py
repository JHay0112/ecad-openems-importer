"""
Provides a description for copper tracks on a PCB.

Author: J. L. Hay
"""



class Segment:
    """
    Describes a copper track segment of a PCB.
    """
    
    def __init__(self):
        
        self.start: tuple[float, float] = None
        self.end: tuple[float, float] = None
        self.width: float = None
        self.net: str = None
        self.layer_id: str = None

    def __repr__(self):

        return f"Segment(start = {self.start}, end = {self.end}, width = {self.width}, net = {self.net}, layer_id = {self.layer_id})"
    

class Track:
    """
    Describes a copper track of a PCB.
    """

    def __init__(self):

        self.segments: list[Segment] = []
        self.net: str = None 
        self.layer_id: str = None 


    def __hash__(self) -> int:
        
        return hash(self.net)
    
    
    def __repr__(self) -> str:
        return f"Track(segments = {self.segments}, net = {self.net}, layer_id = {self.layer_id})"
    

    def add_segment(self, segment: Segment):
        """
        Adds a segment to the track.

        Parameters
        ----------

        segment: Segment
            The segment to add to the track.
        """
        if self.net is None:
            self.net = segment.net 
        if self.layer_id is None:
            self.layer_id = segment.layer_id

        assert self.net == segment.net, "Segment net does not match track net."
        assert self.layer_id == segment.layer_id, "Segment layer does not match tack layer."

        self.segments.append(segment)