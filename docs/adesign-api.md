# Adesign API

## Namespace

The namespace of Adesign is included in `pyslvs`.

The modules are:

+ [`de`](#module-de)
+ [`firefly`](#module-firefly)
+ [`rga`](#module-rga)
+ [`verify`](#module-verify)

## Module `de`

### Differential

| type | inherit |
|:----:|:-------:|
| type | object |

The implementation of Differential Evolution algorithm.

#### Differential.\_\_init__()

| self | func | settings | progress_fun | interrupt_fun | return |
|:----:|:----:|:--------:|:------------:|:-------------:|:------:|
| | [Verification] | Dict[str, Any] | Optional[Callable[[int, str], None]] | Optional[Callable[[], bool]] | None |
| | | | None | None | |

The argument `func` is a object inherit from [Verification],
and all abstract methods should be implemented.

The format of argument `settings`:

+ `strategy`: Strategy
    + type: int (0~9)
    + default: 0
+ `NP`: Population
    + type: int
    + default: 400
+ `F`: Weight factor
    + type: float (0.~1.)
    + default: 0.6
+ `CR`: Crossover rate
    + type: float (0.~1.)
    + default: 0.9
+ `max_gen` or `min_fit` or `max_time` or `slow_down`: Limitation of termination
    + type: int / float / float / float
    + default: Raise `ValueError`
+ `report`: Report per generation
    + type: int
    + default: 10

!!! note

    The option `slow_down` is a percent value that
    current fitnesses difference of two generation is divide by last one.

The argument `progress_fun` will be called when update progress,
and the argument `interrupt_fun` will check the interrupt status from GUI or subprocess.

## Module `firefly`

### Firefly

| type | inherit |
|:----:|:-------:|
| type | object |

The implementation of Firefly algorithm.

#### Firefly.\_\_init__()

| self | func | settings | progress_fun | interrupt_fun | return |
|:----:|:----:|:--------:|:------------:|:-------------:|:------:|
| | [Verification] | Dict[str, Any] | Optional[Callable[[int, str], None]] | Optional[Callable[[], bool]] | None |
| | | | None | None | |

The format of argument `settings`:

+ `n`: Population
    + type: int
    + default: 80
+ `alpha`: Alpha factor
    + type: float (0.~1.)
    + default: 0.01
+ `beta_min`: Minimal attraction
    + type: float (0.~1.)
    + default: 0.2
+ `beta0`: Attraction rate
    + type: float (0.~1.)
    + default: 1.
+ `gamma`: Gamma rate
    + type: float (0.~1.)
    + default: 1.
+ `max_gen` or `min_fit` or `max_time`: Limitation of termination
    + type: int / float / float
    + default: Raise `ValueError`
+ `report`: Report per generation
    + type: int
    + default: 10

Others arguments are same as [`Differential.__init__()`](#differential9595init__).

## Module `rga`

### Genetic

| type | inherit |
|:----:|:-------:|
| type | object |

The implementation of Real-coded Genetic Algorithm.

#### Genetic.\_\_init__()

| self | func | settings | progress_fun | interrupt_fun | return |
|:----:|:----:|:--------:|:------------:|:-------------:|:------:|
| | [Verification] | Dict[str, Any] | Optional[Callable[[int, str], None]] | Optional[Callable[[], bool]] | None |
| | | | None | None | |

The format of argument `settings`:

+ `nPop`: Population
    + type: int
    + default: 500
+ `pCross`: Crossover rate
    + type: float (0.~1.)
    + default: 0.95
+ `pMute`: Mutation rate
    + type: float (0.~1.)
    + default: 0.05
+ `pWin`: Win rate
    + type: float (0.~1.)
    + default: 0.95
+ `bDelta`: Delta value
    + type: float
    + default: 5.
+ `max_gen` or `min_fit` or `max_time`: Limitation of termination
    + type: int / float / float
    + default: Raise `ValueError`
+ `report`: Report per generation
    + type: int
    + default: 10

Others arguments are same as [`Differential.__init__()`](#differential9595init__).

## Module `verify`

### Reference

See the sections of [Pyslvs API](pyslvs-api.md#module-verify)

[Verification]: pyslvs-api.md#verification
