# File Format of Pyslvs

There are two file formats of Pyslvs, the text-based YAML format is default,
and the binary SQLite is used to record the versions.
The YAML format is powered by [PyYAML](https://pyyaml.org),
and the SQLite format is powered by [peewee](http://docs.peewee-orm.com).

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

## Format Differences

| Attributes | YAML | SQLite |
|:----------:|:----:|:------:|
| is default | yes | no |
| suffix | `.pyslvs.yml` | `.pyslvs` |
| base | text | binary |
| file size | larger | smaller |
| file lock | when saving | during open |
| version recording | no | yes |
