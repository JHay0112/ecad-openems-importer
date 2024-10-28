"""
Specific implementation of the board interface for KiCAD 7.

Author: J. L. Hay
"""


import pcbnew
import ctypes

from src.ecad_intf.board import Board
from src.ecad_intf.layer import Layer
from src.ecad_intf.zone import Zone
from src.ecad_intf.track import Track, Segment
from src.ecad_intf.via import Via



class KiCAD7Board(Board):


    def __init__(self):

        self.board: pcbnew.BOARD = None


    @classmethod
    def __to_mm(_, x: float) -> float:
        """Private method for converting KiCAD values to mm."""
        return x / 1_000_000
    

    @classmethod
    def __get_string_from_ptr(_, s) -> str:
        """Private method for converting strings."""
        s_ptr = ctypes.cast(int(s), ctypes.c_char_p)
        return s_ptr.value.decode("UTF-8")


    @classmethod
    def get_filename_extension(_) -> str:
        return "kicad_pcb"
    

    @classmethod
    def load_from_file(_, filename: str) -> Board:

        if not KiCAD7Board.is_valid_file(filename):
            raise ValueError(f"File named \"{filename}\" is not a valid file.")

        board = KiCAD7Board()
        board.board = pcbnew.LoadBoard(filename)
        return board   
    

    def get_thickness(self) -> float:

        kicad_design_settings = self.board.GetDesignSettings()
        kicad_thickness = kicad_design_settings.GetBoardThickness()
        return self.__to_mm(kicad_thickness)
    

    def get_bounding_box(self) -> list[tuple[float, float, float]]:

        kicad_design_settings = self.board.GetDesignSettings()
        kicad_thickness = kicad_design_settings.GetBoardThickness()
        kicad_bbox = self.board.GetBoundingBox()
        kicad_start = kicad_bbox.GetOrigin()
        kicad_end = kicad_bbox.GetEnd()

        start = [kicad_start[0], kicad_start[1], 0]
        end = [kicad_end[0], kicad_end[1], kicad_thickness]

        # Conversion from nm to mm
        start = [self.__to_mm(val) for val in start]
        end = [self.__to_mm(val) for val in end]

        return [start, end]
    

    def get_layers(self) -> list[Layer]:

        kicad_layers = self.board.GetEnabledLayers()
        board_thickness = self.get_thickness()

        copper_layer_ids = kicad_layers.CuStack()
        copper_layers = [Layer() for _ in range(len(copper_layer_ids))]

        for i, id in enumerate(copper_layer_ids):

            copper_layers[i].id = id

            copper_layers[i].name = self.__get_string_from_ptr(kicad_layers.Name(id))

            layer_depth = self.board.LayerDepth(copper_layer_ids[0], id)
            copper_layers[i].depth = board_thickness * layer_depth

        return copper_layers
    

    def get_zones(self) -> list[Zone]:

        ...


    def get_tracks(self) -> list[Track]:

        kicad_tracks = self.board.GetTracks()
        track_map: dict[tuple[str, str], Track] = {}

        for track in kicad_tracks:

            track_net = track.GetNetname()
            track_layer = track.GetLayer()
            track_start = track.GetStart()
            track_end = track.GetEnd()
            track_width = track.GetWidth()

            track_id = (track_net, track_layer)

            if track_id not in track_map.keys():
                track_map[track_id] = Track()

            track_segment = Segment()
            track_segment.start = tuple(self.__to_mm(val) for val in track_start)
            track_segment.end = tuple(self.__to_mm(val) for val in track_end)
            track_segment.net = track_net
            track_segment.layer_id = track_layer
            track_segment.width = self.__to_mm(track_width)

            track_map[track_id].add_segment(track_segment)

        return list(track_map.values())


    def get_vias(self) -> list[Via]:

        kicad_vias = self.board.GetVias()

