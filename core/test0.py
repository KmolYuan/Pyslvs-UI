import sys, platform
py_nm = sys.version[0:sys.version.find(" ")][0:3]
#SLVS Version
if platform.system().lower()=="windows":
    if py_nm=="3.5": from kernel.py35w.slvs import *
elif platform.system().lower()=="linux":
    if py_nm=="3.4": from kernel.py34.slvs import *
    elif py_nm=="3.5": from kernel.py35.slvs import *
else: print("Python Version Not Support.")

def Multi_link(degree):
    #開始繪圖
    sys = System(500)
    #3D原點Point0
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)
    #XY法線
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)
    #工作平面
    Workplane1 = Workplane(Point0, Normal1)
    #2D原點Point1
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
    #Angle約束判斷
    if degree >= 180:
        other = -1
    else:
        other = 1
    #［曲柄］Point1-Point2長15mm
    p9 = sys.add_param(0.0)
    p10 = sys.add_param(20.0*other)
    Point2 = Point2d(Workplane1, p9, p10)
    Constraint.distance(15.0, Workplane1, Point1, Point2)
    Line1 = LineSegment2d(Workplane1, Point1, Point2)
    #第一組［呆鍊］Point3-Point4-Point5（Point3固定）
    #長度41.5-55.8-40.1mm
    p11 = sys.add_param(-38.0)
    p12 = sys.add_param(-7.8)
    Point3 = Point2d(Workplane1, p11, p12)
    Constraint.dragged(Workplane1, Point3)
    p13 = sys.add_param(-50.0)
    p14 = sys.add_param(30.0)
    Point4 = Point2d(Workplane1, p13, p14)
    p15 = sys.add_param(-70.0)
    p16 = sys.add_param(-15.0)
    Point5 = Point2d(Workplane1, p15, p16)
    Constraint.distance(41.5, Workplane1, Point3, Point4)
    Constraint.distance(55.8, Workplane1, Point4, Point5)
    Constraint.distance(40.1, Workplane1, Point3, Point5)
    #第二組［呆鍊］Point6-Point7-Point8
    #長度65.7-49.0-36.7mm
    p17 = sys.add_param(-50.0)
    p18 = sys.add_param(-50.0)
    Point6 = Point2d(Workplane1, p17, p18)
    p19 = sys.add_param(-10.0)
    p20 = sys.add_param(-90.0)
    Point7 = Point2d(Workplane1, p19, p20)
    p21 = sys.add_param(-20.0)
    p22 = sys.add_param(-40.0)
    Point8 = Point2d(Workplane1, p21, p22)
    Constraint.distance(65.7, Workplane1, Point6, Point7)
    Constraint.distance(49.0, Workplane1, Point7, Point8)
    Constraint.distance(36.7, Workplane1, Point6, Point8)
    #兩段［呆鍊-呆鍊］連接桿
    #Point5-Point6長39.4mm
    #Point3-Point8長39.3mm
    Constraint.distance(39.4, Workplane1, Point5, Point6)
    Constraint.distance(39.3, Workplane1, Point3, Point8)
    #兩段［區柄-呆鍊］連接桿
    #Point2-Point4長50.0mm
    #Point2-Point8長61.9mm
    Constraint.distance(50.0, Workplane1, Point2, Point4)
    Constraint.distance(61.9, Workplane1, Point2, Point8)
    #水平輔助Line0
    p23 = sys.add_param(20.0)
    p24 = sys.add_param(0.0)
    Point9 = Point2d(Workplane1, p23, p24)
    Constraint.dragged(Workplane1, Point9)
    Line0 = LineSegment2d(Workplane1, Point1, Point9)
    #區柄角度（手動項目務必放最後）
    Constraint.angle(Workplane1, degree, Line1, Line0, False)
    #以下解題
    sys.solve()
    if (sys.result == SLVS_RESULT_OKAY):
        #回傳Point7
        x = sys.get_param(19).val
        y = sys.get_param(20).val
        return x, y
    else: return None

print(Multi_link(45))
