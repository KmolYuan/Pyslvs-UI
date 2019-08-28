# Build a Planar Linkage Mechanism

The mechanism expression is based on [hypergraph](https://en.wikipedia.org/wiki/Hypergraph),
where "points" and "links" is corresponded to "edges" and "vertices" respectively.
A point will be called "joint" if it's connected between two or more links.

The adjacency is decided by "Links" attribute of the points and
"Points" attribute of the links.
And the dimensions (link lengths) of the mechanism is decided by
"X" and "Y" attributes of the points as its initial position.

There also has "Type" attribute to represent the joint type of a point.

+ "R" means revolute (rotatable) joint.
+ "P" means prismatic joint.
+ "RP" means revolute-prismatic joint.

## Main Canvas

The main canvas of Pyslvs can be changed the view part and size by
dragging and scrolling mouse wheel respectively.
Clicking "zoom to fit" button can adjust it automatically.

Instead of actions on menu bar, context menu (right-click menu) of
the main canvas or tables are also contain most of entity operations.

Even if switching the panel tabs, the main canvas can still operate
the selected entities by hot keys and clicking.

## Operations

The following are the operation of mechanism expression in "Mechanism" menu:

+ New / Edit / Delete point
+ New / Edit / Delete link
+ Scale mechanism

"New point" operation can be triggered by Alt key + left button to create
a new point on mouse position;
"edit" operation can be triggered by double clicking the position on
the main canvas;
and "delete" operation can be triggered by "delete" key.

There are some convenient commands for editing entities in context menu,
they will appear when needed.

+ Points:
    + Grounded: Add / remove ground link to the link list of the point(s).
    + Multiple joint: Merge the point(s) into a specific point.
    + Copy coordinate: Copy the current coordinate to system clipboard.
    + Clone: Copy the point(s) as new point(s).
+ Links:
    + Merge links: Merge the link(s) together.
    + Release: Make the ground link as a new link.
    + Constrain: Merge the link(s) into ground link.
+ Shared:
    + Copy table data: Copy the cell information of the table.

The operations are fully support with the undo and redo action.
And the adjacency will be updated automatically,
even if there has only one entity edited.

## Selection

"Points" and "Links" tabs in "Mechanism" will
active different selection mode of "point" and "link" entities.
"Formulas" tab is not mapped to any type of entities.
Dragging the cursor to select the objects by rectangle.
The selected objects can be correspond to each row of the table.

"Shift" and "Ctrl" keys will decide the behavior of continuous selection.
"Shift" keys will update the selection as union.
"Ctrl" keys will deselect the intersection, update the relative complement.

"Ctrl+A" and "Esc" key can select and deselect all the entities respectively.
Clicking an empty area without holding "Shift" and "Ctrl" keys also can
deselect all the entities.

Using "Shift" key plus scrolling mouse wheel can switch the tabs and the selection modes.
This function also can be activated directly if your mouse has a horizontal wheel.

The "delete" actions and free move modes are support with multiple selected objects.

## Free Move Modes

"Free move mode" options is a combobox button under the main canvas.
There are following modes:

+ View mode (default)
+ Translate mode
+ Rotate mode
+ Reflect mode

The selected points are the operating objects of those modes,
view mode does nothing of them.
When dragging cursor under the main canvas without "Shift" and "Ctrl" keys,
the edit behavior will be active.

+ Translate mode will move the points with the same offset of cursor.

+ Rotate mode will move the points by surrounding origin point (0, 0)
with cursor.

+ Reflect mode will change the sign of the coordinates of the points,
which is decided from the axes that crossed by cursor.

## Storage

When there have multiple expressions, the expressions can be saved in
the list of storage, which is under the selection table.
Enter a name, then press "add" button to save them;
they also can be removed by "delete" button.
When "restore" an expression, the current expression will be cleared first.
All those operations are supported with the undo and redo system.

There have "copy" and "paste" button support with the system clipboard.
The literal string can be add to storage list or
saved to another program directly.
