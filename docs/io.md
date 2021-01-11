# File Format of Pyslvs

There are two file formats of Pyslvs, the text-based YAML format is default,
and the binary SQLite is used to record the versions.
The YAML format is powered by [PyYAML](https://pyyaml.org).

## Saved Data

The following data will saved in the files.

+ Mechanism expression
+ Mechanism storage list
+ Input pairs
+ Path list
+ Kinematic chains collections
+ Configuration collections
+ Dimensional synthesis results

These data called "project" or "Pyslvs project" in the UI.

## Features of Formats

The saving option will be changed when loaded a different type of format.
The default saving format is YAML.

| Format | Description |
|:------:|:------------|
| YAML | Blocked YAML. |
| Compressed YAML | One line YAML. |
| Pickle | Python official compression format. |
