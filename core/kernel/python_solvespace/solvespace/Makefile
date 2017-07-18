WIN_DEFINES = -D_WIN32_WINNT=0x500 -D_WIN32_IE=0x500 -DWIN32_LEAN_AND_MEAN
DEFINES = -DISOLATION_AWARE_ENABLED -DLIBRARY
# Use the multi-threaded static libc because libpng and zlib do; not sure if anything bad
# happens if those mix, but don't want to risk it.
CFLAGS  = -I../extlib -I../../common/win32 -I. -I.. -D_DEBUG -D_CRT_SECURE_NO_WARNINGS -O2 -g -Wno-write-strings -fpermissive
CFLAGS_SHARED = -fPIC -shared $(CFLAGS)

HEADERS = ../common/win32/freeze.h \
          ui.h \
          solvespace.h \
          dsc.h sketch.h \
          expr.h \
          polygon.h \
          srf/surface.h \

OBJDIR = obj

FREEZE   = $(OBJDIR)/freeze.obj

W32OBJS  = $(OBJDIR)/w32main.obj \
           $(OBJDIR)/w32util.obj \

SSOBJS   = $(OBJDIR)/solvespace.obj \
           $(OBJDIR)/textwin.obj \
           $(OBJDIR)/textscreens.obj \
           $(OBJDIR)/confscreen.obj \
           $(OBJDIR)/describescreen.obj \
           $(OBJDIR)/graphicswin.obj \
           $(OBJDIR)/modify.obj \
           $(OBJDIR)/clipboard.obj \
           $(OBJDIR)/view.obj \
           $(OBJDIR)/util.obj \
           $(OBJDIR)/style.obj \
           $(OBJDIR)/entity.obj \
           $(OBJDIR)/drawentity.obj \
           $(OBJDIR)/group.obj \
           $(OBJDIR)/groupmesh.obj \
           $(OBJDIR)/request.obj \
           $(OBJDIR)/glhelper.obj \
           $(OBJDIR)/expr.obj \
           $(OBJDIR)/constraint.obj \
           $(OBJDIR)/constrainteq.obj \
           $(OBJDIR)/mouse.obj \
           $(OBJDIR)/draw.obj \
           $(OBJDIR)/toolbar.obj \
           $(OBJDIR)/drawconstraint.obj \
           $(OBJDIR)/file.obj \
           $(OBJDIR)/undoredo.obj \
           $(OBJDIR)/system.obj \
           $(OBJDIR)/polygon.obj \
           $(OBJDIR)/mesh.obj \
           $(OBJDIR)/bsp.obj \
           $(OBJDIR)/ttf.obj \
           $(OBJDIR)/generate.obj \
           $(OBJDIR)/export.obj \
           $(OBJDIR)/exportvector.obj \
           $(OBJDIR)/exportstep.obj \

SRFOBJS = $(OBJDIR)/ratpoly.obj \
           $(OBJDIR)/curve.obj \
           $(OBJDIR)/surface.obj \
           $(OBJDIR)/triangulate.obj \
           $(OBJDIR)/boolean.obj \
           $(OBJDIR)/surfinter.obj \
           $(OBJDIR)/raycast.obj \
           $(OBJDIR)/merge.obj \

RES = $(OBJDIR)/resource.res


#LIBS = user32.lib gdi32.lib comctl32.lib advapi32.lib shell32.lib opengl32.lib glu32.lib \
        extlib\libpng.lib extlib\zlib.lib extlib\si\siapp.lib
LIBS = extlib/libpng.lib extlib/zlib.lib extlib/si/siapp.lib

CXX = g++

RC = "C:\Program Files (x86)\Windows Kits\$(RCVER)\bin\$(RCBIT)\rc.exe"
RCVER = 10
RCBIT = x64

PERL = W:\Perl524\bin\perl.exe

VPATH = srf \
        win32 \
        ../common/win32 \

all: $(OBJDIR)/solvespace.exe
	@cp $(OBJDIR)/solvespace.exe .

clean:
	@rm -f $(OBJDIR)/*

$(OBJDIR)/%.obj: %.cpp $(HEADERS)
	@echo obj "$@"
	@$(CXX) $(CFLAGS_SHARED) $(DEFINES) -c -o $@ $<

$(RES): resource.rc icon.ico
	@echo RES
	$(RC) $<
	mv win32/resource.res  $@

$(OBJDIR)/solvespace.exe: $(SRFOBJS) $(SSOBJS) $(W32OBJS) $(FREEZE) $(RES)
	@echo solvespaceEXE
	$(CXX) $(DEFINES) $(CFLAGS) -o $@ $^ $(LIBS)
	editbin /nologo /STACK:8388608 $(OBJDIR)/solvespace.exe
	@echo solvespace.exe

toolbar.cpp: $(OBJDIR)/icons.h

textwin.cpp: $(OBJDIR)/icons.h

glhelper.cpp: bitmapfont.table font.table bitmapextra.table

$(OBJDIR)/icons.h: png2c.pl icons/*
	@echo icons
	$(PERL) $< $@ $(OBJDIR)/icons-proto.h