# ECAD OpenEMS Importer

This repository contains a rudimentary application for importing PCB files from an ECAD tool into
OpenEMS. At the moment, I'm just experimenting and targeting KiCAD7 and OpenEMS in particular.
However, I am aiming to leave the interfaces to the ECAD application and the EMS application as
broad as possible so it's not too hard to change in the future. 

At the moment there is enough functionality between the KiCAD interface and the test script to
import the rough outline of a PCB and approximate the shape of some of the traces on the board
in OpenEMS. This is enough to show that the idea is solid, but not enough to do anything very useful
with without a lot of manual work. Once the application is mature it should be able to function as a
simple intermediary for bringing a PCB design into OpenEMS and automatically generating a suitable
mesh.

## Roadmap

- [ ] Produce polygons describing continuous copper areas on all layers.
      (Ideally single polygon per area.)
- [ ] Produce vias and plated through holes at prescribed positions that provide electrical
      connection and air gap in the middle.
- [ ] Improve meshing beyond automatic utility provided by openEMS and guess/check.
