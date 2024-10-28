from src.ecad_impl.kicad7 import KiCAD7Board
from src.ecad_intf.board import Board

from CSXCAD import ContinuousStructure
from openEMS.physical_constants import *
from math import pi

import numpy as np


INPUT_BOARD = "ti_ant.kicad_pcb"

SUBSTR_EPS_R = 3.38
SUBSTR_KAPPA = 1e-3 * 2 * pi * 2.45e9 * EPS0 * SUBSTR_EPS_R



board: Board = KiCAD7Board.load_from_file(INPUT_BOARD)


bbox = board.get_bounding_box()
tracks = board.get_tracks()
layers = board.get_layers()
layer_map = {layer.id: layer for layer in layers}


csx = ContinuousStructure()

substrate = csx.AddMaterial("board", epsilon = SUBSTR_EPS_R, kappa = SUBSTR_KAPPA)
substrate.AddBox(*bbox)


for track in tracks:

    copper = csx.AddMetal(track.net)
    
    for segment in track.segments:

        layer = layer_map[segment.layer_id]

        start = np.array(segment.start)
        end = np.array(segment.end)

        if np.array_equal(start, end):
            continue

        diff = end - start
        dir = diff / np.linalg.norm(diff)
        perp = np.array([-dir[1], dir[0]]) * segment.width/2

        start = np.array([segment.start[0], segment.start[1]])
        end = np.array([segment.end[0], segment.end[1]])

        points = np.array([start + perp, start - perp, end - perp, end + perp]).T

        copper.AddPolygon(points, "z", layer.depth)



csx.Write2XML("test.xml")