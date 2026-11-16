# Changelog

All notable changes to CloneSensor are listed here.

## [1.0.0-beta] — 2026-11

First public beta.

- Tested placement: every candidate is checked against reserved space before it is kept. Nothing is pushed apart afterward.
- Seven sampling modes: Random, Poisson Disk, Blue Noise, Grid, Hex Packing, Vertex, Polygon Center.
- Layout presets: Crowd, Seating, Festival, Parking, Booths, converted to the project's units.
- Collision modes: Sphere, Bounding Box, Footprint (with optional Footprint Proxy), tested as 3D Radius or Surface Radius.
- Keep Away: edge margin with falloff, spline margin, and Cinema 4D field lists.
- Orientation: Surface Normal, World Up, Position Scale Rotation, Spline Direction, Random Rotation, and Sit on Surface.
- Fill Surface with Fill Safety limit (20,000 by default) and Spread Across Surface growth.
- Rules: categories, weights, priorities and per-category clearance with real-world units.
- Output: Instances, Render Instances, Multi-Instance, Point Cloud, Cloner.
- Debug overlays and Show Statistics.
