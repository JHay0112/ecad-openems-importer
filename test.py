from src.ecad_impl.kicad7 import KiCAD7Board
from src.ecad_intf.board import Board
from src.shapes.circle import Circle
from src.shapes.shape import Shape
from src.shapes.compound import CompoundShape

from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from math import pi

import os
import numpy as np


INPUT_BOARD = "ti_ant.kicad_pcb"

RESULTS_DIR = os.path.abspath("out")

SUBSTR_EPS_R = 3.38
SUBSTR_KAPPA = 1e-3 * 2 * pi * 2.45e9 * EPS0 * SUBSTR_EPS_R


NUM_THREADS = 8
MESH_SCALE_FACTOR = 200

FEED_R = 50

F0 = 2.4e9
FC = 1e9

X_PAD = 25
Y_PAD = 25
Z_PAD = 10



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

nets = set(feature.net for feature in tracks)
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



source_start = None
source_end = None


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


    if fp.reference == "TP1":
        pos = fp.shape.centre()
        layer = layer_map[fp.layer_id]
        source_start = (pos[0], pos[1], layer.depth)

    if fp.reference == "TP2":
        pos = fp.shape.centre()
        layer = layer_map[fp.layer_id]
        source_end = (pos[0], pos[1], layer.depth)



pad_vec = np.array([X_PAD, Y_PAD, Z_PAD])
bbox_start = np.array(bbox[0]) - pad_vec
bbox_end = np.array(bbox[1]) + pad_vec
x_bound = [bbox_start[0], bbox_end[0]]
y_bound = [bbox_start[1], bbox_end[1]]
z_bound = [bbox_start[2], bbox_end[2]]

sim = openEMS(NrTS = 60000, EndCriteria = 1e-4)
sim.SetGaussExcite(F0, FC)
sim.SetBoundaryCond(["MUR", "MUR", "MUR", "MUR", "MUR", "MUR"])

sim.SetCSX(csx)

mesh = csx.GetGrid()
mesh.SetDeltaUnit(1e-3)
mesh_res = C0 / ((F0 + FC) * 1e-3)
mesh_res /= MESH_SCALE_FACTOR

mesh.AddLine("x", x_bound)
mesh.AddLine("z", z_bound)
mesh.AddLine("y", y_bound)


for prop in csx.GetAllProperties():
    sim.AddEdges2Grid(dirs = "xyz", properties = prop, metal_edge_res = mesh_res / 2)


e_dump = csx.AddDump("Et")
start, end = bbox
e_dump.AddBox(start, end)


port = sim.AddLumpedPort(1, FEED_R, source_start, source_end, "y", 1.0, priority = 5, edges2grid = "all")
mesh.SmoothMeshLines("all", mesh_res)
nf2ff = sim.CreateNF2FFBox()


# csx.Write2XML("test.xml")
# exit()

sim.Run(RESULTS_DIR, verbose = 3, numThreads = NUM_THREADS)