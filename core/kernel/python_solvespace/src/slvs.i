%module slvs

//NOTE We must put it into the %begin section (instead of %header) because
//     it must be available for the stuff in %extends and that is put
//     directly before the header section...
%begin %{
    // include Python first because it would complain about redefined
    // symbols
#   include <cmath>
#   include <Python.h>

    // we need malloc and memset
#   include <string.h>
#   include <stdlib.h>

    // finally, we include slvs - the library we want to wrap
#   include "../include/slvs.h"

    // and one more: a few helpers to make the API more pythonic
    // (Well, actually it grew to be a bit more than 'a few' *g*)
#   include "slvs_python.hpp"
%}

// Before we include anything that is visible by SWIG, we must set the
// table. This means we tell SWIG how it should map certain types.

#if defined(SWIGPYTHON)

// Some quaternion functions returns values with call-by-reference, so
// we have to tell SWIG to do the right thing.
// example: DLL void Slvs_QuaternionU(double qw, ...,
//                             double *x, double *y, double *z);
// for a more complex example, see http://stackoverflow.com/a/6180075

// The user should have to pass any argument (numinputs=0) and we pass
// a pointer to a temporary variable to store the value in.
%typemap(in, numinputs=0) double * (double temp) {
   $1 = &temp;
}

// We get the value, wrap it in a PyFloat and add it to the output. The
// user can use it like this:
// x, y, z = Slvs_QuaternionU(...)
%typemap(argout) double * {
    PyObject * fl = PyFloat_FromDouble(*$1);
    if (!fl) SWIG_fail;
    $result = SWIG_Python_AppendOutput($result, fl);
}

#endif


%ignore param;


%include "../include/slvs.h"

/*%exception System::System {
   try {
      $action
   } catch (out_of_memory_exception &e) {
      PyErr_SetString(PyExc_MemoryError, const_cast<char*>(e.what()));
      return NULL;
   } catch (not_enough_space_exception &e) {

   }
}*/

%include "exception.i"

%typemap(throws) out_of_memory_exception {
    SWIG_exception(SWIG_MemoryError, const_cast<char*>($1.what()));
}

%typemap(throws) not_enough_space_exception {
    SWIG_exception(SWIG_RuntimeError, const_cast<char*>($1.what()));
}

%typemap(throws) wrong_system_exception {
    SWIG_exception(SWIG_RuntimeError, const_cast<char*>($1.what()));
}

%typemap(throws) invalid_state_exception {
    SWIG_exception(SWIG_RuntimeError, const_cast<char*>($1.what()));
}

%typemap(throws) invalid_value_exception {
    SWIG_exception(SWIG_RuntimeError, const_cast<char*>($1.what()));
}

/*
%except(python) {
    try {
        $function
    } catch (invalid_value_exception& e) {
        SWIG_exception(SWIG_RuntimeError, const_cast<char*>(e.what()));
    }
}
*/


// some vector math

%pythoncode %{

import math

def mat_transpose(m):
    for i in range(4):
        for j in range(4):
            if i < j:
                a = m[i][j]
                b = m[j][i]
                m[i][j] = b
                m[j][i] = a

# call to_openscad(), if it exists
def _to_openscad(x):
    if hasattr(x, 'to_openscad'):
        return x.to_openscad()
    elif isinstance(x, list) or isinstance(x, tuple):
        return map(_to_openscad, x)
    else:
        return x

class Vector(object):
    __slots__ = "xs"

    def __init__(self, *args):
        args = _to_openscad(args)
        if len(args) == 1 and isinstance(args[0], Vector):
            self.xs = list(args[0].xs)
        elif len(args) == 1 and (isinstance(args[0], list) or isinstance(x, tuple)):
            self.xs = list(args[0])
        else:
            self.xs = list(args)

    def __add__(self, v):
        v = Vector(v)
        if len(self.xs) != len(v.xs):
            raise ValueError("vectors must have the same length (self: %d, other: %d)" % (len(self.xs), len(v.xs)))
        return Vector(map(lambda a,b: a+b, self.xs, v.xs))

    def __sub__(self, v):
        v = Vector(v)
        if len(self.xs) != len(v.xs):
            raise ValueError("vectors must have the same length (self: %d, other: %d)" % (len(self.xs), len(v.xs)))
        return Vector(map(lambda a,b: a-b, self.xs, v.xs))

    def __mul__(self, v):
        if not isinstance(v, (int, long, float)):
            raise ValueError("Vectors can only be scaled by a number. Use cross or dot to multiply vectors.")
        return Vector(map(lambda x: x*v, self.xs))

    def cross(self, v):
        v = Vector(v)
        if len(self.xs) != 3 or len(v.xs) != 3:
            raise ValueError("vectors must have length 3")
        a = self.xs
        b = v.xs
        c = [ a[1]*b[2] - a[2]*b[1],
              a[2]*b[0] - a[0]*b[2],
              a[0]*b[1] - a[1]*b[0] ]
        return Vector(c)

    def dot(self, v):
        v = Vector(v)
        if len(self.xs) != len(v.xs):
            raise ValueError("vectors must have the same length (self: %d, other: %d)" % (len(self.xs), len(v.xs)))
        return sum(map(lambda a,b: a*b, self.xs, v.xs))

    def length(self):
        return math.sqrt(sum(map(lambda x: x*x, self.xs)))

    def normalize(self, length = 1.0):
        l = self.length()
        return Vector(map(lambda x: x/l*length, self.xs))

    def to_openscad(self):
        return self.xs

    def __getitem__(self, i):
        return self.xs[i]

    def __setitem__(self, i, v):
        self.xs[i] = _to_openscad(v)

# Move and rotate an object using three points:
# - The origin will be moved into p1.
# - A point of the x axis will be moved into p2.
# - A point of the xy-plane will be moved into p3.
# In practice, this means: Build your object near the
# origin on the xy-plane. You determine the final
# position by deciding where the origin and x-axis
# should go, so both of them should have some
# significance. The xy-plane is also important, but
# usually this will be a flat surface, anyway (if you
# extrude from it).
def move_and_rotate(p1, p2, p3):
    # get values from Param or Point
    origin = Vector(p1)
    p2     = Vector(p2)
    p3     = Vector(p3)

    # calculate vectors from origin to p2 and p3
    v1 = p2 - origin
    v2 = p3 - origin

    # make sure they have length 1.0
    v1 = v1.normalize()
    v2 = v2.normalize()

    # third vector is perpendicular
    v3 = v1.cross(v2)

    # we calculate the second vector again to make sure
    # that v1 and v2 are perpendicular
    v2 = v3.cross(v1)

    # The vectors are the base vectors of our object
    # coordinate system, so we can put them into the
    # rotation matrix.
    m = [ v1.xs  + [0],
          v2.xs  + [0],
          v3.xs  + [0],
          [0, 0, 0, 1] ]
    # We have to transpose it.
    mat_transpose(m)

    # add translation to origin
    m[0][3] = origin[0]
    m[1][3] = origin[1]
    m[2][3] = origin[2]

    return m
%}


// %ignore Param::prepareFor;
// %ignore Entity::Entity;

//%include "slvs_python.hpp"

class Param {
public:
    // This can be used as value for a parameter to signify that a new
    // parameter should be created and used.
    Param(double value);

    Slvs_hParam GetHandle() throw(invalid_state_exception);
    Slvs_hGroup GetGroup()  throw(invalid_state_exception);
    double GetValue()       throw(invalid_state_exception);
    void SetValue(double v) throw(invalid_state_exception);

    // see http://stackoverflow.com/a/4750081
    %pythoncode %{
        __swig_getmethods__["handle"] = GetHandle
        if _newclass: handle = property(GetHandle)

        __swig_getmethods__["group"] = GetHandle
        if _newclass: group = property(GetGroup)

        __swig_getmethods__["value"] = GetValue
        __swig_setmethods__["value"] = SetValue
        if _newclass: value = property(GetValue, SetValue)
    %}

    %pythoncode %{
        def to_openscad(self):
            return self.value
    %}
};

class Entity {
private: Entity();
public:
    Slvs_hEntity GetHandle();
    Slvs_hGroup  GetGroup()  throw(invalid_state_exception);

    %pythoncode %{
        __swig_getmethods__["handle"] = GetHandle
        if _newclass: handle = property(GetHandle)

        __swig_getmethods__["group"] = GetHandle
        if _newclass: group = property(GetGroup)
    %}
};

#define throw_entity_constructor \
    throw(wrong_system_exception, invalid_state_exception, invalid_value_exception, not_enough_space_exception)

class Point : public Entity {
private:
    Point();
};

//NOTE Constructors with double instead of Param are NOT
//     defined in the C++ code. SWIG will generate wrappers
//     and they will work because the C++ compiler
//     automatically uses the Param constructor to convert
//     double to Param.

class Point3d : public Point {
public:
    Point3d(Param x, Param y, Param z,
            System* system = NULL,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    Point3d(double x, double y, double z,
            System* system,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Param x() throw(invalid_state_exception);
    Param y() throw(invalid_state_exception);
    Param z() throw(invalid_state_exception);

    %pythoncode %{
        def to_openscad(self):
            return [ self.x().value, self.y().value, self.z().value ]
    %}
};

class Normal3d : public Entity {
public:
    Normal3d(Param qw, Param qx, Param qy, Param qz,
            System* system = NULL,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    Normal3d(double qw, double qx, double qy, double qz,
            System* system = NULL,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    Normal3d(Workplane wrkpl, Slvs_hGroup group = USE_DEFAULT_GROUP);

    //NOTE You can either use qw, ... OR workplane!

    bool isNormalIn3D() throw(invalid_state_exception);
    Param qw() throw(invalid_state_exception);
    Param qx() throw(invalid_state_exception);
    Param qy() throw(invalid_state_exception);
    Param qz() throw(invalid_state_exception);

    bool isNormalIn2D() throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);

    %pythoncode %{
        def vector(self):
            return [ self.qw().value, self.qx().value,
                     self.qy().value, self.qz().value ]

        # A normal is a quaternion in disguise, so we
        # transform it into a rotation. You can use it
        # with multmatrix.
        def to_openscad(self):
            q = self.vector()
            m = [ Slvs_QuaternionU(*q) + [0],
                  Slvs_QuaternionV(*q) + [0],
                  Slvs_QuaternionN(*q) + [0],
                  [0, 0, 0, 1] ]
            mat_transpose(m)
            return m
    %}
};

class Workplane : public Entity {
public:
    static Workplane FreeIn3D;

    Workplane(Point3d origin, Normal3d normal,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Point3d  origin() throw(invalid_state_exception);
    Normal3d normal() throw(invalid_state_exception);

    %pythoncode %{
        # A workplane is transformed into the rotation
        # and translation that moves an object to the
        # plane and rotates it accordingly:
        # (0,0,0)   ->  origin of plane
        # xy-plane  ->  the plane
        # You can use the matrix with multmatrix.
        def to_openscad(self):
            m = self.normal().to_openscad()
            m[0][3] = self.origin().x().value
            m[1][3] = self.origin().y().value
            m[2][3] = self.origin().z().value
            return m
    %}
};

class Point2d : public Point {
public:
    Point2d(Workplane workplane, Param u,
            Param v, System* system = NULL,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    Point2d(Workplane workplane, double u,
            double v, System* system = NULL,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Param     u()         throw(invalid_state_exception);
    Param     v()         throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);

    %pythoncode %{
        def to_openscad(self):
            return [ self.u().value, self.v().value ]
    %}
};

class LineSegment : public Entity {
private:
    LineSegment();
};

class LineSegment3d : public LineSegment {
public:
    LineSegment3d(Point3d a, Point3d b, Workplane wrkpl = Workplane::FreeIn3D,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Point3d a() throw(invalid_state_exception);
    Point3d b() throw(invalid_state_exception);
};

class LineSegment2d : public LineSegment {
public:
    LineSegment2d(Workplane wrkpl, Point2d a, Point2d b,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Point2d a()           throw(invalid_state_exception);
    Point2d b()           throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);
};

class Circular : public Entity {
private:
    Circular();
};

class ArcOfCircle : public Circular {
public:
    ArcOfCircle(Workplane wrkpl, Normal3d normal,
            Point2d center, Point2d start, Point2d end,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Point2d   center()    throw(invalid_state_exception);
    Point2d   start()     throw(invalid_state_exception);
    Point2d   end()       throw(invalid_state_exception);
    Normal3d  normal()    throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);
};

class Distance : public Entity {
public:
    Distance(Workplane wrkpl, Param distance,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Param     distance()  throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);
};

class Circle : public Circular {
public:
    Circle(Workplane wrkpl, Normal3d normal,
            Point2d center, Distance radius,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;

    Point2d   center()    throw(invalid_state_exception);
    Distance  distance()  throw(invalid_state_exception);
    Normal3d  normal()    throw(invalid_state_exception);
    Workplane workplane() throw(invalid_state_exception);
};

class Cubic : public Entity {
public:
    //TODO can we use it in 2d and 3d ?
    //TODO implement getters
    Cubic(Workplane wrkpl, Point2d pt0, Point2d pt1,
            Point2d pt2, Point2d pt3,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    Cubic(Point3d pt0, Point3d pt1,
            Point3d pt2, Point3d pt3,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
};

class Constraint {
    Constraint();
public:
    Slvs_hEntity GetHandle();

    System* system();

    Slvs_hGroup GetGroup() throw(invalid_state_exception);

    int type() throw(invalid_state_exception);
    //Workplane workplane() throw(invalid_state_exception);

    %pythoncode %{
        __swig_getmethods__["handle"] = GetHandle
        if _newclass: handle = property(GetHandle)

        __swig_getmethods__["group"] = GetHandle
        if _newclass: group = property(GetGroup)
    %}

    // This constructor can be used to make arbitrary
    // constraints. It has a very ugly name to discourage
    // its use. If you need a constraint that the library
    // doesn't support, you should implement it.
    static Constraint some_other_constraint(
            System* system,
            int type, Workplane workplane, double value,
            Point ptA, Point ptB, Entity entityA, Entity entityB,
            Slvs_hGroup group = USE_DEFAULT_GROUP);

    // process source of those functions like this:
    // find:    ' \{(.|\n)*?\}'
    // replace: '\n\t\tthrow_entity_constructor;'
    // (Sublime Text 2)

    static Constraint on(
            Point3d p1, Point3d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint on(
            Workplane wrkpl, Point p1, Point p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint distance(double value,
            Point3d p1, Point3d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint distance(double value,
            Workplane wrkpl, Point p1, Point p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint distance(double value,
            Workplane wrkpl, Point3d p,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint distance(double value,
            Workplane wrkpl, Point p, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint distance(double value,
            Point3d p, LineSegment3d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint on(
            Workplane wrkpl, Point3d p,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint on(
            Workplane wrkpl, Point p, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint on(
            Point3d p, LineSegment3d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint on(
            Workplane wrkpl, Point p, Circle c,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint horizontal(
            Workplane wrkpl, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint vertical(
            Workplane wrkpl, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
		throw_entity_constructor;
    static Constraint diameter(double diameter,
            Workplane wrkpl, Circular c,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint equal_radius(
            Workplane wrkpl, Circular c1, Circular c2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint equal(Workplane wrkpl,
            LineSegment2d line, Circular c,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint equal(Workplane wrkpl,
            LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint equal_point_line(Workplane wrkpl,
            Point2d p1, Point2d p2,
            LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    /*
    static Constraint equal_angle(Workplane wrkpl,
            LineSegment2d line1, LineSegment2d line2, LineSegment2d line3, LineSegment2d line4,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    */
    static Constraint ratio(double value,
            Workplane wrkpl, LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint symmetric(Workplane wrkpl,
            Point3d p1, Point3d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint symmetric(Workplane wrkpl,
            Point2d p1, Point2d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint symmetric(Workplane wrkpl,
            Point2d p1, Point2d p2, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint symmetric_H(Workplane wrkpl,
            Point2d p1, Point2d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint symmetric_V(Workplane wrkpl,
            Point2d p1, Point2d p2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint midpoint(
            Point3d p, LineSegment3d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint midpoint(Workplane wrkpl,
            Point2d p, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint orientation(
            Normal3d nrml1, Normal3d nrml2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint angle(Workplane wrkpl,  double value,
            LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint perpendicular(Workplane wrkpl,
            LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint parallel(
            LineSegment3d line1, LineSegment3d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint parallel(Workplane wrkpl,
            LineSegment2d line1, LineSegment2d line2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(
            ArcOfCircle arc, LineSegment2d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(
            Cubic cubic, LineSegment3d line,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint distance_proj(double value,
            Point3d p1, Point3d p2, Workplane wrkpl,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint dragged(
            Point3d p,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint dragged(Workplane wrkpl,
            Point2d p,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(Workplane wrkpl,
            ArcOfCircle c1, ArcOfCircle c2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(
            Cubic c1, Cubic c2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(Workplane wrkpl,
            ArcOfCircle c1, Cubic c2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
    static Constraint tangent(Workplane wrkpl,
            Cubic c1, ArcOfCircle c2,
            Slvs_hGroup group = USE_DEFAULT_GROUP)
        throw_entity_constructor;
};

class System : public Slvs_System {
public:
    System(int param_space, int entity_space, int constraint_space,
                int failed_space)
        throw(out_of_memory_exception);

    System(int space)
        throw(out_of_memory_exception);

    System()
        throw(out_of_memory_exception);

    ~System();

    Slvs_hGroup default_group;

    void add_param(Slvs_Param p)
        throw(not_enough_space_exception, invalid_value_exception);

    Param add_param(Slvs_hGroup group, double val)
        throw(not_enough_space_exception, invalid_value_exception);

    Param add_param(double val)
        throw(not_enough_space_exception, invalid_value_exception);

    void add_entity(Slvs_Entity p)
        throw(not_enough_space_exception, invalid_value_exception);

    Entity add_entity_with_next_handle(Slvs_Entity p)
        throw(not_enough_space_exception, invalid_value_exception);

    void add_constraint(Slvs_Constraint p)
        throw(not_enough_space_exception, invalid_value_exception);

    Slvs_Param *get_param(int i);

    void set_dragged(int i, Slvs_hParam param)
        throw(invalid_value_exception);

    void set_dragged(int i, Param param);

    void set_dragged(Point2d point);

    void set_dragged(Point3d point);

    %pythoncode %{
        __swig_setmethods__["dragged"] = set_dragged
        if _newclass: value = property(None, set_dragged)
    %}

    int solveFor(Slvs_hGroup hg);

    int solve();

    // entities

    Point2d add_point2d(Workplane workplane, Param u,
            Param v, Slvs_hGroup group = 0)
        throw_entity_constructor;

    Point3d add_point3d(Param x, Param y, Param z,
            Slvs_hGroup group = 0)
        throw_entity_constructor;



    int entity_type(int i) throw(invalid_value_exception);

#   define ENTITY_GETTER(type, typecode)  \
        type get_##type(int i)            \
            throw(invalid_value_exception, invalid_state_exception);
    ENTITY_GETTER(Point2d,       SLVS_E_POINT_IN_2D);
    ENTITY_GETTER(Point3d,       SLVS_E_POINT_IN_3D);
    ENTITY_GETTER(LineSegment2d, SLVS_E_LINE_SEGMENT);
    ENTITY_GETTER(LineSegment3d, SLVS_E_LINE_SEGMENT);
    ENTITY_GETTER(Normal3d,      SLVS_E_NORMAL_IN_3D);
    ENTITY_GETTER(Distance,      SLVS_E_DISTANCE);
    ENTITY_GETTER(Workplane,     SLVS_E_WORKPLANE);
    ENTITY_GETTER(Cubic,         SLVS_E_CUBIC);
    ENTITY_GETTER(Circle,        SLVS_E_CIRCLE);
    ENTITY_GETTER(ArcOfCircle,   SLVS_E_ARC_OF_CIRCLE);
#   undef ENTITY_GETTER
};
