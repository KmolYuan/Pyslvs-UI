# Mechanism Variables

The variables in the mechanism can decide the position of links,
they are called as "input pairs" in Pyslvs.
"Input pairs" are supported with the undo and redo system,
they may be removed automatically if any component was removed.

## Revolute Joint

There has a "base point" and a "driver point" in a input pair.
The base point is the origin point of coordinate system,
and the driver point is the vector.
Set the "angle" value as the rotate angle of the joint.

## Slider Joint

The "base point" and "driver point" are the same point in a input pair
if the joint is a prismatic joint or revolute-prismatic joint.
Set the "offset" value as the distance between pin and slot.

## Records

The path simulation of the first variable will be calculated automatically.
Furthermore, the path is consisted by multiple points decided by interval of
"angle" or "offset" value, so the path can be recorded manually.
But there still has a limitation of its length.

The path data are supported with the undo and redo system.
But their colors will still mapping to current mechanism.
If there has any miss match, the path color will set to default.
