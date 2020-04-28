# Mechanism Variables

The variables in the mechanism can decide the position of links,
they are called as "input pairs" in Pyslvs.
"Input pairs" are supported with the undo and redo system,
they may be removed automatically if any component was removed.

## Inputs

### Variables

The kind of joints can split into two types, revolute (R) joint and slider joint.

#### Revolute Joint

There has a "base point" and a "driver point" in a input pair.
The base point is the origin point of coordinate system,
and the driver point is the vector.
Set the "angle" value as the rotate angle of the joint.

#### Slider Joint

The "base point" and "driver point" are the same point in a input pair
if the joint is a prismatic joint (P) or revolute-prismatic (RP) joint.
Set the "offset" value as the distance between pin and slot.

### Control

A simple constant speed display can be used on the variables.

There are currently no additional features.

## Analysis

### Records

The path simulation of the first variable will be calculated automatically.
Furthermore, the path is consisted by multiple points decided by interval of
"angle" or "offset" value, so the path can be recorded manually.
But there still has a limitation of its length.

The path data are supported with the undo and redo system.
But their colors will still mapping to current mechanism.
If there has any miss match, the path color will set to default.

### Plot

Plotting function can draw specified data for a joint.
The data is come from records, the sampling time will effect the results.

Currently support position, velocity, acceleration, jerk, curvature and path signature.
