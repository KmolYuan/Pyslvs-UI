# Python-Solvespace API

## Module `python_solvespace`
<a id="python_solvespace"></a>

'python_solvespace' module is a wrapper of
Python binding Solvespace solver libraries.

### class Constraint

*Full name:* `python_solvespace.Constraint`
<a id="python_solvespace-constraint"></a>

| Bases |
|:-----:|
| `enum.IntEnum` |

| Enums |
|:-----:|
| POINTS_COINCIDENT |
| PT_PT_DISTANCE |
| PT_PLANE_DISTANCE |
| PT_LINE_DISTANCE |
| PT_FACE_DISTANCE |
| PT_IN_PLANE |
| PT_ON_LINE |
| PT_ON_FACE |
| EQUAL_LENGTH_LINES |
| LENGTH_RATIO |
| EQ_LEN_PT_LINE_D |
| EQ_PT_LN_DISTANCES |
| EQUAL_ANGLE |
| EQUAL_LINE_ARC_LEN |
| SYMMETRIC |
| SYMMETRIC_HORIZ |
| SYMMETRIC_VERT |
| SYMMETRIC_LINE |
| AT_MIDPOINT |
| HORIZONTAL |
| VERTICAL |
| DIAMETER |
| PT_ON_CIRCLE |
| SAME_ORIENTATION |
| ANGLE |
| PARALLEL |
| PERPENDICULAR |
| ARC_LINE_TANGENT |
| CUBIC_LINE_TANGENT |
| EQUAL_RADIUS |
| PROJ_PT_DISTANCE |
| WHERE_DRAGGED |
| CURVE_CURVE_TANGENT |
| LENGTH_DIFFERENCE |

### class Entity

*Full name:* `python_solvespace.Entity`
<a id="python_solvespace-entity"></a>

| Members | Type |
|:-------:|:----:|
| `FREE_IN_3D` | `ClassVar[Entity]` |
| `NONE` | `ClassVar[Entity]` |
| `params` | `Params` |

The handles of entities.

#### Entity.is_3d()

*Full name:* `python_solvespace.Entity.is_3d`
<a id="python_solvespace-entity-is_3d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 3D entity.

#### Entity.is_arc()

*Full name:* `python_solvespace.Entity.is_arc`
<a id="python_solvespace-entity-is_arc"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a arc.

#### Entity.is_circle()

*Full name:* `python_solvespace.Entity.is_circle`
<a id="python_solvespace-entity-is_circle"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a circle.

#### Entity.is_cubic()

*Full name:* `python_solvespace.Entity.is_cubic`
<a id="python_solvespace-entity-is_cubic"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a cubic.

#### Entity.is_distance()

*Full name:* `python_solvespace.Entity.is_distance`
<a id="python_solvespace-entity-is_distance"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a distance.

#### Entity.is_line()

*Full name:* `python_solvespace.Entity.is_line`
<a id="python_solvespace-entity-is_line"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a line.

#### Entity.is\_line\_2d()

*Full name:* `python_solvespace.Entity.is_line_2d`
<a id="python_solvespace-entity-is_line_2d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 2D line.

#### Entity.is\_line\_3d()

*Full name:* `python_solvespace.Entity.is_line_3d`
<a id="python_solvespace-entity-is_line_3d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 3D line.

#### Entity.is_none()

*Full name:* `python_solvespace.Entity.is_none`
<a id="python_solvespace-entity-is_none"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a empty entity.

#### Entity.is_normal()

*Full name:* `python_solvespace.Entity.is_normal`
<a id="python_solvespace-entity-is_normal"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a normal.

#### Entity.is\_normal\_2d()

*Full name:* `python_solvespace.Entity.is_normal_2d`
<a id="python_solvespace-entity-is_normal_2d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 2D normal.

#### Entity.is\_normal\_3d()

*Full name:* `python_solvespace.Entity.is_normal_3d`
<a id="python_solvespace-entity-is_normal_3d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 3D normal.

#### Entity.is_point()

*Full name:* `python_solvespace.Entity.is_point`
<a id="python_solvespace-entity-is_point"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a point.

#### Entity.is\_point\_2d()

*Full name:* `python_solvespace.Entity.is_point_2d`
<a id="python_solvespace-entity-is_point_2d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 2D point.

#### Entity.is\_point\_3d()

*Full name:* `python_solvespace.Entity.is_point_3d`
<a id="python_solvespace-entity-is_point_3d"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a 3D point.

#### Entity.is\_work\_plane()

*Full name:* `python_solvespace.Entity.is_work_plane`
<a id="python_solvespace-entity-is_work_plane"></a>

| self | return |
|:----:|:------:|
| `Self` | `bool` |

Return True if this is a work plane.

### make_quaternion()

*Full name:* `python_solvespace.make_quaternion`
<a id="python_solvespace-make_quaternion"></a>

| ux | uy | uz | vx | vy | vz | return |
|:---:|:---:|:---:|:---:|:---:|:---:|:------:|
| `float` | `float` | `float` | `float` | `float` | `float` | `tuple[float, float, float, float]` |

Input two unit vector, return quaternion.

Where `ux`, `uy`, `uz` are corresponded to the value of U vector;
`vx`, `vy`, `vz` are corresponded to the value of V vector.

### class Params

*Full name:* `python_solvespace.Params`
<a id="python_solvespace-params"></a>

Python object to handle multiple parameter handles.

### quaternion_n()

*Full name:* `python_solvespace.quaternion_n`
<a id="python_solvespace-quaternion_n"></a>

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| `float` | `float` | `float` | `float` | `tuple[float, float, float]` |

Input quaternion, return unit vector of normal.

Signature is same as [quaternion_u](#quaternion_u).

### quaternion_u()

*Full name:* `python_solvespace.quaternion_u`
<a id="python_solvespace-quaternion_u"></a>

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| `float` | `float` | `float` | `float` | `tuple[float, float, float]` |

Input quaternion, return unit vector of U axis.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of
quaternion.

### quaternion_v()

*Full name:* `python_solvespace.quaternion_v`
<a id="python_solvespace-quaternion_v"></a>

| qw | qx | qy | qz | return |
|:---:|:---:|:---:|:---:|:------:|
| `float` | `float` | `float` | `float` | `tuple[float, float, float]` |

Input quaternion, return unit vector of V axis.

Signature is same as [quaternion_u](#quaternion_u).

### class ResultFlag

*Full name:* `python_solvespace.ResultFlag`
<a id="python_solvespace-resultflag"></a>

| Bases |
|:-----:|
| `enum.IntEnum` |

| Enums |
|:-----:|
| OKAY |
| INCONSISTENT |
| DIDNT_CONVERGE |
| TOO_MANY_UNKNOWNS |

### class SolverSystem

*Full name:* `python_solvespace.SolverSystem`
<a id="python_solvespace-solversystem"></a>

A solver system of Python-Solvespace.

The operation of entities and constraints are using the methods of this
class.

#### SolverSystem.\_\_init\_\_()

*Full name:* `python_solvespace.SolverSystem.__init__`
<a id="python_solvespace-solversystem-__init__"></a>

| self | return |
|:----:|:------:|
| `Self` | `None` |

Initialize self.  See help(type(self)) for accurate signature.

#### SolverSystem.add_arc()

*Full name:* `python_solvespace.SolverSystem.add_arc`
<a id="python_solvespace-solversystem-add_arc"></a>

| self | nm | ct | start | end | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` |

Add an arc to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal; `ct` is the center point;
`start` is the start point; `end` is the end point.

#### SolverSystem.add_circle()

*Full name:* `python_solvespace.SolverSystem.add_circle`
<a id="python_solvespace-solversystem-add_circle"></a>

| self | nm | ct | radius | wp | return |
|:----:|:---:|:---:|:------:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` |

Add an circle to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`radius` is the distance value represent radius.

#### SolverSystem.add_constraint()

*Full name:* `python_solvespace.SolverSystem.add_constraint`
<a id="python_solvespace-solversystem-add_constraint"></a>

| self | c_type | wp | v | p1 | p2 | e1 | e2 | e3 | e4 | other | other2 | return |
|:----:|:------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----:|:------:|:------:|
| `Self` | `int` | `Entity` | `float` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `int` | `int` | `None` |
|   |   |   |   |   |   |   |   | `Entity.NONE` | `Entity.NONE` | `0` | `0` |   |   |

Add a constraint by type code `c_type`.
This is an origin function mapping to different constraint methods.

Where `wp` represents work plane; `v` represents constraint value;
`p1` and `p2` represent point entities; `e1` to `e4` represent other
types of entity;
`other` and `other2` are control options of the constraint.

#### SolverSystem.add_cubic()

*Full name:* `python_solvespace.SolverSystem.add_cubic`
<a id="python_solvespace-solversystem-add_cubic"></a>

| self | p1 | p2 | p3 | p4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` |

Add a cubic curve to specific work plane (`wp`) then return the
handle.

Where `p1` to `p4` is the control points.

#### SolverSystem.add_distance()

*Full name:* `python_solvespace.SolverSystem.add_distance`
<a id="python_solvespace-solversystem-add_distance"></a>

| self | d | wp | return |
|:----:|:---:|:---:|:------:|
| `Self` | `float` | `Entity` | `Entity` |

Add a distance to specific work plane (`wp`) then return the handle.

Where `d` is distance value.

#### SolverSystem.add\_line\_2d()

*Full name:* `python_solvespace.SolverSystem.add_line_2d`
<a id="python_solvespace-solversystem-add_line_2d"></a>

| self | p1 | p2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` |

Add a 2D line to specific work plane (`wp`) then return the handle.

Where `p1` is the start point; `p2` is the end point.

#### SolverSystem.add\_line\_3d()

*Full name:* `python_solvespace.SolverSystem.add_line_3d`
<a id="python_solvespace-solversystem-add_line_3d"></a>

| self | p1 | p2 | return |
|:----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` |

Add a 3D line then return the handle.

Where `p1` is the start point; `p2` is the end point.

#### SolverSystem.add\_normal\_2d()

*Full name:* `python_solvespace.SolverSystem.add_normal_2d`
<a id="python_solvespace-solversystem-add_normal_2d"></a>

| self | wp | return |
|:----:|:---:|:------:|
| `Self` | `Entity` | `Entity` |

Add a 2D normal orthogonal to specific work plane (`wp`)
then return the handle.

#### SolverSystem.add\_normal\_3d()

*Full name:* `python_solvespace.SolverSystem.add_normal_3d`
<a id="python_solvespace-solversystem-add_normal_3d"></a>

| self | qw | qx | qy | qz | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
| `Self` | `float` | `float` | `float` | `float` | `Entity` |

Add a 3D normal from quaternion then return the handle.

Where `qw`, `qx`, `qy`, `qz` are corresponded to
the W, X, Y, Z value of quaternion.

#### SolverSystem.add\_point\_2d()

*Full name:* `python_solvespace.SolverSystem.add_point_2d`
<a id="python_solvespace-solversystem-add_point_2d"></a>

| self | u | v | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `float` | `float` | `Entity` | `Entity` |

Add a 2D point to specific work plane (`wp`) then return the handle.

Where `u`, `v` are corresponded to the value of U, V axis on the work
plane.

#### SolverSystem.add\_point\_3d()

*Full name:* `python_solvespace.SolverSystem.add_point_3d`
<a id="python_solvespace-solversystem-add_point_3d"></a>

| self | x | y | z | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `float` | `float` | `float` | `Entity` |

Add a 3D point then return the handle.

Where `x`, `y`, `z` are corresponded to the value of X, Y, Z axis.

#### SolverSystem.add\_work\_plane()

*Full name:* `python_solvespace.SolverSystem.add_work_plane`
<a id="python_solvespace-solversystem-add_work_plane"></a>

| self | origin | nm | return |
|:----:|:------:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` |

Add a work plane then return the handle.

Where `origin` is the origin point of the plane;
`nm` is the orthogonal normal.

#### SolverSystem.angle()

*Full name:* `python_solvespace.SolverSystem.angle`
<a id="python_solvespace-solversystem-angle"></a>

| self | e1 | e2 | value | wp | inverse | return |
|:----:|:---:|:---:|:-----:|:---:|:-------:|:------:|
| `Self` | `Entity` | `Entity` | `float` | `Entity` | `bool` | `None` |
|   |   |   |   |   | `False` |   |   |

Degrees angle (`value`) constraint between two 2d lines (`e1` and
`e2`) on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.clear()

*Full name:* `python_solvespace.SolverSystem.clear`
<a id="python_solvespace-solversystem-clear"></a>

| self | return |
|:----:|:------:|
| `Self` | `None` |

Clear the system.

#### SolverSystem.coincident()

*Full name:* `python_solvespace.SolverSystem.coincident`
<a id="python_solvespace-solversystem-coincident"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.FREE_IN_3D` |   |   |

Coincident two entities.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |
| [is_point] | [is_circle] | Optional |

#### SolverSystem.constraints()

*Full name:* `python_solvespace.SolverSystem.constraints`
<a id="python_solvespace-solversystem-constraints"></a>

| self | return |
|:----:|:------:|
| `Self` | `collections.Counter[str]` |

Return the number of each constraint type.
The name of constraints is represented by string.

#### SolverSystem.create\_2d\_base()

*Full name:* `python_solvespace.SolverSystem.create_2d_base`
<a id="python_solvespace-solversystem-create_2d_base"></a>

| self | return |
|:----:|:------:|
| `Self` | `Entity` |

Create a 2D system on current group,
return the handle of work plane.

#### SolverSystem.diameter()

*Full name:* `python_solvespace.SolverSystem.diameter`
<a id="python_solvespace-solversystem-diameter"></a>

| self | e1 | value | wp | return |
|:----:|:---:|:-----:|:---:|:------:|
| `Self` | `Entity` | `float` | `Entity` | `None` |

Diameter (`value`) constraint of a circular entities.

| Entity 1 (`e1`) | Work plane (`wp`) |
|:---------------:|:-----------------:|
| [is_arc] | Optional |
| [is_circle] | Optional |

#### SolverSystem.distance()

*Full name:* `python_solvespace.SolverSystem.distance`
<a id="python_solvespace-solversystem-distance"></a>

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `float` | `Entity` | `None` |
|   |   |   |   | `Entity.FREE_IN_3D` |   |   |

Distance constraint between two entities.

If `value` is equal to zero, then turn into
[coincident](#solversystemcoincident)

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |

#### SolverSystem.distance_proj()

*Full name:* `python_solvespace.SolverSystem.distance_proj`
<a id="python_solvespace-solversystem-distance_proj"></a>

| self | e1 | e2 | value | return |
|:----:|:---:|:---:|:-----:|:------:|
| `Self` | `Entity` | `Entity` | `float` | `None` |

Projected distance (`value`) constraint between
two 3d points (`e1` and `e2`).

#### SolverSystem.dof()

*Full name:* `python_solvespace.SolverSystem.dof`
<a id="python_solvespace-solversystem-dof"></a>

| self | return |
|:----:|:------:|
| `Self` | `int` |

Return the degrees of freedom of current group.
Only can be called after solving.

#### SolverSystem.dragged()

*Full name:* `python_solvespace.SolverSystem.dragged`
<a id="python_solvespace-solversystem-dragged"></a>

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `None` |
|   |   | `Entity.FREE_IN_3D` |   |   |

Dragged constraint of a point (`e1`) on the work plane (`wp`).

#### SolverSystem.equal()

*Full name:* `python_solvespace.SolverSystem.equal`
<a id="python_solvespace-solversystem-equal"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.FREE_IN_3D` |   |   |

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

#### SolverSystem.equal\_included\_angle()

*Full name:* `python_solvespace.SolverSystem.equal_included_angle`
<a id="python_solvespace-solversystem-equal_included_angle"></a>

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `None` |

Constraint that 2D line 1 (`e1`) and line 2 (`e2`),
line 3 (`e3`) and line 4 (`e4`) must have same included angle on work
plane `wp`.

#### SolverSystem.equal\_point\_to\_line()

*Full name:* `python_solvespace.SolverSystem.equal_point_to_line`
<a id="python_solvespace-solversystem-equal_point_to_line"></a>

| self | e1 | e2 | e3 | e4 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `Entity` | `None` |

Constraint that point 1 (`e1`) and line 1 (`e2`),
point 2 (`e3`) and line 2  (`e4`) must have same distance on work
plane `wp`.

#### SolverSystem.failures()

*Full name:* `python_solvespace.SolverSystem.failures`
<a id="python_solvespace-solversystem-failures"></a>

| self | return |
|:----:|:------:|
| `Self` | `list[int]` |

Return a list of failed constraint numbers.

#### SolverSystem.group()

*Full name:* `python_solvespace.SolverSystem.group`
<a id="python_solvespace-solversystem-group"></a>

| self | return |
|:----:|:------:|
| `Self` | `int` |

Return the current group.

#### SolverSystem.horizontal()

*Full name:* `python_solvespace.SolverSystem.horizontal`
<a id="python_solvespace-solversystem-horizontal"></a>

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `None` |

Vertical constraint of a 2d point (`e1`) on
work plane (`wp` can not be [Entity.FREE_IN_3D]).

#### SolverSystem.midpoint()

*Full name:* `python_solvespace.SolverSystem.midpoint`
<a id="python_solvespace-solversystem-midpoint"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.FREE_IN_3D` |   |   |

Midpoint constraint between a point (`e1`) and
a line (`e2`) on work plane (`wp`).

#### SolverSystem.parallel()

*Full name:* `python_solvespace.SolverSystem.parallel`
<a id="python_solvespace-solversystem-parallel"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.FREE_IN_3D` |   |   |

Parallel constraint between two lines (`e1` and `e2`) on
the work plane (`wp`).

#### SolverSystem.params()

*Full name:* `python_solvespace.SolverSystem.params`
<a id="python_solvespace-solversystem-params"></a>

| self | p | return |
|:----:|:---:|:------:|
| `Self` | `Params` | `tuple[float, ...]` |

Get the parameters from a [Params] handle (`p`) belong to this
system.
The length of tuple is decided by handle.

#### SolverSystem.perpendicular()

*Full name:* `python_solvespace.SolverSystem.perpendicular`
<a id="python_solvespace-solversystem-perpendicular"></a>

| self | e1 | e2 | wp | inverse | return |
|:----:|:---:|:---:|:---:|:-------:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `bool` | `None` |
|   |   |   |   | `False` |   |   |

Perpendicular constraint between two 2d lines (`e1` and `e2`)
on the work plane (`wp` can not be [Entity.FREE_IN_3D]) with
`inverse` option.

#### SolverSystem.ratio()

*Full name:* `python_solvespace.SolverSystem.ratio`
<a id="python_solvespace-solversystem-ratio"></a>

| self | e1 | e2 | value | wp | return |
|:----:|:---:|:---:|:-----:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `float` | `Entity` | `None` |

The ratio (`value`) constraint between two 2D lines (`e1` and
`e2`).

#### SolverSystem.same_orientation()

*Full name:* `python_solvespace.SolverSystem.same_orientation`
<a id="python_solvespace-solversystem-same_orientation"></a>

| self | e1 | e2 | return |
|:----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `None` |

Equal orientation constraint between two 3d normals (`e1` and
`e2`).

#### SolverSystem.set_group()

*Full name:* `python_solvespace.SolverSystem.set_group`
<a id="python_solvespace-solversystem-set_group"></a>

| self | g | return |
|:----:|:---:|:------:|
| `Self` | `int` | `None` |

Set the current group (`g`).

#### SolverSystem.set_params()

*Full name:* `python_solvespace.SolverSystem.set_params`
<a id="python_solvespace-solversystem-set_params"></a>

| self | p | params | return |
|:----:|:---:|:------:|:------:|
| `Self` | `Params` | `collections.abc.Sequence[float]` | `None` |

Set the parameters from a [Params] handle (`p`) belong to this
system.
The values is come from `params`, length must be equal to the handle.

#### SolverSystem.solve()

*Full name:* `python_solvespace.SolverSystem.solve`
<a id="python_solvespace-solversystem-solve"></a>

| self | return |
|:----:|:------:|
| `Self` | `int` |

Start the solving, return the result flag.

#### SolverSystem.symmetric()

*Full name:* `python_solvespace.SolverSystem.symmetric`
<a id="python_solvespace-solversystem-symmetric"></a>

| self | e1 | e2 | e3 | wp | return |
|:----:|:---:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.NONE` | `Entity.FREE_IN_3D` |   |   |

Symmetric constraint between two points.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Entity 3 (`e3`) | Work plane (`wp`) |
|:---------------:|:---------------:|:---------------:|:-----------------:|
| [is_point_3d] | [is_point_3d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |

#### SolverSystem.symmetric_h()

*Full name:* `python_solvespace.SolverSystem.symmetric_h`
<a id="python_solvespace-solversystem-symmetric_h"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |

Symmetric constraint between two 2D points (`e1` and `e2`)
with horizontal line on the work plane (`wp` can not be
[Entity.FREE_IN_3D]).

#### SolverSystem.symmetric_v()

*Full name:* `python_solvespace.SolverSystem.symmetric_v`
<a id="python_solvespace-solversystem-symmetric_v"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |

Symmetric constraint between two 2D points (`e1` and `e2`)
with vertical line on the work plane (`wp` can not be
[Entity.FREE_IN_3D]).

#### SolverSystem.tangent()

*Full name:* `python_solvespace.SolverSystem.tangent`
<a id="python_solvespace-solversystem-tangent"></a>

| self | e1 | e2 | wp | return |
|:----:|:---:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `Entity` | `None` |
|   |   |   | `Entity.FREE_IN_3D` |   |   |

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

*Full name:* `python_solvespace.SolverSystem.vertical`
<a id="python_solvespace-solversystem-vertical"></a>

| self | e1 | wp | return |
|:----:|:---:|:---:|:------:|
| `Self` | `Entity` | `Entity` | `None` |

Vertical constraint of a 2d point (`e1`) on
work plane (`wp` can not be [Entity.FREE_IN_3D]).
