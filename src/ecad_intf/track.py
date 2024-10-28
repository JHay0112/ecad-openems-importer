"""
Provides a description for copper tracks on a PCB.

Author: J. L. Hay
"""


from src.ecad_intf.feature import Feature

    

class Track:
    """
    Describes a copper track of a PCB.
    """

    def __init__(self):

        self.segments: list[Feature] = []
        self.net: str = None 
        self.layer_id: str = None 


    def __hash__(self) -> int:
        
        return hash(self.net)
    
    
    def __repr__(self) -> str:
        return f"Track(segments = {self.segments}, net = {self.net}, layer_id = {self.layer_id})"
    

    def add_segment(self, segment: Feature):
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