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

These data called "workbook" or "Pyslvs project" in the UI.

## Features of Formats

| Attributes | YAML |
|:----------:|:----:|
| is default | yes |
| suffix | `.pyslvs.yml` |
| base | text |
| file size | larger |
| file lock | when saving |
| version recording | no |
