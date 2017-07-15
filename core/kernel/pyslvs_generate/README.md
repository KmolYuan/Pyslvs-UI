Pyslvs_generate
===

Origin repository: [https://github.com/kmollee/algorithm](https://github.com/kmollee/algorithm)

How to build?
===

Linux or Mac
---

Install Cython and continue.

```bash
$sudo pip3 install cython
$make
```

Windows
---

Install Python 3 with Cython and continue.

If you are using 64 bit OS with 64bit Python, unfortunately you **can not** use mingw64 to complete the compilation.

Using Microsoft Visual Studio is the only option, you can get it from [here](https://www.visualstudio.com/downloads/). Get the Visual Studio Community and install Windows SDK.

```bash
>pip install cython
>make
```

Get Library Files
---

Regardless of their name(`*.so` in Linux or `*.pyd` in Windows), should have these items:

* tinycadlib

* planarlinkage

* rga

* firefly

* de

Then run `test.py` to test if they are okay.
