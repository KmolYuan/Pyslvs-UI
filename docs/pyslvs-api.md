# Pyslvs API

## Namespace

The namespace of Pyslvs is `pyslvs`.

The modules are:

+ [`atlas`](#module-atlas)
+ [`bfgs`](#module-bfgs)
+ [`collection`](#module-collection)
+ [`example`](#module-example)
+ [`expression`](#module-expression)
+ [`expression_parser`](#module-expression_parser)
+ [`graph`](#module-graph)
+ [`graph_layout`](#module-graph_layout)
+ [`number`](#module-number)
+ [`planar_check`](#module-planar_check)
+ [`planar_linkage`](#module-planar_check)
+ [`tinycadlib`](#module-tinycadlib)
+ [`triangulation`](#module-triangulation)
+ [`utility`](#module-utility)

## Module `atlas`

### conventional_graph()

| cg_list | c_j_list | no_degenerate | stop_func | return |
|:-------:|:--------:|:-------------:|:---------:|:------:|
| List\[[Graph]] | Sequence[int] | int | Optional[Callable[[], bool]] | List\[[Graph]] |
| | | | None | |

Generate conventional graphs by contracted graphs `cg_list` and
contracted link assortment `c_j_list`.

The degenerate setting `no_degenerate` has following option:

+ `0`: No degenerate.
+ `1`: Only degenerate.
+ Else: All graphs.

The check stop function `stop_func` object for GUI or subprocess,
return `True` to terminate this function.

### contracted_graph()

| link_num | stop_func | return |
|:--------:|:---------:|:------:|
| Sequence[int] | Optional[Callable[[], bool]] | List\[[Graph]] |
| | None | |

Generate contracted graphs by link assortment `link_num`.

The check stop function `stop_func` object for GUI or subprocess,
return `True` to terminate this function.

## Module `bfgs`

### SolverSystem

| type | inherit |
|:----:|:-------:|
| type | object |

Sketch Solve solver.

!!! note

    The object attributes of such type are unable to access.

### SolverSystem.\_\_init__()

| self | vpoints | inputs | data_dict | return |
|:----:|:-------:|:------:|:---------:|:------:|
| | Sequence\[[VPoint]] | Optional[Dict[Tuple[int, int], float]] | Optional\[Dict\[Union[int, Tuple[int, int]], Union\[[Coordinate], float]]] | None |
| | | None | None | |

The expression `vpoints` solver function of BFGS method by
giving the input pairs `inputs` and link length `data_dict` requirements.

!!! note

    The format of input pairs:

    + Revolut joints: `{(base, driver): angle}`
    + Slider joints: `{(base, base): offset}`

The format of `data_dict`:

+ Specific coordinates: Dict\[int, [Coordinate]]
+ Specific link length: Dict\[Tuple[int, int], float]

The `data_dict` parameter will reformat its keys into `frozenset` type.

#### SolverSystem.show_inputs()

| self | return |
|:----:|:------:|
| | FrozenSet[Tuple[int, int]] |

Show the current input pairs keys from original constructor.

#### SolverSystem.show_data()

| self | return |
|:----:|:------:|
| | FrozenSet[Union[int, Tuple[int, int]]] |

Show the current keys of `data_dict` parameter from original constructor.

#### SolverSystem.set_inputs()

| self | inputs | return |
|:----:|:------:|:------:|
| | Dict[Tuple[int, int], float] | None |

Set the values of `inputs` parameter from original constructor.
Two groups of `dict` keys must be the same or subset.

#### SolverSystem.set_data()

| self | data_dict | return |
|:----:|:------:|:------:|
| | Dict[Union[int, Tuple[int, int]], Union[Coordinate, float]] | None |

Set the values of `data_dict` parameter from original constructor.
Two groups of `dict` keys must be the same or subset.

#### SolverSystem.solve()

| self | return |
|:----:|:------:|
| | List[Union[Tuple[float, float] Tuple[Tuple[float, float], Tuple[float, float]]]] |

Solve the conditions and return the result, raise ValueError if not succeeded.
The joint position will returned by its index correspondingly.

+ Revolut joints: Tuple[float, float]
+ Slider joints: Tuple[Tuple[float, float], Tuple[float, float]]

## Module `collection`

### collection_list

| type |
|:----:|
| Dict[str, Dict[str, Any]] |

The example data of collections.

The format of each configuration is:

+ `Expression`: Mechanism expression of the structure.
    + type: str
+ `input`: [Input pairs].
    + type: Sequence[Tuple[int, int]]
+ `Graph`: The generalized chain graph in edge set.
    + type: Sequence[Tuple[int, int]]
+ `Placement`: The grounded joints setting. (`x`, `y`, `r`)
    + type: Dict[int, Optional[Tuple[float, float, float]]]
+ `Target`: The target joints settings.
    + type: Dict[int, Optional[Sequence[Tuple[float, float]]]]
+ `cus`: The custom joints on specific link. (link number correspond to the graph expression.)
    + type: Dict[int, int]
+ `same`: The multiple joints setting.
    + type: Dict[int, int]

## Module `efd`

### efd_fitting

| path | n | return |
|:----:|:---:|:----:|
| Sequence[Tuple[float, float]] | int | ndarray |

Curve fitting using Elliptical Fourier Descriptor.

The path `path` will be translate to Fourier descriptor coefficients,
then regenerate a new paths as a `n` x 4 NumPy array.

## Module `example`

### example_list

| type |
|:----:|
| Dict[str, Tuple[str, Sequence[Tuple[int, int]]]] |

The example data of mechanisms.

The format of each mechanism is:

+ `[0]`: Mechanism expression.
    + type: str
+ `[1]`: [Input pairs].
    + type: Tuple[Tuple[int, int], ...]]

## Module `expression`

### get_vlinks()

| vpoints | return |
|:-------:|:------:|
| Iterable\[[VPoint]] | List\[[VLink]] |

Get VLinks from a list of VPoint `vpoints`.

### Coordinate

| type | inherit |
|:----:|:-------:|
| type | object |

A data class used to store coordinates.

#### Object attributes of Coordinate

| name | type | description |
|:----:|:----:|:------------|
| x | float | The x value of [Coordinate] class. |
| y | float | The y value of [Coordinate] class. |

#### Coordinate.\_\_init__()

| self | x | y |
|:----:|:---:|:---:|
| | float | float |

The constructor of [Coordinate] class.

#### Coordinate.distance()

| self | p | return |
|:----:|:---:|:----:|
| | [Coordinate] | float |

Return the distance between two [Coordinate] objects.

#### Coordinate.is_nan()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the coordinate value is not a number.

#### Coordinate.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

### VJoint

| type | inherit |
|:----:|:-------:|
| type | IntEnum |

Enumeration values of Joint types.

### VPoint

| type | inherit |
|:----:|:-------:|
| type | object |

Mechanism expression class.

#### Class attributes of VPoint

| name | type | description |
|:----:|:----:|:------------|
| HOLDER | [VPoint] | A placeholder of VPoint type. |

#### Object attributes of VPoint

| name | type | description |
|:----:|:----:|:------------|
| links | Sequence[str] | Link list of the joint. |
| c | Tuple[Tuple[float, float], Tuple[float, float]] | Current coordinates of the joint. |
| type | [VJoint] | The type of the joint. |
| type_str | str | The type string of the joint. |
| color | Optional[Tuple[int, int, int]] | The RGB color data of the joint. |
| color_str | str | The color string of the joint. |
| x | float | The original x value of the joint. |
| y | float | The original y value of the joint. |
| angle | float | The slider slot angle value of the joint. |

#### VPoint.\_\_init__()

| self | links | type_int | angle | color_str | x | y | color_func | return |
|:----:|:-----:|:--------:|:-----:|:---------:|:---:|:---:|:------:|:------:|
| | Iterable[str] | [VJoint] | float | str | float | float | Optional[Callable[[str], Tuple[int, int, int]] | None |
| | | | | | | | None | |

The attributes will match to the object attributes of [VPoint] objects.

Where the color function `color_func` needs to transform the color string `color_str` into RGB format.
If color information is not needed, the `color_func` can be `None`.

!!! note

    Some of the attributes are not work in some of the joint types.

#### VPoint.r_joint()

`@staticmethod`

| links | x | y | return |
|:-----:|:---:|:---:|:---:|
| Iterable[str] | float | float | [VPoint] |

A fast constructor of revolut joints.

#### VPoint.slider_joint()

`@staticmethod`

| links | type_int | angle | x | y | return |
|:-----:|:--------:|:-----:|:---:|:---:|:---:|
| Iterable[str] | [VJoint] | float | float | float | [VPoint] |

A fast constructor of slider joints.

#### VPoint.copy()

| self | return |
|:----:|:------:|
| | [VPoint] |

The copy method of the [VPoint] object.

#### VPoint.cx()

`@property`

| self | return |
|:----:|:------:|
| | float |

X value of current coordinate.
If it's slider, the pin coordinate will be returned.

#### VPoint.cy()

`@property`

| self | return |
|:----:|:------:|
| | float |

Y value of current coordinate.
If it's slider, the pin coordinate will be returned.

#### VPoint.set_links()

| self | links | return |
|:----:|:-----:|:------:|
| | Iterable[str] | None |

The update function of links attribute.

#### VPoint.replace_link()

| self | link1 | link2 | return |
|:----:|:-----:|:-----:|:------:|
| | str | str | None |

Replace the value in links attribute.

#### VPoint.move()

| self | c1 | c2 | return |
|:----:|:---:|:---:|:----:|
| | Tuple[float, float] | Optional[Tuple[float, float]] | None |
| | | None | |

The update function of current coordinate(s).
The 2nd placement is the pin coordinate of slider joints.

If there is only one argument for a slider joint,
the slot and pin coordinates will be set to the same position.

#### VPoint.locate()

| self | x | y | return |
|:----:|:---:|:---:|:----:|
| | float | float | None |

The update function of original coordinate.
It will call `self.move((x, y))` after set the position.

#### VPoint.rotate()

| self | angle | return |
|:----:|:-----:|:----:|
| | float | None |

The update function of angle attribute.

#### VPoint.set_offset()

| self | offset | return |
|:----:|:-----:|:----:|
| | float | None |

The update function of slider offset.
It will also enable offset value after called.

#### VPoint.disable_offset()

| self | return |
|:----:|:------:|
| | None |

Disable offset setting of the joint.

#### VPoint.distance()

| self | p | return |
|:----:|:---:|:----:|
| | [VPoint] | float |

Return the distance between two [VPoint] objects.

#### VPoint.has_offset()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the offset setting is enabled.

#### VPoint.offset()

| self | return |
|:----:|:------:|
| | float |

Return the offset constraint value of the joint.

#### VPoint.true_offset()

| self | return |
|:----:|:------:|
| | float |

Return the current offset value of the joint.

#### VPoint.slope_angle()

| self | p | num1 | num2 | return |
|:----:|:---:|:---:|:---:|:------:|
| | [VPoint] | int | int | float |
| | | 2 | 2 | |

Return the value `hypot(p_x - m_x, p_y - m_y)`,
where `m_x`, `m_y` is the value of the joint,
and `p_x`, `p_y` is the value of `p`.

The option `num1` and `num2` is the position of current coordinate attribute.

#### VPoint.grounded()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the joint is connected to ground link.

#### VPoint.pin_grounded()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the joint pin is connected to ground link.

#### VPoint.same_link()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the point is at the same link.

#### VPoint.no_link()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if there is no any link in links attribute.

#### VPoint.is_slot_link()

| self | link_name | return |
|:----:|:---------:|:------:|
| | str | bool |

Return `True` if the slot is on the link `link_name`.

#### VPoint.expr()

| self | return |
|:----:|:------:|
| | str |

Return the literal mechanism expression of the joint.

#### VPoint.\_\_getitem__()

| self | i | return |
|:----:|:---:|:------:|
| | int | float |

Implement `x, y = self` or `x = self[0]` in Python script.

#### VPoint.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

### VLink

| type | inherit |
|:----:|:-------:|
| type | object |

Mechanism expression class in link's view.

#### Class attributes of VLink

| name | type | description |
|:----:|:----:|:------------|
| HOLDER | [VLink] | A placeholder of VLink type. |
| FRAME | str | The name of frame. ("ground") |

#### Object attributes of VLink

| name | type | description |
|:----:|:----:|:------------|
| name | str | The name tag of the link. |
| color | Optional[Tuple[int, int, int]] | The RGB color data of the joint. |
| color_str | str | The color string of the joint. |
| points | Sequence[int] | The points of the link. |

#### VLink.\_\_init__()

| self | name | color_str | points | color_func | return |
|:----:|:----:|:---------:|:------:|:----------:|:------:|
| | str | str | Iterable[int] | Optional[Callable[[str], Tuple[int, int, int]]] | None |
| | | | | None | |

The attributes will match to the object attributes of [VLink] objects.

Where the color function `color_func` needs to transform the color string `color_str` into RGB format.
If color information is not needed, the `color_func` can be `None`.

#### VLink.set_points()

| self | points | return |
|:----:|:------:|:------:|
| | Iterable[int] | None |

The update function of points attribute.

#### VLink.\_\_contains__()

| self | point | return |
|:----:|:-----:|:------:|
| | int | bool |

Implement `point in self` in Python script.
Return `True` if `point` is in the points attribute.

#### VLink.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

## Module `expression_parser`

### color_names

| type |
|:----:|
| Tuple[str, ...] |

The object contains all of supported colors in string format.

### color_rgb()

| name | return |
|:----:|:------:|
| str | Tuple[int, int, int] |

Get RGB color data by name, return `(0, 0, 0)` if it is invalid.

Also support `"(R, G, B)"` string format.

### parse_params()

| expr | return |
|:----:|:------:|
| str | List[List[Union[str, float]]] |

Parse mechanism expression into [VPoint] constructor arguments.

### parse_pos()

| expr | return |
|:----:|:------:|
| str | List[Tuple[float, float]] |

Parse mechanism expression into coordinates.

### parse_vpoints()

| expr | return |
|:----:|:------:|
| str | List\[[VPoint]] |

Parse mechanism expression into [VPoint] objects.

### parse_vlinks()

| expr | return |
|:----:|:------:|
| str | List\[[VLink]] |

Parse mechanism expression into [VLink] objects.

### edges_view()

| graph | return |
|:-----:|:------:|
| [Graph] | Iterator[Tuple[int, Tuple[int, int]]] |

The iterator will yield the sorted edges from `graph`.

### graph2vpoints()

| graph | pos | cus | same | grounded | return |
|:-----:|:---:|:---:|:----:|:--------:|:------:|
| [Graph] | Dict[int, Tuple[float, float]] | Optional[Dict[int, int]] | Optional[Dict[int, int]] | Optional[int] | List\[[VPoint]] |
| | | None | None | None | |

Transform `graph` into [VPoint] objects. The vertices are mapped to links.

+ `pos`: Position for each vertices.
+ `cus`: Extra points on the specific links.
+ `same`: Multiple joint setting. The joints are according to [`edges_view`](#edges_view).
+ `grounded`: The ground link of vertices.

## Module `graph`

### link_assortment()

| g | return |
|:---:|:----:|
| [Graph] | List[int] |

Return link assortment of the graph.

### contracted_link_assortment()

| g | return |
|:---:|:----:|
| [Graph] | List[int] |

Return contracted link assortment of the graph.

### labeled_enumerate()

| g | return |
|:---:|:----:|
| [Graph] | List[Tuple[int, Graph]] |

Enumerate each node with labeled except isomorphism.

### Graph

| type | inherit |
|:----:|:-------:|
| type | object |

The undirected graph class, support multigraph.

#### Object attributes of Graph

| name | type | description |
|:----:|:----:|:------------|
| edges | Tuple[Tuple[int, int], ...] | The edges of the graph. |
| vertices | Tuple[int, ...] | The vertices of the graph. |

#### Graph.\_\_init__()

| self | edges | return |
|:----:|:-----:|:------:|
| | Iterable[Tuple[int, int]] | None |

Input edges of the graph. The vertices symbols are positive continuously integer.

#### Graph.add_edge()

| self | n1 | n2 | return |
|:----:|:---:|:---:|:----:|
| | int | int | None |

Add edge `n1` to `n2`.

#### Graph.add_vertices()

| self | vertices | return |
|:----:|:-----:|:----:|
| | Iterable[int] | None |

Add vertices from iterable object `vertices`.

#### Graph.dof()

| self | return |
|:----:|:------:|
| | int |

Return DOF of the graph.

!!! Note

    DOF is the Degree of Freedoms to a mechanism.

    In the [Graph] objects, all vertices will assumed as revolut joints (1 DOF).

    $$
    F = 3(N_L - 1) - 2N_J
    $$

#### Graph.neighbors()

| self | n | return |
|:----:|:---:|:----:|
| | int | Tuple[int, ...] |

Return the neighbors of the vertex `n`.

#### Graph.degrees()

| self | return |
|:----:|:------:|
| | Dict[int, int] |

Return the degrees of each vertex.

#### Graph.degree_code()

| self | return |
|:----:|:------:|
| | int |

Generate a degree code.

With a sorted vertices mapping by the degrees of each vertex,
regenerate a new adjacency matrix.
A binary code can be found by concatenating the upper right elements.
The degree code is the maximum value of the permutation.

#### Graph.adjacency_matrix()

| self | return |
|:----:|:------:|
| | ndarray |

Generate a adjacency matrix.

Assume the matrix $A[i, j] = A[j, i]$.
Where $A[i, j] = 1$ if edge `(i, j)` exist.

#### Graph.is_connected()

| self | without | return |
|:----:|:--------:|:------:|
| | int | bool |
| | -1 | |

Return `True` if the graph is connected.
Set the argument `without` to ignore one vertex.

#### Graph.has_cut_link()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the graph has cut-link.

#### Graph.is_degenerate()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the graph is degenerate.

#### Graph.is_isomorphic()

| self | graph | return |
|:----:|:-----:|:------:|
| | [Graph] | bool |

Return `True` if the graph is isomorphic to `graph`.
Default is using VF2 algorithm.

#### Graph.is_isomorphic_vf2()

| self | graph | return |
|:----:|:-----:|:------:|
| | [Graph] | bool |

Return `True` if the graph is isomorphic to `graph`.
Compare with VF2 algorithm, one of the high performance isomorphic algorithms.

#### Graph.is_isomorphic_degree_code()

| self | graph | return |
|:----:|:-----:|:------:|
| | [Graph] | bool |

Return `True` if the graph is isomorphic to `graph`.
Compare with degree code algorithm.

+ <https://doi.org/10.1115/1.2919236>

#### Graph.duplicate()

| self | vertices | return |
|:----:|:-----:|:----:|
| | Iterable[int] | [Graph] |

Make the graph duplicate specific vertices (from `vertices`). Return a new graph.

#### Graph.copy()

| self | return |
|:----:|:------:|
| | [Graph] |

The copy method of the [Graph] object.

## Module `graph_layout`

### external_loop_layout()

| graph | node_mode | scale | return |
|:-----:|:---------:|:-----:|:------:|
| [Graph] | bool | float | Dict[int, Tuple[float, float]] |
| | | 1. | |

Return the layout position decided by external loop.

Argument `node_mode` will transform edges into vertices.

Argument `scale` will resize the position by scale factor.

## Module `number`

### link_synthesis()

| nl | nj | stop_func | return |
|:---:|:---:|:-------:|:------:|
| int | int | Optional[Callable[[], bool]] | List[Tuple[int, ...]] |
| | | None | |

Return link assortment by number of links `nl` and number of joints `nj`.

The check stop function `stop_func` object for GUI or subprocess,
return `True` to terminate this function.

### contracted_link_synthesis()

| link_num_list | stop_func | return |
|:-------------:|:---------:|:------:|
| Sequence[int] | Optional[Callable[[], bool]] | List[Tuple[int, ...]] |
| | None | |

Return contracted link assortment by link assortment `link_num_list`.

The check stop function `stop_func` object for GUI or subprocess,
return `True` to terminate this function.

## Module `planar_check`

### is_planar()

| g | return |
|:---:|:----:|
| [Graph] | bool |

Return `True` if graph `g` is a planar graph.

## Module `planar_linkage`

### Planar

| type | inherit |
|:----:|:-------:|
| type | [Objective] |

#### Planar.\_\_init__()

| self | mech_params | return |
|:----:|:-----------:|:------:|
| | Dict[str, Any] | None |

The constructor of objective object.

Options of `mech_params`:

+ `Expression`: The mechanism expression of the structure.
    + type: List\[[VPoint]]
+ `input`: [Input pairs].
    + type: List[Tuple[int, int]]
+ `Placement`: The grounded joints setting. (`x`, `y`, `r`)
    + type: Dict[int, Tuple[float, float, float]]
+ `Target`: The target path.
    + type: Dict[int, Sequence[Tuple[float, float]]]
+ `same`: Multiple joint setting. The joints are according to [`edges_view`](#edges_view).
    + type: Dict[int, int]
+ `upper`: The upper setting of variables, the length must same as variable array.
    + type: List[float]
+ `lower`: The lower setting of variables, the length must same as variable array.
    + type: List[float]

Variable array:

| | Placement | Link length | Inputs |
|:---:|:-----:|:-----------:|:------:|
| `v =` | `x0`, `y0`, ... | `l0`, `l1`, ... | `a00`, `a01`, ..., `a10`, `a11`, ... |

In 1D array: `v = [x0, y0, ..., l0, l1, ..., a00, a01, ..., a10, a11, ...]`

#### Planar.is_two_kernel()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the solving method is two kernel.

#### Planar.result()

| self | v | return |
|:----:|:---:|:----:|
| | numpy.ndarray | str |

Input a generic data (variable array), return the mechanism expression.

## Module `tinycadlib`

### plap()

| c1 | d0 | a0 | c2 | inverse | return |
|:---:|:---:|:---:|:---:|:---:|:------:|
| [Coordinate] | float | float | Optional\[[Coordinate]] | bool | [Coordinate] |
| | | | None | False | |

The PLAP function requires two points, one distance and one angle, obtained the position of thrid point.
The unit of `a0` is degree.

In the following picture, `c1` correspond to "A", `c2` correspond to "B", `d0` correspond to "L0",
`a0` correspond to "beta", `return` correspond to "C". If `c2` is not given, "alpha" will be set to zero.

![PLAP](img/PLAP.png)

Set `inverse` option to `True` can make `a0` value as negative.

### pllp()

| c1 | d0 | d1 | c2 | inverse | return |
|:---:|:---:|:---:|:---:|:---:|:------:|
| [Coordinate] | float | float | [Coordinate] | bool | [Coordinate] |
| | | | | False | |

The PLLP function requires two points and two distances, obtained the position of thrid point.

In the following picture, `c1` correspond to "A", `c2` correspond to "B", `d0` correspond to "L0",
`d1` correspond to "L1", `return` correspond to "C".

![PLLP](img/PLLP.png)

Set `inverse` option to `True` can make the result upside down.

### plpp()

| c1 | d0 | c2 | c3 | inverse | return |
|:---:|:---:|:---:|:---:|:---:|:------:|
| [Coordinate] | float | [Coordinate] | [Coordinate] | bool | [Coordinate] |
| | | | | False | |

The PLLP function requires three points and one distance, obtained the position of fourth point.

In the following picture, `c1` correspond to "A", `c2` correspond to "B", `c3` correspond to "C",
`d0` correspond to "L0", `return` correspond to "D".

![PLPP](img/PLPP.png)

Set `inverse` option to `True` can make the result to the another side between `c1` and line `c2` `c3`.

### pxy()

| c1 | d0 | d1 | return |
|:---:|:---:|:---:|:---:|
| [Coordinate] | float | float | [Coordinate] |

The PXY function requires one point and offset values, obtained the position of second point.

In the following picture, `c1` correspond to "A", `d0` correspond to "X",
`d1` correspond to "Y", `return` correspond to "B", the sign of value are correspond to coordinate system.

![PXY](img/PXY.png)

### vpoint_dof()

| vpoints | return |
|:-------:|:------:|
| Sequence\[[VPoint]] | int |

Return the DOF of the mechanism expression `vpoints`.

### expr_parser()

| exprs | data_dict | return |
|:-----:|:---------:|:------:|
| Sequence[Tuple[str, ...]] | Dict[str, float] | None |

Solve and update information of the triangle expression `exprs` to `data_dict`.
The argument `exprs` can be obtained by [`vpoints_configure`](#vpoints_configure) and [`ExpressionStack.as_list()`](#expressionstackas_list) method.

This function is already included in [`expr_solving`](#expr_solving), not recommended for direct use.

### data_collecting()

| exprs | mapping | vpoints_ | return |
|:-----:|:-------:|:--------:|:------:|
| [ExpressionStack] | Dict[int, str] | Sequence\[[VPoint]] | Tuple\[Dict\[str, Union\[[Coordinate], float]], int] |

Data transform function of Triangular method.

The triangle expression stack `expr` is generated from [`vpoints_configure`](#vpoints_configure).

The information data `mapping` map the symbols to the indicator of `vpoints_`.

This function is already included in [`expr_solving`](#expr_solving), not recommended for direct use.

### expr_solving()

| exprs | mapping | vpoints | angles | return |
|:-----:|:-------:|:-------:|:------:|:------:|
| [ExpressionStack] | Dict[Union[int, Tuple[int, int]], Union[str, float]] | Sequence\[[VPoint]] | Optional[Sequence[float]] | List[Union[Tuple[float, float], Tuple[Tuple[float, float], Tuple[float, float]]]] |
| | | | None | |

Solver function of Triangular method and BFGS method, for mechanism expression `vpoints`.

The triangle expression stack `expr` is generated from [`vpoints_configure`](#vpoints_configure).

The information data `mapping` map the symbols to the indicator of `vpoints`,
additionally has a same format as argument `data_dict` in [SolverSystem].

Solver function will not handle slider input pairs in argument `angles`, which is only support revolut joints.
In another way, the slider input pairs can be set by [`VPoint.disable_offset()`](#vpointdisable_offset) method.

## Module `triangulation`

### ExpressionStack

| type | inherit |
|:----:|:-------:|
| type | object |

Triangle solution stack, generated from [`vpoints_configure`](#vpoints_configure).
It is pointless to call the constructor.

#### ExpressionStack.as_list()

| self | return |
|:----:|:------:|
| | List[Tuple[str, ...]] |

Copy the dataset as list object.

#### ExpressionStack.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

### vpoints_configure()

| vpoints_ | inputs | status | return |
|:--------:|:------:|:------:|:------:|
| Sequence\[[VPoint]] | Sequence[Tuple[int, int]] | Optional[Dict[int, bool]] | ExpressionStack |
| | | None | |

Generate the Triangle solution stack by mechanism expression `vpoints_`.

The argument `inputs` is a list of input pairs.

The argument `status` will track the configuration of each point, which is optional.

## Module `utility`

### Objective

| type | inherit |
|:----:|:-------:|
| type | object |

Objective function base class.
It is used to build the objective function for Metaheuristic Random Algorithms.
See the sections of [metaheuristics API](metaheuristics-api.md).

#### Objective.fitness()

**Cython `cdef` method**

`@abstractmethod`

| self | v | return |
|:----:|:---:|:----:|
| | numpy.ndarray | double |

Return the fitness from the variable list `v`.
This function will be directly called in the algorithms.

#### Objective.result()

`@abstractmethod`

| self | v | return |
|:----:|:---:|:----:|
| | numpy.ndarray | Any |

Return the result from the variable list `v`.

### AlgorithmBase

| type | inherit |
|:----:|:-------:|
| type | object |

Algorithm base class.
It is used to build the Metaheuristic Random Algorithms.
See the sections of [metaheuristics API](metaheuristics-api.md).

#### AlgorithmBase.\_\_init__()

| self | func | settings | progress_fun | interrupt_fun | return |
|:----:|:----:|:--------:|:------------:|:-------------:|:------:|
| | [Objective] | Dict[str, Any] | Optional[Callable[[int, str], None]] | Optional[Callable[[], bool]] | None |
| | | | None | None | |

The argument `func` is a object inherit from [Objective],
and all abstract methods should be implemented.

The format of argument `settings` can be customized.

The argument `progress_fun` will be called when update progress,
and the argument `interrupt_fun` will check the interrupt status from GUI or subprocess.

#### AlgorithmBase.run()

| self | return |
|:----:|:------:|
| | Tuple[Any, List[Tuple[int, float, float]]] |

Run and return the result and convergence history.

The first place of `return` is came from calling [`Objective.result()`](#objectiveresult).

The second place of `return` is a list of generation data,
which type is `Tuple[int, float, float]]`.
The first of them is generation,
the second is fitness, and the last one is time in second.

[SolverSystem]: #solversystem
[Coordinate]: #coordinate
[VJoint]: #vjoint
[VPoint]: #vpoint
[VLink]: #vlink
[Graph]: #graph
[Objective]: #objective
[ExpressionStack]: #expressionstack
