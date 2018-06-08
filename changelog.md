Change Log
===

Version 18.06
===

Features
---

+ Free move mode:
    + Linkage editing is supported in expression table.
    + Fix the error of angle updating.
+ Show the values on expression table.
+ Add solution selection mode with expression table.
+ Dimensional synthesis function:
    + Re-designed user interface.

Development
---

+ Update module "dxfwrite" to "ezdxf".


Version 18.05
===

Features
---

+ Linkage selection mode:
    + New linkage selection function for both of table widget and main canvas.
    + Using ctrl + mouse wheel can adjust the tab of entities table widget.
+ Main canvas:
    + Add cursor tooltips when dragging on main canvas.
    + Center zooming function and option with 'by cursor' and 'by canvas center'.
+ Colors:
    + Pyslvs can support custom color by using '(R, G, B)' string.
    + Add color picker in setting interface.
+ Solvespace format:
    + Comments will be generate into a new layout in Solvespace format.
    + Simple reading function for *.slvs format (only support P joint).
    + New option to generate part files.
+ Path record:
    + Add "copy path" function in path context menu.
    + Path preview function are support P joint.
+ New solving kernel option "Pyslvs" as default.
+ Add mouse snapping option (default 1 unit).
+ Triple ball lifter example.
+ Shortcut keys adjustment.
+ "Add" command of storage function will not clean the canvas (should do it by self).
+ Add "merge linkages" function in link context menu.
+ Add virtual model option to change linkages appearance.

Development
---

+ Expression grammar:
    + New highlight module Pygments, use to support Python and PMKS expression.
    + Now PMKS grammar can support color string, one-line annotations, multiple line and indentations.
+ Cython libraries:
    + Pyslvs kernel has been independently.
    + Compile method adjustment.
    + Merge into 'pyslvs' folder.
    + Using Python typing for Python functions in Cython libraries.
    + Add Cython header to sharing declarations between libraries.
    + Add new "PXY" function to make solution of P joint.
+ Compile:
    + Compile process improvement.
    + Reduce the size while packing AppImage file.
    + Reduce the size of images.
+ Solvespace format:
    + Python API for simple 2D sketch IO.
+ Modules and objects naming adjustment.
+ PyQt version should upgrade to 5.10 or above to support Qt graph methods.


Version 18.04
===

Features
---

+ Auto preview path will be shown when input joint has been set.
+ Triangular solutions can be show in main canvas when switch to "Expression" table.
+ New driver setting mode of triangular iteration.
+ Add a spin box for input QDial.
+ 'New link' functional behavior improvement.
+ Pyslvs will save the settings in local, if user let it to do this.

Development
---

+ Several functional corrections and optimizations.
+ PLPP function has been optimized.
+ "P0", "P1", "P2" letters will be use as expression, instead of "A", "B", "C".
+ Main window method was split into sub function at "widget" folder.
+ Build process improvements.


Version 18.03:

Features
---

+ Fix an error caused by wrong grounded linkage.
+ Auto configuration function in triangular iteration.
+ Backtrack function for the 'Keep DOF' option.
+ Database will saving the inputs variables settings.
+ Inputs variables settings can be support undo function.

Development
---

+ Script annotations for functions and classes.
+ Separate 'Inputs' tab widget.
+ Cython type checker for Python containers.
+ Windows executable file was compiled by Mysys 2.


Version 18.02
===

Features
---

+ Dimensional synthesis function has been associated with triangular iteration function.
+ Related function about dimensional synthesis has been improved.
    + Loading profile function.
    + Appearance and editing function of target paths.
    + Result operating function.
    + Task target has been added "fitness" and "time" limitation options.
+ Preview canvas in triangular iteration has been applied to related interface.
+ "New link" function improvement.
+ "Zoom to fit" function improvement.
+ "Mechanism storage" function improvement.
+ Check for updates function.

Development
---

+ Some improvements about functions and objects.
+ Dimensional synthesis dialog move to a new name space.
+ Remove unnecessary icons and library source code to make execution size reduction.
+ More errors fixed.


Version 18.01
===

Features
---

+ Triangular iteration function.
+ Collections IO improvements.
+ Dimensional synthesis function improvements.
+ Some options and interface adjustments.

Development
---

+ Use `__init__.py` modules to manage classes and functions.
+ Cython kernel of Number synthesis.
+ Adjust some modules and classified.
