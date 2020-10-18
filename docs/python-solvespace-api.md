# Python-Solvespace API

## Module `python_solvespace`

'python_solvespace' module is a wrapper of
Python binding Solvespace solver libraries.

### quaternion_u()

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| float | float | float | float | Tuple\[float, float, float] |

Input quaternion, return unit vector of U axis.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of
quaternion.

### quaternion_v()

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| float | float | float | float | Tuple\[float, float, float] |

Input quaternion, return unit vector of V axis.

Signature is same as [quaternion_u](#quaternion_u).

### quaternion_n()

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| float | float | float | float | Tuple\[float, float, float] |

Input quaternion, return unit vector of normal.

Signature is same as [quaternion_u](#quaternion_u).

### make_quaternion()

| ux | uy | uz | vx | vy | vz | return |
|:---:|:---:|:---:|:---:|:---:|:---:|:------:|
| float | float | float | float | float | float | Tuple\[float, float, float, float] |

Input two unit vector, return quaternion.

Where `ux`, `uy`, `uz` are corresponded to the value of U vector;
`vx`, `vy`, `vz` are corresponded to the value of V vector.

### Constraint

Inherited from `IntEnum`.

Is an enum class.

| POINTS_COINCIDENT | PT\_PT_DISTANCE | PT\_PLANE_DISTANCE | PT\_LINE_DISTANCE | PT\_FACE_DISTANCE | PT\_IN_PLANE | PT\_ON_LINE | PT\_ON_FACE | EQUAL\_LENGTH_LINES | LENGTH_RATIO | EQ\_LEN\_PT\_LINE_D | EQ\_PT\_LN_DISTANCES | EQUAL_ANGLE | EQUAL\_LINE\_ARC_LEN | SYMMETRIC | SYMMETRIC_HORIZ | SYMMETRIC_VERT | SYMMETRIC_LINE | AT_MIDPOINT | HORIZONTAL | VERTICAL | DIAMETER | PT\_ON_CIRCLE | SAME_ORIENTATION | ANGLE | PARALLEL | PERPENDICULAR | ARC\_LINE_TANGENT | CUBIC\_LINE_TANGENT | EQUAL_RADIUS | PROJ\_PT_DISTANCE | WHERE_DRAGGED | CURVE\_CURVE_TANGENT | LENGTH_DIFFERENCE |
|:-----------------:|:--------------:|:-----------------:|:----------------:|:----------------:|:-----------:|:----------:|:----------:|:------------------:|:------------:|:----------------:|:------------------:|:-----------:|:------------------:|:---------:|:---------------:|:--------------:|:--------------:|:-----------:|:----------:|:--------:|:--------:|:------------:|:----------------:|:-----:|:--------:|:-------------:|:----------------:|:------------------:|:------------:|:----------------:|:-------------:|:-------------------:|:-----------------:|
| `100000` | `100001` | `100002` | `100003` | `100004` | `100005` | `100006` | `100007` | `100008` | `100009` | `100010` | `100011` | `100012` | `100013` | `100014` | `100015` | `100016` | `100017` | `100018` | `100019` | `100020` | `100021` | `100022` | `100023` | `100024` | `100025` | `100026` | `100027` | `100028` | `100029` | `100030` | `100031` | `100032` | `100033` |

An enumeration.

### ResultFlag

Inherited from `IntEnum`.

Is an enum class.

| OKAY | INCONSISTENT | DIDNT_CONVERGE | TOO\_MANY_UNKNOWNS |
|:----:|:------------:|:--------------:|:-----------------:|
| `0` | `1` | `2` | `3` |

An enumeration.

### Params

Inherited from `object`.

Python object to handle multiple parameter handles.

#### Params.\_\_init__()

| self | **args | **kwargs | return |
|:----:|:------:|:--------:|:------:|
|   | Any | Any | Any |

Initialize self.  See help(type(self)) for accurate signature.

### Entity

Inherited from `object`.

| FREE\_IN_3D | NONE | params |
|:----------:|:----:|:------:|
| ClassVar\[python\_solvespace.slvs.Entity] | ClassVar\[python\_solvespace.slvs.Entity] | Params |

The handles of entities.

#### Entity.\_\_init__()

| self | **args | **kwargs | return |
|:----:|:------:|:--------:|:------:|
|   | Any | Any | Any |

Initialize self.  See help(type(self)) for accurate signature.

#### Entity.is_3d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 3D entity.

#### Entity.is_arc()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a arc.

#### Entity.is_circle()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a circle.

#### Entity.is_cubic()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a cubic.

#### Entity.is_distance()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a distance.

#### Entity.is_line()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a line.

#### Entity.is\_line_2d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 2D line.

#### Entity.is\_line_3d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 3D line.

#### Entity.is_none()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a empty entity.

#### Entity.is_normal()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a normal.

#### Entity.is\_normal_2d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 2D normal.

#### Entity.is\_normal_3d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 3D normal.

#### Entity.is_point()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a point.

#### Entity.is\_point_2d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 2D point.

#### Entity.is\_point_3d()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a 3D point.

#### Entity.is\_work_plane()

| self | return |
|:----:|:------:|
|   | bool |

Return True if this is a work plane.

### SolverSystem

Inherited from `object`.

A solver system of Python-Solvespace.

The operation of entities and constraints are using the methods of this
class.

#### SolverSystem.\_\_init__()

| self | return |
|:----:|:------:|
|   | None |

Initialization method. Create a solver system.

#### SolverSystem.add_arc()

| self | nm | ct | start | end | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | Entity | Entity |

Add an arc to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal; `ct` is the center point;
`start` is the start point; `end` is the end point.

#### SolverSystem.add_circle()

| self | nm | ct | radius | wp | return |
|:----:|:---:|:---:|:------:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | Entity |

Add an circle to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`radius` is the distance value represent radius.

#### SolverSystem.add_constraint()

| self | c_type | wp | v | p1 | p2 | e1 | e2 | e3 | e4 | other | other2 | return |
|:----:|:------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----:|:------:|:------:|
|   | int | Entity | float | Entity | Entity | Entity | Entity | Entity | Entity | int | int | None |
|   |   |   |   |   |   |   |   | ... | ... | 0 | 0 |   |

Add a constraint by type code `c_type`.
This is an origin function mapping to different constraint methods.

Where `wp` represents work plane; `v` represents constraint value;
`p1` and `p2` represent point entities; `e1` to `e4` represent other
types of entity;
`other` and `other2` are control options of the constraint.

#### SolverSystem.add_cubic()

| self | p1 | p2 | p3 | p4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | Entity | Entity |

Add a cubic curve to specific work plane (`wp`) then return the
handle.

Where `p1` to `p4` is the control points.

#### SolverSystem.add_distance()

| self | d | wp | return |
|:----:|:---:|:---:|:------:|
|   | float | Entity | Entity |

Add a distance to specific work plane (`wp`) then return the handle.

Where `d` is distance value.

#### SolverSystem.add\_line_2d()

| self | p1 | p2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity |

Add a 2D line to specific work plane (`wp`) then return the handle.

Where `p1` is the start point; `p2` is the end point.

#### SolverSystem.add\_line_3d()

| self | p1 | p2 | return |
|:----:|:---:|:---:|:------:|
|   | Entity | Entity | Entity |

Add a 3D line then return the handle.

Where `p1` is the start point; `p2` is the end point.

#### SolverSystem.add\_normal_2d()

| self | wp | return |
|:----:|:---:|:------:|
|   | Entity | Entity |

Add a 2D normal orthogonal to specific work plane (`wp`)
then return the handle.

#### SolverSystem.add\_normal_3d()

| self | qw | qx | qy | qz | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
|   | float | float | float | float | Entity |

Add a 3D normal from quaternion then return the handle.

Where `qw`, `qx`, `qy`, `qz` are corresponded to
the W, X, Y, Z value of quaternion.

#### SolverSystem.add\_point_2d()

| self | u | v | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | float | float | Entity | Entity |

Add a 2D point to specific work plane (`wp`) then return the handle.

Where `u`, `v` are corresponded to the value of U, V axis on the work
plane.

#### SolverSystem.add\_point_3d()

| self | x | y | z | return |
|:----:|:---:|:---:|:---:|:------:|
|   | float | float | float | Entity |

Add a 3D point then return the handle.

Where `x`, `y`, `z` are corresponded to the value of X, Y, Z axis.

#### SolverSystem.add\_work_plane()

| self | origin | nm | return |
|:----:|:------:|:---:|:------:|
|   | Entity | Entity | Entity |

Add a work plane then return the handle.

Where `origin` is the origin point of the plane;
`nm` is the orthogonal normal.

#### SolverSystem.angle()

| self | e1 | e2 | value | wp | inverse | return |
|:----:|:---:|:---:|:-----:|:---:|:-------:|:------:|
|   | Entity | Entity | float | Entity | bool | None |
|   |   |   |   |   | False |   |

Degrees angle (`value`) constraint between two 2d lines (`e1` and
`e2`) on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.clear()

| self | return |
|:----:|:------:|
|   | None |

Clear the system.

#### SolverSystem.coincident()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |
|   |   |   | ... |   |

Coincident two entities.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |
| [is_point] | [is_circle] | Optional |

#### SolverSystem.constraints()

| self | return |
|:----:|:------:|
|   | Counter\[str] |

Return the number of each constraint type.
The name of constraints is represented by string.

#### SolverSystem.create_2d_base()

| self | return |
|:----:|:------:|
|   | Entity |

Create a 2D system on current group,
return the handle of work plane.

#### SolverSystem.diameter()

| self | e1 | value | wp | return |
|:----:|:---:|:-----:|:---:|:------:|
|   | Entity | float | Entity | None |

Diameter (`value`) constraint of a circular entities.

| Entity 1 (`e1`) | Work plane (`wp`) |
|:---------------:|:-----------------:|
| [is_arc] | Optional |
| [is_circle] | Optional |

#### SolverSystem.distance()

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:------:|
|   | Entity | Entity | float | Entity | None |
|   |   |   |   | ... |   |

Distance constraint between two entities.

If `value` is equal to zero, then turn into
[coincident](#solversystemcoincident)

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |

#### SolverSystem.distance_proj()

| self | e1 | e2 | value | return |
|:----:|:---:|:---:|:-----:|:------:|
|   | Entity | Entity | float | None |

Projected distance (`value`) constraint between
two 3d points (`e1` and `e2`).

#### SolverSystem.dof()

| self | return |
|:----:|:------:|
|   | int |

Return the degrees of freedom of current group.
Only can be called after solving.

#### SolverSystem.dragged()

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
|   | Entity | Entity | None |
|   |   | ... |   |

Dragged constraint of a point (`e1`) on the work plane (`wp`).

#### SolverSystem.equal()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |
|   |   |   | ... |   |

Equal constraint between two entities.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_line] | [is_line] | Optional |
| [is_line] | [is_arc] | Optional |
| [is_line] | [is_circle] | Optional |
| [is_arc] | [is_arc] | Optional |
| [is_arc] | [is_circle] | Optional |
| [is_circle] | [is_circle] | Optional |
| [is_circle] | [is_arc] | Optional |

#### SolverSystem.equal\_included_angle()

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | Entity | None |

Constraint that 2D line 1 (`e1`) and line 2 (`e2`),
line 3 (`e3`) and line 4 (`e4`) must have same included angle on work
plane `wp`.

#### SolverSystem.equal\_point\_to_line()

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | Entity | None |

Constraint that point 1 (`e1`) and line 1 (`e2`),
point 2 (`e3`) and line 2  (`e4`) must have same distance on work
plane `wp`.

#### SolverSystem.failures()

| self | return |
|:----:|:------:|
|   | List\[int] |

Return a list of failed constraint numbers.

#### SolverSystem.group()

| self | return |
|:----:|:------:|
|   | int |

Return the current group.

#### SolverSystem.horizontal()

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
|   | Entity | Entity | None |

Vertical constraint of a 2d point (`e1`) on
work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.midpoint()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |
|   |   |   | ... |   |

Midpoint constraint between a point (`e1`) and
a line (`e2`) on work plane (`wp`).

#### SolverSystem.parallel()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |
|   |   |   | ... |   |

Parallel constraint between two lines (`e1` and `e2`) on
the work plane (`wp`).

#### SolverSystem.params()

| self | p | return |
|:----:|:---:|:------:|
|   | Params | Tuple\[float, ...] |

Get the parameters from a [Params] handle (`p`) belong to this
system.
The length of tuple is decided by handle.

#### SolverSystem.perpendicular()

| self | e1 | e2 | wp | inverse | return |
|:----:|:---:|:---:|:---:|:-------:|:------:|
|   | Entity | Entity | Entity | bool | None |
|   |   |   |   | False |   |

Perpendicular constraint between two 2d lines (`e1` and `e2`)
on the work plane (`wp` can not be [Entity.FREE_IN_3D]) with
`inverse` option.

#### SolverSystem.ratio()

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:------:|
|   | Entity | Entity | float | Entity | None |

The ratio (`value`) constraint between two 2D lines (`e1` and
`e2`).

#### SolverSystem.same_orientation()

| self | e1 | e2 | return |
|:----:|:---:|:---:|:------:|
|   | Entity | Entity | None |

Equal orientation constraint between two 3d normals (`e1` and
`e2`).

#### SolverSystem.set_group()

| self | g | return |
|:----:|:---:|:------:|
|   | int | None |

Set the current group (`g`).

#### SolverSystem.set_params()

| self | p | params | return |
|:----:|:---:|:------:|:------:|
|   | Params | Sequence\[float] | None |

Set the parameters from a [Params] handle (`p`) belong to this
system.
The values is come from `params`, length must be equal to the handle.

#### SolverSystem.solve()

| self | return |
|:----:|:------:|
|   | int |

Start the solving, return the result flag.

#### SolverSystem.symmetric()

| self | e1 | e2 | e3 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | Entity | None |
|   |   |   | ... | ... |   |

Symmetric constraint between two points.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Entity 3 (`e3`) | Work plane (`wp`) |
|:---------------:|:---------------:|:---------------:|:-----------------:|
| [is_point_3d] | [is_point_3d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |

#### SolverSystem.symmetric_h()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |

Symmetric constraint between two 2D points (`e1` and `e2`)
with horizontal line on the work plane (`wp` can not be
[Entity.FREE_IN_3D]).

#### SolverSystem.symmetric_v()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |

Symmetric constraint between two 2D points (`e1` and `e2`)
with vertical line on the work plane (`wp` can not be
[Entity.FREE_IN_3D]).

#### SolverSystem.tangent()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
|   | Entity | Entity | Entity | None |
|   |   |   | ... |   |

Parallel constraint between two entities (`e1` and `e2`) on the
work plane (`wp`).

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_arc] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |
| [is_cubic] | [is_line_3d] | [Entity.FREE_IN_3D] |
| [is_arc] | [is_cubic] | Is not [Entity.FREE_IN_3D] |
| [is_arc] | [is_arc] | Is not [Entity.FREE_IN_3D] |
| [is_cubic] | [is_cubic] | Optional |

#### SolverSystem.vertical()

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
|   | Entity | Entity | None |

Vertical constraint of a 2d point (`e1`) on
work plane (`wp` can not be [Entity.FREE_IN_3D]).

[quaternion_u]: #quaternion_u
[Params]: #params
[Entity.FREE_IN_3D]: #entity
[is_arc]: #entityis_arc
[is_circle]: #entityis_circle
[is_cubic]: #entityis_cubic
[is_line]: #entityis_line
[is_line_2d]: #entityis_line_2d
[is_line_3d]: #entityis_line_3d
[is_point]: #entityis_point
[is_point_2d]: #entityis_point_2d
[is_point_3d]: #entityis_point_3d
[is_work_plane]: #entityis_work_plane
[coincident]: #solversystemcoincident
