all: build

# into package folder
build: *.pyx
ifeq ($(OS),Windows_NT)
	-rename __init__.py .__init__.py
	python setup.py build_ext --inplace
	rename .__init__.py __init__.py
else
	-mv __init__.py .__init__.py
	python3 setup.py build_ext --inplace
	mv .__init__.py __init__.py
endif

test: build
ifeq ($(OS),Windows_NT)
	python test.py
else
	python3 test.py
endif

clean:
ifeq ($(OS),Windows_NT)
	-rename .__init__.py __init__.py
	-del *.pyd /q
	-rd .\build /s /q
	-del *.c /q
else
	-mv .__init__.py __init__.py
	-rm -f *.so
	-rm -fr build
	-rm -f *.c
endif
