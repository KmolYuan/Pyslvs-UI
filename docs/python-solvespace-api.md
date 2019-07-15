# Python-Solvespace API

## Namespace

The namespace of Python-Solvespace is `python_solvespace`.

The modules are:

+ [`slvs`](#module-slvs)

## Module `slvs`

### quaternion_u()

| qw | qx | qy | qz | return |
|:--:|:--:|:--:|:--:|:------:|
| float | float | float | float | Tuple[float, float, float] |

Input quaternion, return unit vector of U axis.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of quaternion.

### quaternion_v()

| qw | qx | qy | qz | return |
|:--:|:--:|:--:|:--:|:------:|
| float | float | float | float | Tuple[float, float, float] |

Input quaternion, return unit vector of V axis.

Signature is same as [quaternion_u](#quaternion_u).

### quaternion_n()

| qw | qx | qy | qz | return |
|:--:|:--:|:--:|:--:|:------:|
| float | float | float | float | Tuple[float, float, float] |

Input quaternion, return unit vector of normal.

Signature is same as [quaternion_u](#quaternion_u).

### make_quaternion()

| ux | uy | uz | vx | vy | vz | return |
|:--:|:--:|:--:|:--:|:--:|:--:|:------:|
| float | float | float | float | float | float | Tuple[float, float, float, float] |

Input two unit vector, return quaternion.

Where `ux`, `uy`, `uz` are corresponded to the value of U vector;
`vx`, `vy`, `vz` are corresponded to the value of V vector.

### Constraint

| type | inherit |
|:----:|:-------:|
| type | IntEnum |

Expose macro of constraint types.

### ResultFlag

| type | inherit |
|:----:|:-------:|
| type | IntEnum |

Expose macro of result flags.

### Params

| type | inherit |
|:----:|:-------:|
| type | object |

The handles of parameters.

#### Params.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

### Entity

| type | inherit |
|:----:|:-------:|
| type | object |

The handles of entities.

#### Class attributes of Entity

| name | type | description |
|:----:|:----:|:------------|
| FREE_IN_3D | [Entity] | The entity represented a spacial work plane object. If any 2D entity object in the constraint, the work plane must be input. |
| NONE | [Entity] | The entity represented a empty input of [Entity] object. |

#### Object attributes of Entity

| name | type | description |
|:----:|:----:|:------------|
| params | [Params] | The parameter of the entity. |

#### Entity.is_3d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 3D entity.

#### Entity.is_none()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a empty entity.

#### Entity.is_point_2d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 2D point.

#### Entity.is_point_3d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 3D point.

#### Entity.is_point()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a point.

#### Entity.is_normal_2d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 2D normal.

#### Entity.is_normal_3d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 3D normal.

#### Entity.is_normal()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a normal.

#### Entity.is_distance()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a distance.

#### Entity.is_work_plane()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a work plane.

#### Entity.is_line_2d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 2D line.

#### Entity.is_line_3d()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a 3D line.

#### Entity.is_line()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a line.

#### Entity.is_cubic()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a cubic.

#### Entity.is_circle()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a circle.

#### Entity.is_arc()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if this is a arc.

#### Entity.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

### SolverSystem

| type | inherit |
|:----:|:-------:|
| type | object |

A solver system of Python-Solvespace.

The operation of entities and constraints are using the methods of this class.

#### SolverSystem.\_\_init__()

| self | return |
|:----:|:------:|
| | None |

Initialization method. Create a solver system.

#### SolverSystem.clear()

| self | return |
|:----:|:------:|
| | None |

Clear the system.

#### SolverSystem.set_group()

| self | g | return |
|:----:|:---:|:------:|
| | int | None |

Set the current group (`g`).

#### SolverSystem.group()

| self | return |
|:----:|:------:|
| | int |

Return the current group.

#### SolverSystem.set_params()

| self | p | params | return |
|:----:|:---:|:----:|:------:|
| | [Params] | Sequence[float] | None |

Set the parameters from a [Params] handle (`p`) belong to this system.
The values is come from `params`, length must be equal to the handle.

#### SolverSystem.params()

| self | p | return |
|:----:|:---:|:------:|
| | [Params] | Tuple[float, ...] |

Get the parameters from a [Params] handle (`p`) belong to this system.
The length of tuple is decided by handle.

#### SolverSystem.dof()

| self | return |
|:----:|:------:|
| | int |

Return the degrees of freedom of current group. Only can be called after solving.

#### SolverSystem.constraints()

| self | return |
|:----:|:------:|
| | collections.Counter[str] |

Return the number of each constraint type.
The name of constraints is represented by string.

#### SolverSystem.faileds()

| self | return |
|:----:|:------:|
| | List[int] |

Return a list of failed constraint numbers.

#### SolverSystem.solve()

| self | return |
|:----:|:------:|
| | ResultFlag |

Start the solving, return the result flag.

#### SolverSystem.create_2d_base()

| self | return |
|:----:|:------:|
| | [Entity] |

Create a 2D system on current group, return the handle of work plane.

#### SolverSystem.add_point_2d()

| self | u | v | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| | float | float | [Entity] | [Entity] |

Add a 2D point to specific work plane (`wp`) then return the handle.

Where `u`, `v` are corresponded to the value of U, V axis on the work plane.

#### SolverSystem.add_point_3d()

| self | x | y | z | return |
|:----:|:---:|:---:|:---:|:------:|
| | float | float | float | [Entity] |

Add a 3D point then return the handle.

Where `x`, `y`, `z` are corresponded to the value of X, Y, Z axis.

#### SolverSystem.add_normal_2d()

| self | wp | return |
|:----:|:---:|:------:|
| | [Entity] | [Entity] |

Add a 2D normal orthogonal to specific work plane (`wp`) then return the handle.

#### SolverSystem.add_normal_3d()

| self | qw | qx | qy | qz | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
| | float | float | float | float | [Entity] |

Add a 3D normal from quaternion then return the handle.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of quaternion.

#### SolverSystem.add_distance()

| self | d | wp | return |
|:----:|:---:|:---:|:------:|
| | float | [Entity] | [Entity] |

Add a distance to specific work plane (`wp`) then return the handle.

Where `d` is distance value.

#### SolverSystem.add_line_2d()

| self | p1 | p2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | [Entity] |

Add a 2D line to specific work plane (`wp`) then return the handle.

Where `p1` is the start point;
`p2` is the end point.

#### SolverSystem.add_line_3d()

| self | p1 | p2 | return |
|:----:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] |

Add a 3D line then return the handle.

Where `p1` is the start point;
`p2` is the end point.

#### SolverSystem.add_cubic()

| self | p1 | p2 | p3 | p4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] |

Add a cubic curve to specific work plane (`wp`) then return the handle.

Where `p1` to `p4` is the control points.

#### SolverSystem.add_arc()

| self | nm | ct | start | end | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] |

Add an arc to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`start` is the start point;
`end` is the end point.

#### SolverSystem.add_circle()

| self | nm | ct | radius | wp | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] |

Add an circle to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`radius` is the distance value represent radius.

#### SolverSystem.add_work_plane()

| self | origin | nm | return |
|:----:|:------:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] |

Add a work plane then return the handle.

Where `origin` is the origin point of the plane;
`nm` is the orthogonal normal.

#### SolverSystem.add_constraint()

| self | c_type | wp | v | p1 | p2 | e1 | e2 | e3 | e4 | other | other2 | return |
|:----:|:------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:------:|
| | Constraint | [Entity] | float | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | int | int | None |
| | | | | | | | | [Entity.NONE] | [Entity.NONE] | 0 | 0 | |

Add a constraint by type code `c_type`.
This is an origin function mapping to different constraint methods.

Where `wp` represents work plane; `v` represents constraint value;
`p1` and `p2` represent point entities; `e1` to `e4` represent other types of entity;
`other` and `other2` are control options of the constraint.

#### SolverSystem.coincident()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.FREE_IN_3D] | |

Coincident two entities.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |
| [is_point] | [is_circle] | Optional |

#### SolverSystem.distance()

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:---:|:---:|:-----:|
| | [Entity] | [Entity] | float | [Entity] | None |
| | | | | [Entity.FREE_IN_3D] | |

Distance constraint between two entities.

If `value` is equal to zero, then turn into [coincident](#solversystemcoincident)

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |

#### SolverSystem.equal()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.FREE_IN_3D] | |

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

#### SolverSystem.equal_included_angle()

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | None |

Constraint that 2D line 1 (`e1`) and line 2 (`e2`), line 3 (`e3`) and line 4 (`e4`)
must have same included angle on work plane `wp`.

#### SolverSystem.equal_point_to_line()

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | [Entity] | [Entity] | None |

Constraint that point 1 (`e1`) and line 1 (`e2`), point 2 (`e3`) and line 2  (`e4`)
must have same distance on work plane `wp`.

#### SolverSystem.ratio()

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:---:|:---:|:-----:|
| | [Entity] | [Entity] | float | [Entity] | None |

The ratio (`value`) constraint between two 2D lines (`e1` and `e2`).

#### SolverSystem.symmetric()

| self | e1 | e2 | e3 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.NONE] | [Entity.FREE_IN_3D] | |

Symmetric constraint between two points.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Entity 3 (`e3`) | Work plane (`wp`) |
|:---------------:|:---------------:|:---------------:|:-----------------:|
| [is_point_3d] | [is_point_3d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |

#### SolverSystem.symmetric_h()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | None |

Symmetric constraint between two 2D points (`e1` and `e2`)
with horizontal line on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.symmetric_v()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | None |

Symmetric constraint between two 2D points (`e1` and `e2`)
with vertical line on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.midpoint()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:---:|
| | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.FREE_IN_3D] | |

Midpoint constraint between a point (`e1`) and a line (`e2`) on work plane (`wp`).

#### SolverSystem.horizontal()

| self | e1 | wp | return |
|:----:|:---:|:---:|:---:|
| | [Entity] | [Entity] | None |

Horizontal constraint of a 2d point (`e1`) on work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.vertical()

| self | e1 | wp | return |
|:----:|:---:|:---:|:----:|
| | [Entity] | [Entity] | None |

Vertical constraint of a 2d point (`e1`) on work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.diameter()

| self | e1 | value | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| | [Entity] | float | [Entity] | None |

Diameter (`value`) constraint of a circular entities.

| Entity 1 (`e1`) | Work plane (`wp`) |
|:---------------:|:-----------------:|
| [is_arc] | Optional |
| [is_circle] | Optional |

#### SolverSystem.same_orientation()

| self | e1 | e2 | return |
|:----:|:---:|:---:|:----:|
| | [Entity] | [Entity] | None |

Equal orientation constraint between two 3d normals (`e1` and `e2`).

#### SolverSystem.angle()

| self | e1 | e2 | value | wp | inverse | return |
|:----:|:---:|:---:|:---:|:---:|:------:|:------:|
| | [Entity] | [Entity] | float | [Entity] | bool | None |
| | | | | | False | |

Degrees angle (`value`) constraint between two 2d lines (`e1` and `e2`)
on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.perpendicular()

| self | e1 | e2 | wp | inverse | return |
|:----:|:---:|:---:|:---:|:------:|:------:|
| | [Entity] | [Entity] | [Entity] | bool | None |
| | | | | False | |

Perpendicular constraint between two 2d lines (`e1` and `e2`)
on the work plane (`wp` can not be [Entity.FREE_IN_3D]) with `inverse` option.

#### SolverSystem.parallel()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.FREE_IN_3D] | |

Parallel constraint between two lines (`e1` and `e2`) on the work plane (`wp`).

#### SolverSystem.tangent()

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | [Entity] | None |
| | | | [Entity.FREE_IN_3D] | |

Parallel constraint between two entities (`e1` and `e2`) on the work plane (`wp`).

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_arc] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |
| [is_cubic] | [is_line_3d] | [Entity.FREE_IN_3D] |
| [is_arc] | [is_cubic] | Is not [Entity.FREE_IN_3D] |
| [is_arc] | [is_arc] | Is not [Entity.FREE_IN_3D] |
| [is_cubic] | [is_cubic] | Optional |

#### SolverSystem.distance_proj()

| self | e1 | e2 | value | return |
|:----:|:---:|:---:|:---:|:------:|
| | [Entity] | [Entity] | float | None |

Projected distance (`value`) constraint between two 3d points (`e1` and `e2`).

#### SolverSystem.dragged()

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
| | [Entity] | [Entity] | None |
| | | [Entity.FREE_IN_3D] | |

Dragged constraint of a point (`e1`) on the work plane (`wp`).

[Params]: #params
[Entity]: #entity
[Entity.NONE]: #class-attributes-of-entity
[Entity.FREE_IN_3D]: #class-attributes-of-entity

[is_point]: #entityis_point
[is_point_2d]: #entityis_point_2d
[is_point_3d]: #entityis_point_3d
[is_work_plane]: #entityis_work_plane
[is_line]: #entityis_line
[is_line_2d]: #entityis_line_2d
[is_line_3d]: #entityis_line_3d
[is_arc]: #entityis_arc
[is_cubic]: #entityis_cubic
[is_circle]: #entityis_circle
