Library Files
===

1. `_slvs.pyd` or `_slvs.so`

1. `slvs.py`

1. `libslvs.so`

1. `slvs_solid.py` (If you want to use it)

1. And your python program(s)

Use this comment:

<pre>
$python3 configure.py
$make
</pre>

Anaconda Adjustment (Windows)
===

Some conflicts between the C Language and Python.

You need change a few of Python files to avoid these conflicts.

But you can be assured that the changes won't cause any negative impact.

libpython35.a
---

If you got a warning say can't find `libpython35`, or a lot of warning, such as:

`slvs_wrap.o: In function '_SWIG_Py_None': slvs_wrap.cxx:1446: undefined reference to '__imp__Py_RefTotal'`

1. Copy `Anaconda3\python35.dll` into `Anaconda3\libs` folder.

1. Download **gendef** and install it.

Use this command:

<pre>
>cd "where your python"\Anaconda3\libs
>gendef python35.dll
>dlltool --dllname python35.dll --def python35.def --output-lib libpython35.a
</pre>

In `\Anaconda3\include\pyconfig.h`, find this:

<pre>
#ifdef _WIN64
#define MS_WIN64
#endif
</pre>

Cut them **Above** this:

<pre>
#ifdef _MSC_VER
</pre>

In `\Anaconda3\Lib\distutils\cygwinccompiler.py`, find this:

<pre>
#with MSVC 7.0 or later.
self.dll_libraries = get_msvcr()
</pre>

Commit `self.dll_libraries = get_msvcr()`

`math.h` conflict with `pyconfig.h`
---

If you got a warning with `_hypot` in `pyconfig.h`, you should do this:

In `\Anaconda3\include\pyconfig.h`, find this:

<pre>
#define hypot _hypot
</pre>

Edit it to this:

<pre>
#ifndef _MATH_H_
#define hypot _hypot
#endif
</pre>
