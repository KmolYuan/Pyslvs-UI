# Settings

The Pyslvs settings are saved by Qt settings mechanism.
It will be saved into "~/.pyslvs.ini" on any platform,
where "~" is the user home path.

## Auto Save

### Do not save Pyslvs option

All of setting **will not** be saved after closed Pyslvs,
unless uncheck this option.

If the option has be check, the setting on user's computer will be deleted.

Default is checked.

## Main Canvas

### Line width (pixel)

The line width of the canvas.

Default is 3.

### Font size (pixel)

The font size of the canvas.

Default is 14.

### Path width (pixel)

The path curve width of the canvas.

Default is 3.

### Scale factor

The scale factor of the view.
Increase the factor will zoom faster.

Default is 10.

### Selection radius (pixel)

The radius of the points detection when selecting them.

Default is 10.

### Link transparency (percent)

The link transparency excluding its edges.
This option will consume more resources.

Default is 0%.

### Margin of "zoom to fit" (percent)

When calling "zoom to fit" action,
the margin between mechanism and the bounds of canvas.
Its size is relative to the width and height of main canvas.

Default is 5%.

### Joint annotation size (diameter) (pixel)

The size of joints annotation, excluding selection annotation.

Default is 5.

### Center zooming by (options)
 
Options: {Cursor, Canvas center}

The behavior during zooming.
 
Default is Cursor.

### Snap the mouse when dragging (unit)

The minimal unit of dragging.
Set to zero can be disable this function.

Default is 1.

### Background (file path)

The file path of the background image.
The file format should be supported by Qt.
Invalid path or empty path will disable this function.

Default is empty.

### Background opacity

The opacity of the background, between 0.0 to 1.0.

Default is 1.

### Background scale (times)

The scale factor of the background.

Default is 1.

### Background offset (unit)

The XY offset of the background.

Default is (0, 0).

## History

### Undo limit (times)

The undo and redo limit of Qt.

Default is 32.

## Kernels

### Planar solving (options)

Options: {Pyslvs, Python-Solvespace, Sketch Solve}

The solver of mechanism.

Default is Pyslvs.

### Path preview (options)

Options: {Pyslvs, Python-Solvespace, Sketch Solve, Same as solver kernel}

The solver of path preview function.

Default is Same as solver kernel.

## Misc

### Show full file path on window title.

Default is unchecked.

### Show error messages in the console.

Default is unchecked.

### Monochrome mode for mechanism. (Excluding indicators)

Default is unchecked.
