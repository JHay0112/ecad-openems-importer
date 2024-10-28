from src.ecad_impl.kicad7 import KiCAD7Board
from src.ecad_intf.board import Board
from src.shapes.circle import Circle
from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape

from CSXCAD import ContinuousStructure
from openEMS.physical_constants import *
from math import pi

import numpy as np


INPUT_BOARD = "ti_ant.kicad_pcb"

SUBSTR_EPS_R = 3.38
SUBSTR_KAPPA = 1e-3 * 2 * pi * 2.45e9 * EPS0 * SUBSTR_EPS_R



def polygon_circle(centre: tuple[float, float], radius: float, edges: int) -> list[tuple[float, float]]:
    """Produces a polygon approximation of a circle."""
    centre = np.array(centre)
    rads = np.linspace(0, 2 * pi, edges)
    xs = radius * np.cos(rads) + centre[0]
    ys = radius * np.sin(rads) + centre[1]

    return [[x, y] for x, y in zip(xs, ys)]


board: Board = KiCAD7Board.load_from_file(INPUT_BOARD)



bbox = board.get_bounding_box()
layers = board.get_layers()
footprints = board.get_footprints()
pads = board.get_pads()
tracks = board.get_tracks()


csx = ContinuousStructure()


layer_map = {layer.id: layer for layer in layers}

nets = set(feature.net for feature in tracks + pads)
net_map = {net: csx.AddMetal(net) for net in nets}


substrate = csx.AddMaterial("board", epsilon = SUBSTR_EPS_R, kappa = SUBSTR_KAPPA)
substrate.AddBox(*bbox)


for track in tracks:

    copper = net_map[track.net]
    
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

        start_circle = Circle(start, segment.width/2).polygon()
        copper.AddPolygon(np.array(start_circle).T, "z", layer.depth)
        end_circle = Circle(end, segment.width/2).polygon()
        copper.AddPolygon(np.array(end_circle).T, "z", layer.depth)

        points = np.array([start + perp, start - perp, end - perp, end + perp]).T

        copper.AddPolygon(points, "z", layer.depth)


for pad in pads:

    if pad.shape is None:
        continue

    copper = net_map[pad.net]


    if isinstance(pad.shape, CompoundShape):

        for shape in pad.shape:

            points = np.array(shape.polygon()).T
            layer = layer_map[pad.layer_id]

            copper.AddPolygon(points, "z", layer.depth)

    else:

        points = np.array(pad.shape.polygon()).T
        layer = layer_map[pad.layer_id]

        copper.AddPolygon(points, "z", layer.depth)


for fp in footprints:

    if fp.shape is None:
        continue

    copper = csx.AddMetal(fp.reference)

    if isinstance(fp.shape, CompoundShape):

        for shape in fp.shape:

            points = np.array(shape.polygon()).T
            layer = layer_map[fp.layer_id]

            copper.AddPolygon(points, "z", layer.depth)

    else:

        points = np.array(fp.shape.polygon()).T
        layer = layer_map[fp.layer_id]

        copper.AddPolygon(points, "z", layer.depth)



csx.Write2XML("test.xml")