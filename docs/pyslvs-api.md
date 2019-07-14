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

Under planning.

[input pairs]: #vpoint_solving
[Graph]: #graph
[VPoint]: #vpoint
[Coordinate]: #coordinate
