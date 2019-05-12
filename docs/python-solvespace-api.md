# Namespace

The namespace of Python-Solvespace is `slvs`.

# Functions

## quaternion_u(qw: float, qx: float, qy: float, qz: float) -> Tuple\[float, float, float] {#quaternion_u data-toc-label='quaternion_u'}

Input quaternion, return unit vector of U axis.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of quaternion.

## quaternion_v(qw: float, qx: float, qy: float, qz: float) -> Tuple\[float, float, float] {#quaternion_v data-toc-label='quaternion_v'}

Input quaternion, return unit vector of V axis.

Signature is same as [quaternion_u](#quaternion_u).

## quaternion_n(qw: float, qx: float, qy: float, qz: float) -> Tuple\[float, float, float] {#quaternion_n data-toc-label='quaternion_n'}

Input quaternion, return unit vector of normal.

Signature is same as [quaternion_u](#quaternion_u).

## make_quaternion(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> Tuple\[float, float, float, float] {#make_quaternion data-toc-label='make_quaternion'}

Input two unit vector, return quaternion.

Where `ux`, `uy`, `uz` are corresponded to the value of U vector;
`vx`, `vy`, `vz` are corresponded to the value of V vector.

# Classes

## class Constraint(IntEnum)  {#constraint}

Expose macro of constraint types.

## class ResultFlag(IntEnum) {#resultflag}

Expose macro of result flags.

## class Params(object) {#params}

The handles of parameters.

### Params.\_\_repr__(self) -> str {#params-\_\_repr__}

Over loaded method to print the objects.

## class Entity(object) {#entity}

The handles of entities.                 

### Entity.FREE_IN_3D: Entity {#entity-free_in_3d}

**\[Class attribute]** The entity represented a spacial work plane object.

### Entity.NONE: Entity {#entity-none}

**\[Class attribute]** The entity represented a empty input of [`Entity`](#entity) object.

### Entity.params: Params {#entity-params}

**\[Object attribute]** The parameter of this entity.

### Entity.is_3d(self) -> bool {#entity-is_3d}

Return True if this is a 3D entity.

### Entity.is_none(self) -> bool {#entity-is_none}

Return True if this is a empty entity.

### Entity.is_point_2d(self) -> bool {#entity-is_point_2d}

Return True if this is a 2D point.

### Entity.is_point_3d(self) -> bool {#entity-is_point_3d}

Return True if this is a 3D point.

### Entity.is_point(self) -> bool {#entity-is_point}

Return True if this is a point.

### Entity.is_normal_2d(self) -> bool {#entity-is_normal_2d}

Return True if this is a 2D normal.

### Entity.is_normal_3d(self) -> bool {#entity-is_normal_3d}

Return True if this is a 3D normal.

### Entity.is_normal(self) -> bool {#entity-is_normal}

Return True if this is a normal.

### Entity.is_distance(self) -> bool {#entity-is_distance}

Return True if this is a distance.

### Entity.is_work_plane(self) -> bool {#entity-is_work_plane}

Return True if this is a work plane.

### Entity.is_line_2d(self) -> bool {#entity-is_line_2d}

Return True if this is a 2D line.

### Entity.is_line_3d(self) -> bool {#entity-is_line_3d}

Return True if this is a 3D line.

### Entity.is_line(self) -> bool {#entity-is_line}

Return True if this is a line.

### Entity.is_cubic(self) -> bool {#entity-is_cubic}

Return True if this is a cubic.

### Entity.is_circle(self) -> bool {#entity-is_circle}

Return True if this is a circle.

### Entity.is_arc(self) -> bool {#entity-is_arc}

Return True if this is a arc.

### Entity.\_\_repr__(self) -> str {#entity-\_\_repr__}

Over loaded method to print the objects.

## class SolverSystem(object) {#solversystem}

A solver system of Python-Solvespace.

The operation of entities and constraints are using the methods of this class.

### SolverSystem.\_\_init__(self) -> None {#solversystem-\_\_init__}

Initialization method. Create a solver system.

### SolverSystem.clear(self) -> None {#solversystem-clear}

Clear the system.

### SolverSystem.set_group(self, g: int) -> None {#solversystem-set_group}

Set the current group (`g`).

### SolverSystem.group(self) -> int {#solversystem-group}

Return the current group.

### SolverSystem.params(self, p: Params) -> Tuple\[float, ...] {#solversystem-params}

Get the parameters from a [`Params`](#params) handle (`p`) belong to this system.
The length of tuple is decided by handle.

### SolverSystem.dof(self) -> int {#solversystem-dof}

Return the degrees of freedom of current group. Only can be called after solving.

### SolverSystem.constraints(self) -> collections.Counter\[str] {#solversystem-constraints}

Return the number of each constraint type.
The name of constraints is represented by string.

### SolverSystem.faileds(self) -> List\[int] {#solversystem-faileds}

Return a list of failed constraint numbers.

### SolverSystem.solve(self) -> ResultFlag {#solversystem-solve}

Start the solving, return the result flag.

### SolverSystem.create_2d_base(self) -> Entity {#create_2d_base}

Create a 2D system on current group, return the handle of work plane.

### SolverSystem.add_point_2d(self, u: float, v: float, wp: Entity) -> Entity {#solversystem-add_point_2d}

Add a 2D point to specific work plane (`wp`) then return the handle.

Where `u`, `v` are corresponded to the value of U, V axis on the work plane.

### SolverSystem.add_point_3d(self, x: float, y: float, z: float) -> Entity {#solversystem-add_point_3d}

Add a 3D point then return the handle.

Where `x`, `y`, `z` are corresponded to the value of X, Y, Z axis.

### SolverSystem.add_normal_2d(self, wp: Entity) -> Entity {#solversystem-add_normal_2d}

Add a 2D normal orthogonal to specific work plane (`wp`) then return the handle.

### SolverSystem.add_normal_3d(self, qw: float, qx: float, qy: float, qz: float) -> Entity {#solversystem-add_normal_3d}

Add a 3D normal from quaternion then return the handle.

Where `qw`, `qx`, `qy`, `qz` are corresponded to the W, X, Y, Z value of quaternion.

### SolverSystem.add_distance(self, d: float, wp: Entity) -> Entity {#solversystem-add_distance}

Add a distance to specific work plane (`wp`) then return the handle.

Where `d` is distance value.

### SolverSystem.add_line_2d(self, p1: Entity, p2: Entity, wp: Entity) -> Entity {#solversystem-add_line_2d}

Add a 2D line to specific work plane (`wp`) then return the handle.

Where `p1` is the start point;
`p2` is the end point.

### SolverSystem.add_line_3d(self, p1: Entity, p2: Entity) -> Entity {#solversystem-add_line_3d}

Add a 3D line then return the handle.

Where `p1` is the start point;
`p2` is the end point.

### SolverSystem.add_cubic(self, p1: Entity, p2: Entity, p3: Entity, p4: Entity, wp: Entity) -> Entity {#solversystem-add_cubic}

Add a cubic curve to specific work plane (`wp`) then return the handle.

Where `p1` to `p4` is the control points.

### SolverSystem.add_arc(self, nm: Entity, ct: Entity, start: Entity, end: Entity, wp: Entity) -> Entity {#solversystem-add_arc}

Add an arc to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`start` is the start point;
`end` is the end point.

### SolverSystem.add_circle(self, nm: Entity, ct: Entity, radius: Entity, wp: Entity) -> Entity {#solversystem-add_circle}

Add an circle to specific work plane (`wp`) then return the handle.

Where `nm` is the orthogonal normal;
`ct` is the center point;
`radius` is the distance value represent radius.

### SolverSystem.add_work_plane(self, origin: Entity, nm: Entity) -> Entity {#solversystem-add_work_plane}

Add a work plane then return the handle.

Where `origin` is the origin point of the plane;
`nm` is the orthogonal normal.

### SolverSystem.add_constraint(self, c_type: Constraint, wp: Entity, v: float, p1: Entity, p2: Entity, e1: Entity, e2: Entity, e3: Entity = Entity.NONE, e4: Entity = Entity.NONE, other: int = 0, other2: int = 0) -> None {#solversystem-add_constraint}

Add a constraint by type code `c_type`.
This is an origin function mapping to different constraint methods.

Where `wp` represents work plane; `v` represents constraint value;
`p1` and `p2` represent point entities; `e1` to `e4` represent other types of entity;
`other` and `other2` are control options of the constraint.

### SolverSystem.coincident(self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D) -> None {#solversystem-coincident}

Coincident two entities.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |
| [is_point] | [is_circle] | Optional |

### SolverSystem.distance(self, e1: Entity, e2: Entity, value: float, wp: Entity = Entity.FREE_IN_3D) -> None {#solversystem-distance}

Distance constraint between two entities.

If `value` is equal to zero, then turn into [coincident](#solversystem-coincident)

| Entity 1 (`e1`) | Entity 2 (`e2`) | Work plane (`wp`) |
|:---------------:|:---------------:|:-----------------:|
| [is_point] | [is_point] | Optional |
| [is_point] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point] | [is_line] | Optional |

### SolverSystem.equal(self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D) -> None {#solversystem-equal}

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

### SolverSystem.equal_included_angle(self, e1: Entity, e2: Entity, e3: Entity, e4: Entity, wp: Entity) -> None {#solversystem-equal_included_angle}

Constraint that 2D line 1 (`e1`) and line 2 (`e2`), line 3 (`e3`) and line 4 (`e4`)
must have same included angle on work plane `wp`.

### SolverSystem.equal_point_to_line(self, e1: Entity, e2: Entity, e3: Entity, e4: Entity, wp: Entity) -> None {#solversystem-equal_point_to_line}

Constraint that point 1 (`e1`) and line 1 (`e2`), point 2 (`e3`) and line 2  (`e4`)
must have same distance on work plane `wp`.

### SolverSystem.ratio(self, e1: Entity, e2: Entity, value: float, wp: Entity) -> None {#solversystem-ratio}

The ratio (`value`) constraint between two 2D lines (`e1` and `e2`).

### SolverSystem.symmetric(self, e1: Entity, e2: Entity, e3: Entity = Entity.NONE, wp: Entity = Entity.FREE_IN_3D) -> None {#solversystem-symmetric}

Symmetric constraint between two points.

| Entity 1 (`e1`) | Entity 2 (`e2`) | Entity 3 (`e3`) | Work plane (`wp`) |
|:---------------:|:---------------:|:---------------:|:-----------------:|
| [is_point_3d] | [is_point_3d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_work_plane] | [Entity.FREE_IN_3D] |
| [is_point_2d] | [is_point_2d] | [is_line_2d] | Is not [Entity.FREE_IN_3D] |

### SolverSystem.symmetric_h(self, e1: Entity, e2: Entity, wp: Entity) -> None {#solversystem-symmetric_h}

Symmetric constraint between two 2D points (`e1` and `e2`)
with horizontal line on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

### SolverSystem.symmetric_v(self, e1: Entity, e2: Entity, wp: Entity) -> None {#solversystem-symmetric_v}

Symmetric constraint between two 2D points (`e1` and `e2`)
with vertical line on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

### SolverSystem.midpoint(self, e1: Entity, e2: Entity, wp: Entity = Entity.FREE_IN_3D) -> None {#solversystem-midpoint}

Midpoint constraint between a point (`e1`) and a line (`e2`) on work plane (`wp`).

### SolverSystem.horizontal(self, e1: Entity, wp: Entity) -> None {#solversystem-horizontal}

Horizontal constraint of a 2d point (`e1`) on work plane (`wp` can not be [Entity.FREE_IN_3D]).

### SolverSystem.vertical(self, e1: Entity, wp: Entity) -> None {#solversystem-vertical}

Vertical constraint of a 2d point (`e1`) on work plane (`wp` can not be [Entity.FREE_IN_3D]).

### SolverSystem.diameter(self, e1: Entity, value: float, wp: Entity) -> None {#solversystem-diameter}

Diameter (`value`) constraint of a circular entities.

| Entity 1 (`e1`) | Work plane (`wp`) |
|:---------------:|:-----------------:|
| [is_arc] | Optional |
| [is_circle] | Optional |

### SolverSystem.same_orientation(self, e1: Entity, e2: Entity) -> None {#solversystem-same_orientation}

Equal orientation constraint between two 3d normals (`e1` and `e2`).

### SolverSystem.angle(self, e1: Entity, e2: Entity, value: float, wp: Entity, inverse: bool = False) -> None {#solversystem-angle}

Degrees angle (`value`) constraint between two 2d lines (`e1` and `e2`)
on the work plane (`wp` can not be [Entity.FREE_IN_3D]).

# TODO:

[Entity.FREE_IN_3D]: #entity-free_in_3d

[is_point]: #entity-is_point
[is_point_2d]: #entity-is_point_2d
[is_point_3d]: #entity-is_point_3d
[is_work_plane]: #entity-is_work_plane
[is_line]: #entity-is_line
[is_line_2d]: #entity-is_line_2d
[is_arc]: #entity-is_arc
[is_circle]: #entity-is_circle
