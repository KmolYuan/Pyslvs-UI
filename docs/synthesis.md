# Mechanism Synthesis

The synthesis methods are used to help the user to recreate the mechanism
as a new one.

There are following steps:

1. Structural Synthesis
1. Collections
    + Structures
    + Configuration
1. Dimensional Synthesis (path generation)

**Structural Synthesis** can find a new adjacency of the mechanism,
which is decided by the joints number and the links number.
The graph blocks are called "generalized chains",
they will add more constraints and requirements in **Collections** step.
At last, the configuration will be recreated its dimensions in
**Dimensional Synthesis** step.
The new mechanism can be added to project as mechanism expression.

## Structural Synthesis

Recreate new adjacency of the mechanism.

### Graph Expression

In this step, graphs are represented by Edge Set in [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory).
The data format of Edge Set is store the edges of a graph only,
where the vertices are labeled.

The expression is mapping to [NetworkX](https://networkx.github.io/),
a famous module used to study the networks problems, which is written in pure Python.
Inherit from its concept, the Pyslvs can parse following string (without assignment)
as graphs, with Python built-in containers:

```python
# List and tuple pairs
g1 = [(0, 1), (1, 2), (2, 3), (0, 3)]

# Tuples and tuple pairs (quit unclear)
g2 = ((0, 1), (1, 2), (2, 3), (0, 3))

# Use list comprehensions with built-in iterator
g3 = [(n, n + 1) for n in range(3)] + [(0, 3)]
```

Conversely, Pyslvs also generate the strings as `g1` style.

### From Current Mechanism

The generalized chain of current mechanism can be obtained by clicking
"analysis" button top of the page.

This process is called "generalization".
The result contains the graph, the number of joints and the number of links.
The multiple joints will be parsed as several joints connected on the previous links; 
and each joint with 2 DOF will be turned into two 1 DOF joints.

### Number Synthesis

Base on the number of joints and the number links, the graphs can be divide as following features:

+ Link assortment
+ Contracted link assortment

The link assortment is the numbers of each link types,
and the contracted link assortment is the numbers of each series of binary links.
In the same assortment, the graphs will have same features as above.

### Graph Atlas

The enumeration process will take a lot of times if the numbers are too large.
If terminated the process, the calculated graph atlas will still be kept.

After enumeration of conventional graphs, the graphs can be copied as string,
saved as image, saved as string list or added to collection.
The saved string list can be import to Pyslvs as well.

The layout system may cause the adjacency of some graphs to unclear or
even can't draw some graphs.
Don't worry, the expression will still working with the graph checking and
other mechanisms.

## Structure Collections

Collect structures of interest.

### Filters

The graphs can be input to the collection list.
There has some graph filter of the input graph(s):

+ Is empty: The Edge Set of the graph is empty.
+ Is not connected: The vertices is not connect as one graph.
+ Is not planar: The graph is not a planar graph.
+ Has cut-link: The graph has cut-vertex.
+ Can't draw: The graph is unsupported with layout system.
+ Is isomorphic with other graphs.

The check processes are very fast, unless there are too much graphs.

## Configuration of Collections

On this page, there has a database of your project (file).
When adjusted a configuration, you need to save it manually,
because of the database is not supported with the undo and redo system.
Load and create them are working with the same mechanism.

### Topological Configuration

There have some settings for the generalized chains:

1. Grounded link
1. Input list
1. Custom points
1. Multiple joints
1. Target points
1. Initial positions

## Dimensional Synthesis

Recreate new dimensions of the mechanism.
This target is path generation,
other types of target are currently not provided in Pyslvs.

### Mechanism Settings

The settings are inherit from the configuration, but added the upper and lower bounds.
The bounds control the follows:

1. Grounded joints
1. Length of links
1. Input list

### Metaheuristic Random Algorithms

There are three types of algorithm provided in Pyslvs:

+ Real-coded Genetic Algorithm
+ Differential Evolution
+ Firefly Algorithm

Each algorithm has different settings, some of them will affect the evolution time.

### Results

The results of synthesis will add to result list, which is not supported with
the undo and redo system.
The "merge" button can merge the result as a mechanism expression into the main canvas,
and the path will also be added into "records list".
