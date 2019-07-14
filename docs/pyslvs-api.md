# Namespace

The namespace of Pyslvs is `pyslvs`.

The modules are:

+ `atlas`
+ `bfgs`
+ `collection`
+ `example`
+ `expression`
+ `expression_parser`
+ `graph`
+ `graph_layout`
+ `number`
+ `planar_check`
+ `planar_linkage`
+ `sketch_solve`
+ `tinycadlib`
+ `triangulation`
+ `verify`

# atlas

## conventional_graph()

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

## contracted_graph()

| link_num | stop_func | return |
|:--------:|:---------:|:------:|
| Sequence[int] | Optional[Callable[[], bool]] | List\[[Graph]] |
| | None | |

Generate contracted graphs by link assortment `link_num`.

The check stop function `stop_func` object for GUI or subprocess,
return `True` to terminate this function.

# bfgs

## vpoint_solving()

| vpoints | inputs | data_dict | return |
|:-------:|:------:|:---------:|:------:|
| Sequence\[[VPoint]] | Optional[Dict[Tuple[int, int], float]] | Optional\[Dict\[Union[int, Tuple[int, int]], Union\[[Coordinate], float]]] | List[Union[Tuple[float, float] Tuple[Tuple[float, float], Tuple[float, float]]]] |
| | None | None | |

The expression `vpoints` solver function of BFGS method by
giving the input pairs `inputs` and link length `data_dict` requirements.

!!! note

    The format of input pairs:

    + Revolut joints: `{(base, driver): angle}`
    + Slider joints: `{(base, base): offset}`

The format of `data_dict`:

+ Specific coordinates: Dict\[int, [Coordinate]]
+ Specific link length: Dict\[Tuple[int, int], float]

The joint position will returned by its index correspondingly.

+ Revolut joints: Tuple[float, float]
+ Slider joints: Tuple[Tuple[float, float], Tuple[float, float]]

# collection

## collection_list

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
+ `Placement`: The grounded joints settings.
    + type: Dict[int, Optional[Tuple[float, float, float]]]
+ `Target`: The target joints settings.
    + type: Dict[int, Optional[Sequence[Tuple[float, float]]]]
+ `cus`: The custom joints on specific link. (link number correspond to the graph expression.)
    + type: Dict[int, int]
+ `same`: The multiple joints setting.
    + type: Dict[int, int]

# example

## example_list

| type |
|:----:|
| Dict[str, Tuple[str, Tuple[Tuple[int, int], ...]]] |

The example data of mechanisms.

The format of each mechanism is:

+ `[0]`: Mechanism expression.
    + type: str
+ `[1]`: [Input pairs].
    + type: Tuple[Tuple[int, int], ...]]

# expression

## get_vlinks()

| vpoints | return |
|:-------:|:------:|
| Iterable\[[VPoint]] | List\[[VLink]] |

Get VLinks from a list of VPoint `vpoints`.

## Coordinate

| type | inherit |
|:----:|:-------:|
| type | object |

A data class used to store coordinates.

### Object attributes of Coordinate

| name | type | description |
|:----:|:----:|:------------|
| x | float | The x value of [Coordinate] class. |
| y | float | The y value of [Coordinate] class. |

### Coordinate.\_\_init__()

| self | x | y |
|:----:|:---:|:---:|
| | float | float |

The constructor of [Coordinate] class.

### Coordinate.distance()

| self | p | return |
|:----:|:---:|:----:|
| | [Coordinate] | float |

Return the distance between two [Coordinate] objects.

### Coordinate.is_nan()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the coordinate value is not a number.

### Coordinate.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

## VJoint

| type | inherit |
|:----:|:-------:|
| type | IntEnum |

Enumeration values of Joint types.

## VPoint

| type | inherit |
|:----:|:-------:|
| type | object |

Mechanism expression class.

### Object attributes of VPoint

| name | type | description |
|:----:|:----:|:------------|
| links | Tuple[str, ...] | Link list of the joint. |
| c | numpy.ndarray | Current coordinates of the joint. |
| type | [VJoint] | The type of the joint. |
| type_str | str | The type string of the joint. |
| color | Tuple[int, int, int] | The RGB color data of the joint. |
| color_str | str | The color string of the joint. |
| x | float | The original x value of the joint. |
| y | float | The original y value of the joint. |
| angle | float | The slider slot angle value of the joint. |

### VPoint.\_\_init__()

| self | links | type_int | angle | color_str | x | y | color_func | return |
|:----:|:-----:|:--------:|:-----:|:---------:|:---:|:---:|:------:|:------:|
| | Iterable[str] | [VJoint] | float | str | float | float | Optional[Callable[[str], Tuple[int, int, int]] | None |
| | | | | | | | None | |

The attributes will match to the object attributes of [VPoint] objects.

Where the color function `color_func` needs to transform the color string `color_str` into RGB format.
If color information is not needed, the `color_func` can be `None`.

!!! note

    Some of the attributes are not work in some of the joint types.

### VPoint.r_joint()

`@staticmethod`

| links | x | y | return |
|:-----:|:---:|:---:|:---:|
| Iterable[str] | float | float | [VPoint] |

A fast constructor of revolut joints.

### VPoint.slider_joint()

`@staticmethod`

| links | type_int | angle | x | y | return |
|:-----:|:--------:|:-----:|:---:|:---:|:---:|
| Iterable[str] | [VJoint] | float | float | float | [VPoint] |

A fast constructor of slider joints.

### VPoint.copy()

| self | return |
|:----:|:------:|
| | [VPoint] |

The copy method of the [VPoint] object.

### VPoint.cx()

`@property`

| self | return |
|:----:|:------:|
| | float |

X value of current coordinate.
If it's slider, the pin coordinate will be returned.

### VPoint.cy()

`@property`

| self | return |
|:----:|:------:|
| | float |

Y value of current coordinate.
If it's slider, the pin coordinate will be returned.

### VPoint.set_links()

| self | links | return |
|:----:|:-----:|:------:|
| | Iterable[str] | None |

The update function of links attribute.

### VPoint.replace_link()

| self | link1 | link2 | return |
|:----:|:-----:|:-----:|:------:|
| | str | str | None |

Replace the value in links attribute.

### VPoint.move()

| self | c1 | c2 | return |
|:----:|:---:|:---:|:----:|
| | Tuple[float, float] | Optional[Tuple[float, float]] | None |
| | | None | |

The update function of current coordinate(s).
The 2nd placement is the pin coordinate of slider joints.

If there is only one argument for a slider joint,
the slot and pin coordinates will be set to the same position.

### VPoint.locate()

| self | x | y | return |
|:----:|:---:|:---:|:----:|
| | float | float | None |

The update function of original coordinate.
It will call `self.move((x, y))` after set the position.

### VPoint.rotate()

| self | angle | return |
|:----:|:-----:|:----:|
| | float | None |

The update function of angle attribute.

### VPoint.set_offset()

| self | offset | return |
|:----:|:-----:|:----:|
| | float | None |

The update function of slider offset.
It will also enable offset value after called.

### VPoint.disable_offset()

| self | return |
|:----:|:------:|
| | None |

Disable offset setting of the joint.

### VPoint.distance()

| self | p | return |
|:----:|:---:|:----:|
| | [VPoint] | float |

Return the distance between two [VPoint] objects.

### VPoint.has_offset()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the offset setting is enabled.

### VPoint.offset()

| self | return |
|:----:|:------:|
| | float |

Return the offset constraint value of the joint.

### VPoint.true_offset()

| self | return |
|:----:|:------:|
| | float |

Return the current offset value of the joint.

### VPoint.slope_angle()

| self | p | num1 | num2 | return |
|:----:|:---:|:---:|:---:|:------:|
| | [VPoint] | int | int | float |
| | | 2 | 2 | |

Return the value `hypot(p_x - m_x, p_y - m_y)`,
where `m_x`, `m_y` is the value of the joint,
and `p_x`, `p_y` is the value of `p`.

The option `num1` and `num2` is the position of current coordinate attribute.

### VPoint.grounded()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the joint is connected to ground link.

### VPoint.pin_grounded()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the joint pin is connected to ground link.

### VPoint.same_link()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if the point is at the same link.

### VPoint.no_link()

| self | return |
|:----:|:------:|
| | bool |

Return `True` if there is no any link in links attribute.

### VPoint.is_slot_link()

| self | link_name | return |
|:----:|:---------:|:------:|
| | str | bool |

Return `True` if the slot is on the link `link_name`.

### VPoint.expr()

| self | return |
|:----:|:------:|
| | str |

Return the literal mechanism expression of the joint.

### VPoint.\_\_getitem__()

| self | i | return |
|:----:|:---:|:------:|
| | int | float |

Implement `x, y = self` or `x = self[0]` in Python script.

### VPoint.\_\_repr__()

| self | return |
|:----:|:------:|
| | str |

Over loaded method to print the objects.

## VLink

| type | inherit |
|:----:|:-------:|
| type | object |

Mechanism expression class in link's view.

### Object attributes of VLink

| name | type | description |
|:----:|:----:|:------------|

Under planning.

[input pairs]: #vpoint_solving
[Coordinate]: #coordinate
[VJoint]: #vjoint
[VPoint]: #vpoint
[VLink]: #vlink
[Graph]: #graph
