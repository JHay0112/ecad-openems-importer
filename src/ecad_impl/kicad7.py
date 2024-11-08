"""
Specific implementation of the board interface for KiCAD 7.

Author: J. L. Hay
"""


import pcbnew
import ctypes

from src.ecad_intf.board import Board
from src.ecad_intf.layer import Layer
from src.ecad_intf.pad import Pad
from src.ecad_intf.via import Via

from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape
from src.shapes.rectangle import Rectangle
from src.shapes.circle import Circle
from src.shapes.polygon import Polygon



class KiCAD7Board(Board):


    def __init__(self):

        self.board: pcbnew.BOARD = None


    @classmethod
    def __to_mm(_, x: float) -> float:
        """Private method for converting KiCAD values to mm."""
        return x / 1_000_000
    

    @classmethod
    def __convert_shape(cls, kicad_shape) -> Shape | CompoundShape:
        """Private method for convering KiCAD shapes into valid shapes."""


        # Deal with shapes that haven't been cast yet
        if isinstance(kicad_shape, pcbnew.SHAPE):
            kicad_shape = kicad_shape.Cast()
        

        if isinstance(kicad_shape, pcbnew.SHAPE_COMPOUND):

            shapes: list[Shape] = []

            for sub_shape in kicad_shape.GetSubshapes():

                shape = cls.__convert_shape(sub_shape)
                if shape is not None:
                    shapes.append(shape)

            if len(shapes) == 1:
                # Trivial shape!
                return shapes[0]

            compound_shape = CompoundShape(shapes)

            return compound_shape
        

        if isinstance(kicad_shape, pcbnew.SHAPE_RECT):

            pos = kicad_shape.GetPosition()
            width = kicad_shape.GetWidth()
            height = kicad_shape.GetHeight()

            pos = [cls.__to_mm(val) for val in pos]
            width = cls.__to_mm(width)
            height = cls.__to_mm(height)

            start = [pos[0], pos[1]]
            end = [pos[0] + width, pos[1] + height]
            shape = Rectangle(start, end)

            return shape
        

        if isinstance(kicad_shape, pcbnew.SHAPE_CIRCLE):

            centre = kicad_shape.GetCenter()
            radius = kicad_shape.GetRadius()

            centre = [cls.__to_mm(val) for val in centre]
            radius = cls.__to_mm(radius)

            shape = Circle(centre, radius)
            return shape
        
        
        if isinstance(kicad_shape, pcbnew.SHAPE_SIMPLE):
            # Polygon!
            points = []
            
            for i in range(kicad_shape.GetPointCount()):
                point = kicad_shape.GetPoint(i)
                point = [cls.__to_mm(val) for val in point]
                points.append(point)

            return Polygon(points)
        

        if isinstance(kicad_shape, pcbnew.SHAPE_ARC):

            return None
        
        if isinstance(kicad_shape, pcbnew.SHAPE_SEGMENT):

            return None
        
        raise ValueError(f"Shape of type \"{type(kicad_shape)}\" passed to __convert_shape is not handled.")
    

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

            polyset = pcbnew.SHAPE_POLY_SET()
            self.board.ConvertBrdLayerToPolygonalContours(id, polyset)
            copper_layers[i].polygons = []

            for j in range(polyset.OutlineCount()):
                
                outline = polyset.Outline(j)
                points = []

                for k in range(outline.PointCount()):

                    point = outline.CPoint(k)
                    x = self.__to_mm(point.x)
                    y = self.__to_mm(point.y)

                    points.append((x, y))
                
                copper_layers[i].polygons.append(points)

        return copper_layers


    def get_pads(self) -> list[Pad]:

        kicad_pads = self.board.GetPads()
        pads = [Pad() for _ in kicad_pads]

        for i, pad in enumerate(kicad_pads):

            pads[i].name = pad.GetPadName()
            pads[i].shape = self.__convert_shape(pad.GetEffectiveShape())
            pads[i].net = pad.GetNetname()
            pads[i].layer_id = pad.GetPrincipalLayer()

        return pads


    def get_vias(self) -> list[Via]:

        kicad_vias = self.board.GetVias()

