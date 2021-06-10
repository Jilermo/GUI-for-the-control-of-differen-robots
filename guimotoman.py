import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.widgets import Slider,CheckButtons,Button
from robolink import *

fig, ax = plt.subplots()
plt.subplots_adjust(left=0,bottom=0.28,right=1,top=1)
ax = plt.axes(projection = "3d")

def mmatrix(*matrices):
    n=0
    for m in matrices:
        if (n==0):
            ma=m
            n=n+1
        elif (n==1):
            r=np.dot(ma,m)
            n=n+1
        else:
            r=np.dot(r,m)
    return r
    


def dibujar():
    plt.draw()
    plt.pause(0.001)


def sind(t):
    res=np.sin(t*np.pi/180)
    return res

def cosd(t):
    res=np.cos(t*np.pi/180)
    return res

def setaxis(lim=2):
    x1=-lim
    x2=lim
    y1=-lim
    y2=lim
    z1=-lim
    z2=lim
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30,azim=40)
    ax.grid(True)

def sistemafijo(rango=1):
    x=[0,1*rango]
    y=[0,1*rango]
    z=[0,1*rango]
    ax.plot3D(x,[0,0],[0,0],color='red')
    ax.plot3D([0,0],y,[0,0],color='green')
    ax.plot3D([0,0],[0,0],z,color='blue')


def rotax(t):
    Rx=np.array(([1,0,0,0],[0,cosd(t),-sind(t),0],[0,sind(t),cosd(t),0],[0,0,0,1]))
    return Rx

def rotay(t):
    Ry=np.array(([cosd(t),0,sind(t),0],[0,1,0,0],[-sind(t),0,cosd(t),0],[0,0,0,1]))
    return Ry

def rotaz(t):
    Rz=np.array(([cosd(t),-sind(t),0,0],[sind(t),cosd(t),0,0],[0,0,1,0],[0,0,0,1]))
    return Rz

def rotaxf(t,r):
    px=r[0,3]
    py=r[1,3]
    pz=r[2,3]
    Rx=np.array(([1,0,0,0],[0,cosd(t),-sind(t),0],[0,sind(t),cosd(t),0],[0,0,0,1]))
    Rx=np.dot(Rx,r)
    Rx[0,3]=px
    Rx[1,3]=py
    Rx[2,3]=pz
    return Rx

def rotayf(t,r):
    px=r[0,3]
    py=r[1,3]
    pz=r[2,3]
    Ry=np.array(([cosd(t),0,sind(t),0],[0,1,0,0],[-sind(t),0,cosd(t),0],[0,0,0,1]))
    Ry=np.dot(Ry,r)
    Ry[0,3]=px
    Ry[1,3]=py
    Ry[2,3]=pz
    return Ry

def rotazf(t,r):
    px=r[0,3]
    py=r[1,3]
    pz=r[2,3]
    Rz=np.array(([cosd(t),-sind(t),0,0],[sind(t),cosd(t),0,0],[0,0,1,0],[0,0,0,1]))
    Rz=np.dot(Rz,r)
    Rz[0,3]=px
    Rz[1,3]=py
    Rz[2,3]=pz
    return Rz


def trasx(Dx):
    Tx=np.array(([[1,0,0,Dx],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))
    return Tx

def trasy(Dy):
    Ty=np.array(([[1,0,0,0],[0,1,0,Dy],[0,0,1,0],[0,0,0,1]]))
    return Ty

def trasz(Dz):
    Tz=np.array(([[1,0,0,0],[0,1,0,0],[0,0,1,Dz],[0,0,0,1]]))
    return Tz

def minv(R):
    r=np.zeros((4,4))
    a=np.zeros((3,3))
    p=np.zeros((3,1))
    a[0,0]=R[0,0]
    a[0,1]=R[0,1]
    a[0,2]=R[0,2]
    a[1,0]=R[1,0]
    a[1,1]=R[1,1]
    a[1,2]=R[1,2]
    a[2,0]=R[2,0]
    a[2,1]=R[2,1]
    a[2,2]=R[2,2]
    a=np.transpose(a)
    r[0,0]=a[0,0]
    r[0,1]=a[0,1]
    r[0,2]=a[0,2]
    r[1,0]=a[1,0]
    r[1,1]=a[1,1]
    r[1,2]=a[1,2]
    r[2,0]=a[2,0]
    r[2,1]=a[2,1]
    r[2,2]=a[2,2]
    a=-1*a
    p[0,0]=R[0,3]
    p[1,0]=R[1,3]
    p[2,0]=R[2,3]
    p1=np.dot(a,p)
    r[0,3]=p1[0,0]
    r[1,3]=p1[1,0]
    r[2,3]=p1[2,0]
    r[3,3]=1
    return r
    


def sistemamovil(r,rango=1):
    ux=r[0,0]
    uy=r[1,0]
    uz=r[2,0]
    vx=r[0,1]
    vy=r[1,1]
    vz=r[2,1]
    wx=r[0,2]
    wy=r[1,2]
    wz=r[2,2]

    px=r[0,3]
    py=r[1,3]
    pz=r[2,3]
    
    ax.plot3D([px,px+ux*rango],[py,py+uy*rango],[pz,pz+uz*rango],color='red') #Dibuja eje movil u
    ax.plot3D([px,px+vx*rango],[py,py+vy*rango],[pz,pz+vz*rango],color='green') #Dibuja eje movil v
    ax.plot3D([px,px+wx*rango],[py,py+wy*rango],[pz,pz+wz*rango],color='blue') #Dibuja eje movil w
    
def ppp(d1,d2,d3):
    t0=np.eye(4)
    t01=trasz(d1)@rotax(-90)
    t12=trasz(d2)@rotax(-90)@rotay(90)
    t23=trasz(d3)@rotaz(180)
    t02=t01@t12
    t03=t02@t23
    sistemafijo()
    sistemamovil(t01)
    sistemamovil(t02)
    sistemamovil(t03)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')


def rpp(t1,d2,d3):
    t0=np.eye(4)
    t01=rotaz(t1)
    t12=trasz(d2)
    t23=rotay(90)@trasz(d3)
    t02=t01@t12
    t03=t02@t23
    sistemafijo()
    sistemamovil(t01)
    sistemamovil(t02)
    sistemamovil(t03)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')


def rrp(t1,t2,d3):
    t0=np.eye(4)
    t01=rotaz(t1)
    t12=trasz(5)@rotay(90)@rotaz(90)@rotaz(t2)
    t23=rotay(90)@rotaz(-90)@trasz(d3)
    t02=t01@t12
    t03=t02@t23
    sistemafijo()
    sistemamovil(t01)
    sistemamovil(t02)
    sistemamovil(t03)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')



def rrr(t1,t2,t3):
    t0=np.eye(4)
    t01=rotaz(t1)
    t12=trasz(4)@rotax(90)@rotaz(t2)
    t23=trasx(4)@rotaz(t3)
    t34=trasx(4)@rotay(90)@rotaz(-90)
    t02=t01@t12
    t03=t02@t23
    t04=t03@t34
    sistemafijo()
    sistemamovil(t01)
    sistemamovil(t02)
    sistemamovil(t03)
    sistemamovil(t04)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')
    ax.plot3D([t03[0,3],t04[0,3]],[t03[1,3],t04[1,3]],[t03[2,3],t04[2,3]],color='red')


def scara(t1,t2,d3,t4):
    t0=np.eye(4)
    t01=rotaz(t1)@trasz(4)
    t12=trasx(4)
    t23=rotaz(t2)@trasz(-1)
    t34=trasx(4)@rotax(180)@rotaz(-90)
    t45=trasz(d3)
    t56=rotaz(t4)@trasz(1)
    t02=t01@t12
    t03=t02@t23
    t04=t03@t34
    t05=t04@t45
    t06=t05@t56
    sistemafijo()
    sistemamovil(t01)
    sistemamovil(t02)
    sistemamovil(t03)
    sistemamovil(t04)
    sistemamovil(t05)
    sistemamovil(t06)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')
    ax.plot3D([t03[0,3],t04[0,3]],[t03[1,3],t04[1,3]],[t03[2,3],t04[2,3]],color='red')
    ax.plot3D([t04[0,3],t05[0,3]],[t04[1,3],t05[1,3]],[t04[2,3],t05[2,3]],color='red')
    ax.plot3D([t05[0,3],t06[0,3]],[t05[1,3],t06[1,3]],[t05[2,3],t06[2,3]],color='red')


def cobras800(t1,t2,d3,t4):
    t0=np.eye(4)
    t01=rotaz(t1)@trasz(342)
    t12=trasx(425)
    t23=rotaz(t2)@trasz(56)
    t34=trasx(375)
    t45=trasz(-210)@trasz(d3)
    t56=rotax(180)@rotaz(-180)@rotaz(t4)
    t02=t01@t12
    t03=t02@t23
    t04=t03@t34
    t05=t04@t45
    t06=t05@t56
    sistemafijo(100)
    #sistemamovil(t01,100)
    #sistemamovil(t02,100)
    sistemamovil(t03,100)
    #sistemamovil(t04,100)
    #sistemamovil(t05,100)
    sistemamovil(t06,100)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')
    ax.plot3D([t03[0,3],t04[0,3]],[t03[1,3],t04[1,3]],[t03[2,3],t04[2,3]],color='red')
    ax.plot3D([t04[0,3],t05[0,3]],[t04[1,3],t05[1,3]],[t04[2,3],t05[2,3]],color='red')
    ax.plot3D([t05[0,3],t06[0,3]],[t05[1,3],t06[1,3]],[t05[2,3],t06[2,3]],color='red')


def ur5(t1,t2,t3,t4,t5,t6):
    t0=np.eye(4)
    t01=rotaz(t1)@trasz(89.2)#
    t12=trasy(-134.2)@rotax(90)@rotaz(t2)#
    t23=trasy(425)
    t34=trasz(-118.45)@rotaz(t3)#
    t45=trasx(392.25)@rotaz(t4)#
    t56=trasz(94.75)@rotax(-90)@rotaz(t5)#
    t67=trasz(94.75)
    t78=trasx(82.5)@rotay(90)@rotaz(-90)@rotaz(t6)#
    t02=t01@t12
    t03=t02@t23
    t04=t03@t34
    t05=t04@t45
    t06=t05@t56
    t07=t06@t67
    t08=t07@t78
    sistemafijo(100)
    #sistemamovil(t01,100)
    sistemamovil(t02,100)
    sistemamovil(t03,100)
    #sistemamovil(t04,100)
    sistemamovil(t05,100)
    sistemamovil(t06,100)
    sistemamovil(t07,100)
    #sistemamovil(t08,100)
    ax.plot3D([t0[0,3],t01[0,3]],[t0[1,3],t01[1,3]],[t0[2,3],t01[2,3]],color='red')
    ax.plot3D([t01[0,3],t02[0,3]],[t01[1,3],t02[1,3]],[t01[2,3],t02[2,3]],color='red')
    ax.plot3D([t02[0,3],t03[0,3]],[t02[1,3],t03[1,3]],[t02[2,3],t03[2,3]],color='red')
    ax.plot3D([t03[0,3],t04[0,3]],[t03[1,3],t04[1,3]],[t03[2,3],t04[2,3]],color='red')
    ax.plot3D([t04[0,3],t05[0,3]],[t04[1,3],t05[1,3]],[t04[2,3],t05[2,3]],color='red')
    ax.plot3D([t05[0,3],t06[0,3]],[t05[1,3],t06[1,3]],[t05[2,3],t06[2,3]],color='red')
    ax.plot3D([t06[0,3],t07[0,3]],[t06[1,3],t07[1,3]],[t06[2,3],t07[2,3]],color='red')
    ax.plot3D([t07[0,3],t08[0,3]],[t07[1,3],t08[1,3]],[t07[2,3],t08[2,3]],color='red')


def motoman(tb,t1a,t2a,t3a,t4a,t5a,t6a,t7a,t1b,t2b,t3b,t4b,t5b,t6b,t7b):
    T0=np.eye(4)
    Ti=rotaz(tb)
    Ti1=Ti@trasz(8)
    Ti2=Ti1@trasx(1.57)
    Ti3=Ti2@trasy(2.5)@rotax(-90)
    Tib3=Ti2@trasy(-2.5)@rotax(90)
    
    T01=Ti3@rotaz(270)@rotaz(t1a)@trasz(.3);
    T12=trasx(-1.09)
    T23=trasz(2.5)
    T34=trasx(1.09)@rotay(90)@rotaz(t2a)
    T45=rotay(-90)@trasx(1.2)
    T56=trasz(1)
    T67=trasx(-1.2)
    T78=trasz(0.45)@rotaz(t3a)
    T89=trasz(2.225)
    T910=trasx(1.04)
    T1011=trasz(1.225)
    T1112=trasx(-1.04)@rotay(90)@rotaz(t4a)
    T1213=rotay(-90)@trasx(-0.98)
    T1314=trasz(1.4)
    T1415=trasx(0.98)
    T1516=trasz(0.7)@rotaz(t5a)
    T1617=trasz(0.7)
    T1718=trasx(-0.86)
    T1819=trasz(1.4)
    T1920=trasx(0.86)@rotay(90)@rotaz(t6a)
    T2021=rotay(-90)@trasx(0.8)
    T2122=trasz(0.9)
    T2223=trasx(-0.8)
    T2324=trasz(0.9)@rotaz(90)@rotaz(t7a)
    T02=T01@T12
    T03=T02@T23
    T04=T03@T34
    T05=T04@T45
    T06=T05@T56
    T07=T06@T67
    T08=T07@T78
    T09=T08@T89
    T10=T09@T910
    T11=T10@T1011
    T12=T11@T1112
    T13=T12@T1213
    T14=T13@T1314
    T15=T14@T1415
    T16=T15@T1516
    T17=T16@T1617
    T18=T17@T1718
    T19=T18@T1819
    T20=T19@T1920
    T21=T20@T2021
    T22=T21@T2122
    T23=T22@T2223
    T24=T23@T2324
    print(T24)



    Tb01=Tib3@rotaz(270)@rotaz(t1b)@trasz(0.3)
    Tb12=trasx(-1.09)
    Tb23=trasz(2.5)
    TB34=trasx(1.09)@rotay(90)@rotaz(t2b)
    Tb45=rotay(-90)@trasx(1.2)
    Tb56=trasz(1)
    Tb67=trasx(-1.2) 
    Tb78=trasz(0.45)@rotaz(t3b)
    Tb89=trasz(2.225)
    TB910=trasx(1.04)
    Tb1011=trasz(1.225)
    Tb1112=trasx(-1.04)@rotay(90)@rotaz(t4b)
    Tb1213=rotay(-90)@trasx(-0.98)
    Tb1314=trasz(1.4)
    Tb1415=trasx(0.98)
    Tb1516=trasz(0.7)@rotaz(t5b)
    Tb1617=trasz(0.7)
    Tb1718=trasx(-0.86)
    Tb1819=trasz(1.4)
    Tb1920=trasx(0.86)@rotay(90)@rotaz(t6b)
    Tb2021=rotay(-90)@trasx(0.8)
    Tb2122=trasz(0.9)
    Tb2223=trasx(-0.8)
    Tb2324=trasz(0.9)@rotaz(90)@rotaz(t7b)

    Tb02=Tb01@Tb12
    Tb03=Tb02@Tb23
    Tb04=Tb03@TB34
    Tb05=Tb04@Tb45
    Tb06=Tb05@Tb56
    Tb07=Tb06@Tb67
    Tb08=Tb07@Tb78
    Tb09=Tb08@Tb89
    Tb10=Tb09@TB910
    Tb11=Tb10@Tb1011
    Tb12=Tb11@Tb1112
    Tb13=Tb12@Tb1213
    Tb14=Tb13@Tb1314
    Tb15=Tb14@Tb1415
    Tb16=Tb15@Tb1516
    Tb17=Tb16@Tb1617
    Tb18=Tb17@Tb1718
    Tb19=Tb18@Tb1819
    Tb20=Tb19@Tb1920
    Tb21=Tb20@Tb2021
    Tb22=Tb21@Tb2122
    Tb23=Tb22@Tb2223
    Tb24=Tb23@Tb2324

    sistemafijo()
    sistemamovil(T0)
    sistemamovil(T01)
    sistemamovil(T04)
    sistemamovil(T08)
    sistemamovil(T12)
    sistemamovil(T16)
    sistemamovil(T20)
    sistemamovil(T24)
    sistemamovil(T0)
    sistemamovil(Tb01)
    sistemamovil(Tb04)
    sistemamovil(Tb08)
    sistemamovil(Tb12)
    sistemamovil(Tb16)
    sistemamovil(Tb20)
    sistemamovil(Tb24)

    ax.plot3D([Ti[0,3], Ti1[0,3]], [Ti[1,3], Ti1[1,3]], [Ti[2,3], Ti1[2,3]],color='red')

    ax.plot3D([Ti1[0,3], Ti2[0,3]], [Ti1[1,3], Ti2[1,3]], [Ti1[2,3], Ti2[2,3]],color='red')
    ax.plot3D([Ti2[0,3], Ti3[0,3]], [Ti2[1,3], Ti3[1,3]], [Ti2[2,3], Ti3[2,3]],color='red')

    ax.plot3D([Ti3[0,3], T01[0,3]], [Ti3[1,3], T01[1,3]], [Ti3[2,3], T01[2,3]],color='red')
    ax.plot3D([T01[0,3], T02[0,3]], [T01[1,3], T02[1,3]], [T01[2,3], T02[2,3]],color='red')
    ax.plot3D([T02[0,3], T03[0,3]], [T02[1,3], T03[1,3]], [T02[2,3], T03[2,3]],color='red')
    ax.plot3D([T03[0,3], T04[0,3]], [T03[1,3], T04[1,3]], [T03[2,3], T04[2,3]],color='red')
    ax.plot3D([T04[0,3], T05[0,3]], [T04[1,3], T05[1,3]], [T04[2,3], T05[2,3]],color='red')
    ax.plot3D([T05[0,3], T06[0,3]], [T05[1,3], T06[1,3]], [T05[2,3], T06[2,3]],color='red')
    ax.plot3D([T06[0,3], T07[0,3]], [T06[1,3], T07[1,3]], [T06[2,3], T07[2,3]],color='red')
    ax.plot3D([T07[0,3], T08[0,3]], [T07[1,3], T08[1,3]], [T07[2,3], T08[2,3]],color='red')
    ax.plot3D([T08[0,3], T09[0,3]], [T08[1,3], T09[1,3]], [T08[2,3], T09[2,3]],color='red')
    ax.plot3D([T09[0,3], T10[0,3]], [T09[1,3], T10[1,3]], [T09[2,3], T10[2,3]],color='red')
    ax.plot3D([T10[0,3], T11[0,3]], [T10[1,3], T11[1,3]], [T10[2,3], T11[2,3]],color='red')
    ax.plot3D([T11[0,3], T12[0,3]], [T11[1,3], T12[1,3]], [T11[2,3], T12[2,3]],color='red')
    ax.plot3D([T12[0,3], T13[0,3]], [T12[1,3], T13[1,3]], [T12[2,3], T13[2,3]],color='red')
    ax.plot3D([T13[0,3], T14[0,3]], [T13[1,3], T14[1,3]], [T13[2,3], T14[2,3]],color='red')
    ax.plot3D([T14[0,3], T15[0,3]], [T14[1,3], T15[1,3]], [T14[2,3], T15[2,3]],color='red')
    ax.plot3D([T15[0,3], T16[0,3]], [T15[1,3], T16[1,3]], [T15[2,3], T16[2,3]],color='red')
    ax.plot3D([T16[0,3], T17[0,3]], [T16[1,3], T17[1,3]], [T16[2,3], T17[2,3]],color='red')
    ax.plot3D([T17[0,3], T18[0,3]], [T17[1,3], T18[1,3]], [T17[2,3], T18[2,3]],color='red')
    ax.plot3D([T18[0,3], T19[0,3]], [T18[1,3], T19[1,3]], [T18[2,3], T19[2,3]],color='red')
    ax.plot3D([T19[0,3], T20[0,3]], [T19[1,3], T20[1,3]], [T19[2,3], T20[2,3]],color='red')
    ax.plot3D([T20[0,3], T21[0,3]], [T20[1,3], T21[1,3]], [T20[2,3], T21[2,3]],color='red')
    ax.plot3D([T21[0,3], T22[0,3]], [T21[1,3], T22[1,3]], [T21[2,3], T22[2,3]],color='red')
    ax.plot3D([T22[0,3], T23[0,3]], [T22[1,3], T23[1,3]], [T22[2,3], T23[2,3]],color='red')
    ax.plot3D([T23[0,3], T24[0,3]], [T23[1,3], T24[1,3]], [T23[2,3], T24[2,3]],color='red')

    ax.plot3D([Ti[0,3], Ti1[0,3]], [Ti[1,3], Ti1[1,3]], [Ti[2,3], Ti1[2,3]],color='red')

    ax.plot3D([Ti1[0,3], Ti2[0,3]], [Ti1[1,3], Ti2[1,3]], [Ti1[2,3], Ti2[2,3]],color='red')
    ax.plot3D([Ti2[0,3], Tib3[0,3]], [Ti2[1,3], Tib3[1,3]], [Ti2[2,3], Tib3[2,3]],color='red')

    ax.plot3D([Tib3[0,3], Tb01[0,3]], [Tib3[1,3], Tb01[1,3]], [Tib3[2,3], Tb01[2,3]],color='red')
    ax.plot3D([Tb01[0,3], Tb02[0,3]], [Tb01[1,3], Tb02[1,3]], [Tb01[2,3], Tb02[2,3]],color='red')
    ax.plot3D([Tb02[0,3], Tb03[0,3]], [Tb02[1,3], Tb03[1,3]], [Tb02[2,3], Tb03[2,3]],color='red')
    ax.plot3D([Tb03[0,3], Tb04[0,3]], [Tb03[1,3], Tb04[1,3]], [Tb03[2,3], Tb04[2,3]],color='red')
    ax.plot3D([Tb04[0,3], Tb05[0,3]], [Tb04[1,3], Tb05[1,3]], [Tb04[2,3], Tb05[2,3]],color='red')
    ax.plot3D([Tb05[0,3], Tb06[0,3]], [Tb05[1,3], Tb06[1,3]], [Tb05[2,3], Tb06[2,3]],color='red')
    ax.plot3D([Tb06[0,3], Tb07[0,3]], [Tb06[1,3], Tb07[1,3]], [Tb06[2,3], Tb07[2,3]],color='red')
    ax.plot3D([Tb07[0,3], Tb08[0,3]], [Tb07[1,3], Tb08[1,3]], [Tb07[2,3], Tb08[2,3]],color='red')
    ax.plot3D([Tb08[0,3], Tb09[0,3]], [Tb08[1,3], Tb09[1,3]], [Tb08[2,3], Tb09[2,3]],color='red')
    ax.plot3D([Tb09[0,3], Tb10[0,3]], [Tb09[1,3], Tb10[1,3]], [Tb09[2,3], Tb10[2,3]],color='red')
    ax.plot3D([Tb10[0,3], Tb11[0,3]], [Tb10[1,3], Tb11[1,3]], [Tb10[2,3], Tb11[2,3]],color='red')
    ax.plot3D([Tb11[0,3], Tb12[0,3]], [Tb11[1,3], Tb12[1,3]], [Tb11[2,3], Tb12[2,3]],color='red')
    ax.plot3D([Tb12[0,3], Tb13[0,3]], [Tb12[1,3], Tb13[1,3]], [Tb12[2,3], Tb13[2,3]],color='red')
    ax.plot3D([Tb13[0,3], Tb14[0,3]], [Tb13[1,3], Tb14[1,3]], [Tb13[2,3], Tb14[2,3]],color='red')
    ax.plot3D([Tb14[0,3], Tb15[0,3]], [Tb14[1,3], Tb15[1,3]], [Tb14[2,3], Tb15[2,3]],color='red')
    ax.plot3D([Tb15[0,3], Tb16[0,3]], [Tb15[1,3], Tb16[1,3]], [Tb15[2,3], Tb16[2,3]],color='red')
    ax.plot3D([Tb16[0,3], Tb17[0,3]], [Tb16[1,3], Tb17[1,3]], [Tb16[2,3], Tb17[2,3]],color='red')
    ax.plot3D([Tb17[0,3], Tb18[0,3]], [Tb17[1,3], Tb18[1,3]], [Tb17[2,3], Tb18[2,3]],color='red')
    ax.plot3D([Tb18[0,3], Tb19[0,3]], [Tb18[1,3], Tb19[1,3]], [Tb18[2,3], Tb19[2,3]],color='red')
    ax.plot3D([Tb19[0,3], Tb20[0,3]], [Tb19[1,3], Tb20[1,3]], [Tb19[2,3], Tb20[2,3]],color='red')
    ax.plot3D([Tb20[0,3], Tb21[0,3]], [Tb20[1,3], Tb21[1,3]], [Tb20[2,3], Tb21[2,3]],color='red')
    ax.plot3D([Tb21[0,3], Tb22[0,3]], [Tb21[1,3], Tb22[1,3]], [Tb21[2,3], Tb22[2,3]],color='red')
    ax.plot3D([Tb22[0,3], Tb23[0,3]], [Tb22[1,3], Tb23[1,3]], [Tb22[2,3], Tb23[2,3]],color='red')
    ax.plot3D([Tb23[0,3], Tb24[0,3]], [Tb23[1,3], Tb24[1,3]], [Tb23[2,3], Tb24[2,3]],color='red')


def accmotoman(tb,t1a,t2a,t3a,t4a,t5a,t6a,t7a,t1b,t2b,t3b,t4b,t5b,t6b,t7b):
    T0=np.eye(4)
    Ti=trasz(893.5)
    Ti1=Ti@trasx(92.5)@rotaz(tb)
    Ti2=Ti1@trasx(100)@trasz(306.5)
    Ti3=Ti2@rotax(-90)@rotaz(-180)@rotaz(t1a)@trasz(265)
    Tib3=Ti2@rotax(90)@rotaz(-180)@rotaz(t1b)@trasz(265)
    
    T01=Ti3@rotax(-90)@rotaz(t2a)
    T12=trasz(-80)
    T23=trasy(-90)
    T34=trasz(80)
    T45=trasy(-90)@rotax(90)@rotaz(t3a)
    T56=trasz(90)
    T67=trasy(-80)
    T78=trasz(90)
    T89=trasy(80)@rotax(-90)@rotaz(t4a)
    T910=trasz(80)
    T1011=trasy(-90)
    T1112=trasz(-80)
    T1213=trasy(-90)@rotax(90)@rotaz(t5a)
    T1314=trasz(90)
    T1415=trasy(80)
    T1516=trasz(90)
    T1617=trasy(-80)@rotax(-90)@rotaz(t6a)
    T1718=trasz(-80)
    T1819=trasy(-87.5)
    T1920=trasz(80)
    T2021=trasy(-87.5)@rotax(90)@rotaz(t7a)
    T02=T01@T12
    T03=T02@T23
    T04=T03@T34
    T05=T04@T45
    T06=T05@T56
    T07=T06@T67
    T08=T07@T78
    T09=T08@T89
    T10=T09@T910
    T11=T10@T1011
    T12=T11@T1112
    T13=T12@T1213
    T14=T13@T1314
    T15=T14@T1415
    T16=T15@T1516
    T17=T16@T1617
    T18=T17@T1718
    T19=T18@T1819
    T20=T19@T1920
    T21=T20@T2021
    print("derecho ++++++")
    print(T21)


    Tb01=Tib3@rotax(-90)@rotaz(t2b)
    Tb12=trasz(-80)
    Tb23=trasy(-90)
    Tb34=trasz(80)
    Tb45=trasy(-90)@rotax(90)@rotaz(t3b)
    Tb56=trasz(90)
    Tb67=trasy(-80)
    Tb78=trasz(90)
    Tb89=trasy(80)@rotax(-90)@rotaz(t4b)
    Tb910=trasz(80)
    Tb1011=trasy(-90)
    Tb1112=trasz(-80)
    Tb1213=trasy(-90)@rotax(90)@rotaz(t5b)
    Tb1314=trasz(90)
    Tb1415=trasy(80)
    Tb1516=trasz(90)
    Tb1617=trasy(-80)@rotax(-90)@rotaz(t6b)
    Tb1718=trasz(-80)
    Tb1819=trasy(-87.5)
    Tb1920=trasz(80)
    Tb2021=trasy(-87.5)@rotax(90)@rotaz(t7b)
    
    

    Tb02=Tb01@Tb12
    Tb03=Tb02@Tb23
    Tb04=Tb03@Tb34
    Tb05=Tb04@Tb45
    Tb06=Tb05@Tb56
    Tb07=Tb06@Tb67
    Tb08=Tb07@Tb78
    Tb09=Tb08@Tb89
    Tb10=Tb09@Tb910
    Tb11=Tb10@Tb1011
    Tb12=Tb11@Tb1112
    Tb13=Tb12@Tb1213
    Tb14=Tb13@Tb1314
    Tb15=Tb14@Tb1415
    Tb16=Tb15@Tb1516
    Tb17=Tb16@Tb1617
    Tb18=Tb17@Tb1718
    Tb19=Tb18@Tb1819
    Tb20=Tb19@Tb1920
    Tb21=Tb20@Tb2021
    print("Izquierdo ++++++")
    print(Tb21)

    sistemafijo(100)
    sistemamovil(T0,100)
    sistemamovil(T01,100)
    sistemamovil(T05,100)
    sistemamovil(T09,100)
    sistemamovil(T13,100)
    sistemamovil(T17,100)
    sistemamovil(T21,100)
    sistemamovil(Tb01,100)
    sistemamovil(Tb05,100)
    sistemamovil(Tb09,100)
    sistemamovil(Tb13,100)
    sistemamovil(Tb17,100)
    sistemamovil(Tb21,100)

    ax.plot3D([T0[0,3], Ti[0,3]], [T0[1,3], Ti[1,3]], [T0[2,3], Ti[2,3]],color='red')


    ax.plot3D([Ti[0,3], Ti1[0,3]], [Ti[1,3], Ti1[1,3]], [Ti[2,3], Ti1[2,3]],color='red')

    ax.plot3D([Ti1[0,3], Ti2[0,3]], [Ti1[1,3], Ti2[1,3]], [Ti1[2,3], Ti2[2,3]],color='red')
    ax.plot3D([Ti2[0,3], Ti3[0,3]], [Ti2[1,3], Ti3[1,3]], [Ti2[2,3], Ti3[2,3]],color='red')

    ax.plot3D([Ti3[0,3], T01[0,3]], [Ti3[1,3], T01[1,3]], [Ti3[2,3], T01[2,3]],color='red')
    ax.plot3D([T01[0,3], T02[0,3]], [T01[1,3], T02[1,3]], [T01[2,3], T02[2,3]],color='red')
    ax.plot3D([T02[0,3], T03[0,3]], [T02[1,3], T03[1,3]], [T02[2,3], T03[2,3]],color='red')
    ax.plot3D([T03[0,3], T04[0,3]], [T03[1,3], T04[1,3]], [T03[2,3], T04[2,3]],color='red')
    ax.plot3D([T04[0,3], T05[0,3]], [T04[1,3], T05[1,3]], [T04[2,3], T05[2,3]],color='red')
    ax.plot3D([T05[0,3], T06[0,3]], [T05[1,3], T06[1,3]], [T05[2,3], T06[2,3]],color='red')
    ax.plot3D([T06[0,3], T07[0,3]], [T06[1,3], T07[1,3]], [T06[2,3], T07[2,3]],color='red')
    ax.plot3D([T07[0,3], T08[0,3]], [T07[1,3], T08[1,3]], [T07[2,3], T08[2,3]],color='red')
    ax.plot3D([T08[0,3], T09[0,3]], [T08[1,3], T09[1,3]], [T08[2,3], T09[2,3]],color='red')
    ax.plot3D([T09[0,3], T10[0,3]], [T09[1,3], T10[1,3]], [T09[2,3], T10[2,3]],color='red')
    ax.plot3D([T10[0,3], T11[0,3]], [T10[1,3], T11[1,3]], [T10[2,3], T11[2,3]],color='red')
    ax.plot3D([T11[0,3], T12[0,3]], [T11[1,3], T12[1,3]], [T11[2,3], T12[2,3]],color='red')
    ax.plot3D([T12[0,3], T13[0,3]], [T12[1,3], T13[1,3]], [T12[2,3], T13[2,3]],color='red')
    ax.plot3D([T13[0,3], T14[0,3]], [T13[1,3], T14[1,3]], [T13[2,3], T14[2,3]],color='red')
    ax.plot3D([T14[0,3], T15[0,3]], [T14[1,3], T15[1,3]], [T14[2,3], T15[2,3]],color='red')
    ax.plot3D([T15[0,3], T16[0,3]], [T15[1,3], T16[1,3]], [T15[2,3], T16[2,3]],color='red')
    ax.plot3D([T16[0,3], T17[0,3]], [T16[1,3], T17[1,3]], [T16[2,3], T17[2,3]],color='red')
    ax.plot3D([T17[0,3], T18[0,3]], [T17[1,3], T18[1,3]], [T17[2,3], T18[2,3]],color='red')
    ax.plot3D([T18[0,3], T19[0,3]], [T18[1,3], T19[1,3]], [T18[2,3], T19[2,3]],color='red')
    ax.plot3D([T19[0,3], T20[0,3]], [T19[1,3], T20[1,3]], [T19[2,3], T20[2,3]],color='red')
    ax.plot3D([T20[0,3], T21[0,3]], [T20[1,3], T21[1,3]], [T20[2,3], T21[2,3]],color='red')

    ax.plot3D([Ti[0,3], Ti1[0,3]], [Ti[1,3], Ti1[1,3]], [Ti[2,3], Ti1[2,3]],color='red')

    ax.plot3D([Ti1[0,3], Ti2[0,3]], [Ti1[1,3], Ti2[1,3]], [Ti1[2,3], Ti2[2,3]],color='red')
    ax.plot3D([Ti2[0,3], Tib3[0,3]], [Ti2[1,3], Tib3[1,3]], [Ti2[2,3], Tib3[2,3]],color='red')

    ax.plot3D([Tib3[0,3], Tb01[0,3]], [Tib3[1,3], Tb01[1,3]], [Tib3[2,3], Tb01[2,3]],color='red')
    ax.plot3D([Tb01[0,3], Tb02[0,3]], [Tb01[1,3], Tb02[1,3]], [Tb01[2,3], Tb02[2,3]],color='red')
    ax.plot3D([Tb02[0,3], Tb03[0,3]], [Tb02[1,3], Tb03[1,3]], [Tb02[2,3], Tb03[2,3]],color='red')
    ax.plot3D([Tb03[0,3], Tb04[0,3]], [Tb03[1,3], Tb04[1,3]], [Tb03[2,3], Tb04[2,3]],color='red')
    ax.plot3D([Tb04[0,3], Tb05[0,3]], [Tb04[1,3], Tb05[1,3]], [Tb04[2,3], Tb05[2,3]],color='red')
    ax.plot3D([Tb05[0,3], Tb06[0,3]], [Tb05[1,3], Tb06[1,3]], [Tb05[2,3], Tb06[2,3]],color='red')
    ax.plot3D([Tb06[0,3], Tb07[0,3]], [Tb06[1,3], Tb07[1,3]], [Tb06[2,3], Tb07[2,3]],color='red')
    ax.plot3D([Tb07[0,3], Tb08[0,3]], [Tb07[1,3], Tb08[1,3]], [Tb07[2,3], Tb08[2,3]],color='red')
    ax.plot3D([Tb08[0,3], Tb09[0,3]], [Tb08[1,3], Tb09[1,3]], [Tb08[2,3], Tb09[2,3]],color='red')
    ax.plot3D([Tb09[0,3], Tb10[0,3]], [Tb09[1,3], Tb10[1,3]], [Tb09[2,3], Tb10[2,3]],color='red')
    ax.plot3D([Tb10[0,3], Tb11[0,3]], [Tb10[1,3], Tb11[1,3]], [Tb10[2,3], Tb11[2,3]],color='red')
    ax.plot3D([Tb11[0,3], Tb12[0,3]], [Tb11[1,3], Tb12[1,3]], [Tb11[2,3], Tb12[2,3]],color='red')
    ax.plot3D([Tb12[0,3], Tb13[0,3]], [Tb12[1,3], Tb13[1,3]], [Tb12[2,3], Tb13[2,3]],color='red')
    ax.plot3D([Tb13[0,3], Tb14[0,3]], [Tb13[1,3], Tb14[1,3]], [Tb13[2,3], Tb14[2,3]],color='red')
    ax.plot3D([Tb14[0,3], Tb15[0,3]], [Tb14[1,3], Tb15[1,3]], [Tb14[2,3], Tb15[2,3]],color='red')
    ax.plot3D([Tb15[0,3], Tb16[0,3]], [Tb15[1,3], Tb16[1,3]], [Tb15[2,3], Tb16[2,3]],color='red')
    ax.plot3D([Tb16[0,3], Tb17[0,3]], [Tb16[1,3], Tb17[1,3]], [Tb16[2,3], Tb17[2,3]],color='red')
    ax.plot3D([Tb17[0,3], Tb18[0,3]], [Tb17[1,3], Tb18[1,3]], [Tb17[2,3], Tb18[2,3]],color='red')
    ax.plot3D([Tb18[0,3], Tb19[0,3]], [Tb18[1,3], Tb19[1,3]], [Tb18[2,3], Tb19[2,3]],color='red')
    ax.plot3D([Tb19[0,3], Tb20[0,3]], [Tb19[1,3], Tb20[1,3]], [Tb19[2,3], Tb20[2,3]],color='red')
    ax.plot3D([Tb20[0,3], Tb21[0,3]], [Tb20[1,3], Tb21[1,3]], [Tb20[2,3], Tb21[2,3]],color='red')



def animsistemamovilx(t):
    n=0
    
    while n<t:
       ax.cla() 
       setaxis(-1,1,-1,1,-1,1)
       r=rotax(n)
       sistemafijo()
       sistemamovil(r)
       n=n+1
       dibujar()

def animsistemamovily(t):
    n=0

    while n<t:
        ax.cla()
        setaxis(-1,1,-1,1,-1,1)
        r=rotay(n)
        sistemafijo()
        sistemamovil(r)
        n=n+1
        dibujar()
    
def animsistemamovilz(t):
    n=0

    while n<t:
        ax.cla()
        setaxis()
        r=rotaz(n)
        sistemafijo()
        sistemamovil(r)
        n=n+1
        dibujar()


def muevemoscax(t): 
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotax(n)
        ax.scatter(0,0.4,0.6,'o')
        Auvw=np.array([[0],[0.4],[0.6]])
        Axyz=np.dot(r,Auvw)
        x=Axyz[0,0]
        y=Axyz[1,0]
        z=Axyz[2,0]
        sistemafijo()
        sistemamovil(r)
        ax.scatter(x,y,z,'o')
        n=n+1
        dibujar()

def muevemoscay(t):
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotay(n)
        ax.scatter(0,0.4,0.6,'o')
        Auvw=np.array([[0],[0.4],[0.6]])
        Axyz=np.dot(r,Auvw)
        x=Axyz[0,0]
        y=Axyz[1,0]
        z=Axyz[2,0]
        sistemafijo()
        sistemamovil(r)
        ax.scatter(x,y,z,'o')
        n=n+1
        dibujar()

def muevemoscaz(t):
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotaz(n)
        ax.scatter(0,0.4,0.6,'o')
        Auvw=np.array([[0],[0.4],[0.6]])
        Axyz=np.dot(r,Auvw)
        x=Axyz[0,0]
        y=Axyz[1,0]
        z=Axyz[2,0]
        sistemafijo()
        sistemamovil(r)
        ax.scatter(x,y,z,'o')
        n=n+1
        dibujar()

def dibujarcaja(d=1,w=1,l=1,r=0):
    #setaxis()
    a1=np.array([[0],[0],[0],[1]], dtype=object)
    b1=np.array([[0],[0],[l],[1]], dtype=object)
    c1=np.array([[0],[w],[l],[1]], dtype=object)
    d1=np.array([[0],[w],[0],[1]], dtype=object)
    e1=np.array([[d],[0],[0],[1]], dtype=object)
    f1=np.array([[d],[0],[l],[1]], dtype=object)
    g1=np.array([[d],[w],[l],[1]], dtype=object)
    h1=np.array([[d],[w],[0],[1]], dtype=object)
    a=np.dot(r,a1)
    b=np.dot(r,b1)
    c=np.dot(r,c1)
    d=np.dot(r,d1)
    e=np.dot(r,e1)
    f=np.dot(r,f1)
    g=np.dot(r,g1)
    h=np.dot(r,h1)
    ax.plot3D([a[0,0],b[0,0]],[a[1,0],b[1,0]],[a[2,0],b[2,0]],color='red') 
    ax.plot3D([a[0,0],d[0,0]],[a[1,0],d[1,0]],[a[2,0],d[2,0]],color='red') 
    ax.plot3D([a[0,0],e[0,0]],[a[1,0],e[1,0]],[a[2,0],e[2,0]],color='red')
    ax.plot3D([b[0,0],c[0,0]],[b[1,0],c[1,0]],[b[2,0],c[2,0]],color='red')
    ax.plot3D([b[0,0],f[0,0]],[b[1,0],f[1,0]],[b[2,0],f[2,0]],color='red')
    ax.plot3D([c[0,0],d[0,0]],[c[1,0],d[1,0]],[c[2,0],d[2,0]],color='red')
    ax.plot3D([c[0,0],g[0,0]],[c[1,0],g[1,0]],[c[2,0],g[2,0]],color='red')
    ax.plot3D([d[0,0],h[0,0]],[d[1,0],h[1,0]],[d[2,0],h[2,0]],color='red')
    ax.plot3D([e[0,0],h[0,0]],[e[1,0],h[1,0]],[e[2,0],h[2,0]],color='red')
    ax.plot3D([e[0,0],f[0,0]],[e[1,0],f[1,0]],[e[2,0],f[2,0]],color='red')
    ax.plot3D([g[0,0],f[0,0]],[g[1,0],f[1,0]],[g[2,0],f[2,0]],color='red')
    ax.plot3D([g[0,0],h[0,0]],[g[1,0],h[1,0]],[g[2,0],h[2,0]],color='red')

    
def animcajax(t):
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotax(n)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()

def animcajay(t):
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotay(n)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()

def animcajaz(t):
    n=0
    while n<t:
        ax.cla()
        setaxis()
        r=rotaz(n)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()
        
    

def animcajaxyz(t1,t2,t3,t4):
    n=0
    while n<t1:
        ax.cla()
        setaxis()
        r=rotaz(n)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()
        
    Rc=r
    n=0
    while n<t2:
        ax.cla()
        setaxis()
        r=rotax(n)
        r=np.dot(r,Rc)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()

    Rc=r
    n=0
    while n<t3:
        ax.cla()
        setaxis()
        r=rotay(n)
        r=np.dot(Rc,r)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()

    Rc=r
    n=0
    while n<t4:
        ax.cla()
        setaxis()
        r=rotax(n)
        r=np.dot(r,Rc)
        dibujarcaja(r=r)
        n=n+1
        sistemafijo()
        dibujar()

#         Ryft4 Rzft2 Rxft1 I Rxmt3 Rzmt5
def animcajaxyz2(t1,t2,t3,t4,t5):
    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    while n1<t1:
        ax.cla()
        setaxis()
        r=mmatrix(rotay(n4),rotaz(n2),rotax(n1),rotax(n3),rotaz(n5))
        dibujarcaja(r=r)
        n1=n1+1
        sistemafijo()
        sistemamovil(r)
        dibujar()
        
    Rc=r
    n=0
    while n2<t2:
        ax.cla()
        setaxis()
        r=mmatrix(rotay(n4),rotaz(n2),rotax(n1),rotax(n3),rotaz(n5))
        dibujarcaja(r=r)
        n2=n2+1
        sistemafijo()
        sistemamovil(r)
        dibujar()

    Rc=r
    n=0
    while n3<t3:
        ax.cla()
        setaxis()
        r=mmatrix(rotay(n4),rotaz(n2),rotax(n1),rotax(n3),rotaz(n5))
        dibujarcaja(r=r)
        n3=n3+1
        sistemafijo()
        sistemamovil(r)
        dibujar()

    Rc=r
    n=0
    while n4<t4:
        ax.cla()
        setaxis()
        r=mmatrix(rotay(n4),rotaz(n2),rotax(n1),rotax(n3),rotaz(n5))
        dibujarcaja(r=r)
        n4=n4+1
        sistemafijo()
        sistemamovil(r)
        dibujar()

    Rc=r
    n=0
    while n5<t5:
        ax.cla()
        setaxis()
        r=mmatrix(rotay(n4),rotaz(n2),rotax(n1),rotax(n3),rotaz(n5))
        dibujarcaja(r=r)
        n5=n5+1
        sistemafijo()
        sistemamovil(r)
        dibujar()

def animcajaxyzt(Dx,t1,t2):
    n=0
    while n<Dx+0.01:
        ax.cla()
        setaxis(4)
        r=trasx(n)
        print(r)
        dibujarcaja(r=r)
        n=n+0.2
        sistemafijo()
        sistemamovil(r)
        dibujar()
        
    Rc=r
    n=0
    while n<t1+0.01:
        ax.cla()
        setaxis(4)
        r=rotaz(n)
        r=np.dot(Rc,r)
        dibujarcaja(r=r)
        n=n+5
        sistemafijo()
        sistemamovil(r)
        dibujar()

    Rc=r
    n=0
    while n<t2+0.01:
        ax.cla()
        setaxis(4)
        r=rotaxf(n,Rc)
        dibujarcaja(r=r)
        n=n+5
        sistemafijo()
        sistemamovil(r)
        dibujar()


def animcajaxyzt2(Dx,Dy,t1,t2):
    n=0
    while n<Dx+0.01:
        ax.cla()
        setaxis(4)
        r=trasx(n)
        a=minv(r)
        a1=np.linalg.inv(r)
        print('incio')
        print('r')
        print(np.round(r,3))
        print('a')
        print(np.round(a,3))
        print('a1')
        print(np.round(a1,3))
        print('fin')
        dibujarcaja(r=r)
        n=n+0.2
        sistemafijo()
        sistemamovil(r)
        dibujar()
    Rc=r
    n=0
    while n<Dy+0.01:
        ax.cla()
        setaxis(4)
        r=trasy(n)
        r=np.dot(Rc,r)
        a=minv(r)
        a1=np.linalg.inv(r)
        print('incio')
        print('r')
        print(np.round(r,3))
        print('a')
        print(np.round(a,3))
        print('a1')
        print(np.round(a1,3))
        print('fin')
        dibujarcaja(r=r)
        n=n+0.2
        sistemafijo()
        sistemamovil(r)
        dibujar()
        
    Rc=r
    n=0
    while n<t1+0.01:
        ax.cla()
        setaxis(4)
        r=rotaz(n)
        r=np.dot(Rc,r)
        a=minv(r)
        a1=np.linalg.inv(r)
        print('incio')
        print('r')
        print(np.round(r,3))
        print('a')
        print(np.round(a,3))
        print('a1')
        print(np.round(a1,3))
        print('fin')
        dibujarcaja(r=r)
        n=n+5
        sistemafijo()
        sistemamovil(r)
        dibujar()

    Rc=r
    n=0
    while n<t2+0.01:
        ax.cla()
        setaxis(4)
        r=rotaxf(n,Rc)
        a=minv(r)
        a1=np.linalg.inv(r)
        print('incio')
        print('r')
        print(np.round(r,3))
        print('a')
        print(np.round(a,3))
        print('a1')
        print(np.round(a1,3))
        print('fin')
        dibujarcaja(r=r)
        n=n+5
        sistemafijo()
        sistemamovil(r)
        dibujar()

def animejeresaotro():
    n=0
    while n<3+0.01:
        ax.cla()
        setaxis(10)
        tab=trasx(n)
        n=n+0.2
        sistemafijo()
        sistemamovil(tab)
        dibujar()
        
    Rtab=tab
    n=0
    while n<5+0.01:
        ax.cla()
        setaxis(10)
        tab=trasy(n)
        tab=np.dot(Rtab,tab)
        n=n+0.2
        sistemafijo()
        sistemamovil(tab)
        dibujar()

    Rtab=tab
    n=0
    while n<45+0.01:
        ax.cla()
        setaxis(10)
        tab=rotax(n)
        tab=np.dot(Rtab,tab)
        n=n+5
        sistemafijo()
        sistemamovil(tab)
        dibujar()
        
    n=0
    while n>-5-0.01:
        ax.cla()
        setaxis(10)
        tac=trasx(n)
        n=n-0.2
        sistemafijo()
        sistemamovil(tac)
        sistemamovil(tab)
        dibujar()
        
    Rtac=tac
    n=0
    while n>-4-0.01:
        ax.cla()
        setaxis(10)
        tac=trasy(n)
        tac=np.dot(Rtac,tac)
        n=n-0.2
        sistemafijo()
        sistemamovil(tac)
        sistemamovil(tab)
        dibujar()

    tba=minv(tab)
    tbc=np.dot(tba,tac)

    n=0
    while n>-6-0.01:
        ax.cla()
        setaxis(10)
        #ntbc=rotazf(n,tbc)
        ntbc=np.dot(trasy(n),tbc)
        tac=np.dot(tab,ntbc)
        n=n-0.2
        sistemafijo()
        sistemamovil(tac)
        sistemamovil(tab)
        dibujar()

def animppp(d1,d2,d3):
    n1=0
    n2=0
    n3=0
    while n1<d1+0.01:
        ax.cla()
        setaxis(10)
        ppp(n1,n2,n3)
        n1=n1+0.2
        dibujar()

    while n2<d2+0.01:
        ax.cla()
        setaxis(10)
        ppp(n1,n2,n3)
        n2=n2+0.2
        dibujar()

    while n3<d3+0.01:
        ax.cla()
        setaxis(10)
        ppp(n1,n2,n3)
        n3=n3+0.2
        dibujar()

def animrpp(t1,d2,d3):
    n1=0
    n2=2
    n3=1
    while n1<t1+0.01:
        ax.cla()
        setaxis(5)
        rpp(n1,n2,n3)
        n1=n1+5
        dibujar()

    while n2<d2+0.01:
        ax.cla()
        setaxis(5)
        rpp(n1,n2,n3)
        n2=n2+0.2
        dibujar()

    while n3<d3+0.01:
        ax.cla()
        setaxis(5)
        rpp(n1,n2,n3)
        n3=n3+0.2
        dibujar()


def animrrp(t1,t2,d3):
    n1=0
    n2=0
    n3=1
    while n1<t1+0.01:
        ax.cla()
        setaxis(5)
        rrp(n1,n2,n3)
        n1=n1+5
        dibujar()

    while n2<t2+0.01:
        ax.cla()
        setaxis(5)
        rrp(n1,n2,n3)
        n2=n2+5
        dibujar()

    while n3<d3+0.01:
        ax.cla()
        setaxis(5)
        rrp(n1,n2,n3)
        n3=n3+0.2
        dibujar()

def animrrr(t1,t2,t3):
    n1=0
    n2=0
    n3=0
    while n1<t1+0.01:
        ax.cla()
        setaxis(5)
        rrr(n1,n2,n3)
        n1=n1+5
        dibujar()

    while n2<t2+0.01:
        ax.cla()
        setaxis(5)
        rrr(n1,n2,n3)
        n2=n2+5
        dibujar()

    while n3<t3+0.01:
        ax.cla()
        setaxis(5)
        rrr(n1,n2,n3)
        n3=n3+5
        dibujar()

def animscara(t1,t2,d3,t4):
    n1=0
    n2=0
    n3=1
    n4=0
    while n1<t1+0.01:
        ax.cla()
        setaxis(5)
        scara(n1,n2,n3,n4)
        n1=n1+5
        dibujar()

    while n2<t2+0.01:
        ax.cla()
        setaxis(5)
        scara(n1,n2,n3,n4)
        n2=n2+5
        dibujar()

    while n3<d3+0.01:
        ax.cla()
        setaxis(5)
        scara(n1,n2,n3,n4)
        n3=n3+0.2
        dibujar()

    while n4<t4+0.01:
        ax.cla()
        setaxis(5)
        scara(n1,n2,n3,n4)
        n4=n4+5
        dibujar()


def animcobras800(t1,t2,d3,t4):
    n1=0
    n2=0
    n3=1
    n4=0
    while n1<t1+0.01:
        ax.cla()
        setaxis(1000)
        cobras800(n1,n2,n3,n4)
        n1=n1+5
        dibujar()

    while n2<t2+0.01:
        ax.cla()
        setaxis(1000)
        cobras800(n1,n2,n3,n4)
        n2=n2+5
        dibujar()

    while n3<d3+0.01:
        ax.cla()
        setaxis(1000)
        cobras800(n1,n2,n3,n4)
        n3=n3+5
        dibujar()

    while n4<t4+0.01:
        ax.cla()
        setaxis(1000)
        cobras800(n1,n2,n3,n4)
        n4=n4+5
        dibujar()


def animur5(t1,t2,t3,t4,t5,t6):
    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    n6=0
    while n1<t1+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n1=n1+5
        dibujar()

    while n2<t2+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n2=n2+5
        dibujar()

    while n3<t3+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n3=n3+5
        dibujar()

    while n4<t4+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n4=n4+5
        dibujar()

    while n5<t5+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n5=n5+5
        dibujar()

    while n6<t6+0.01:
        ax.cla()
        setaxis(1000)
        ur5(n1,n2,n3,n4,n5,n6)
        n6=n6+5
        dibujar()



def animotoman(tb,t1a,t2a,t3a,t4a,t5a,t6a,t7a,t1b,t2b,t3b,t4b,t5b,t6b,t7b):
    nb=0
    n1a=0
    n2a=0
    n3a=0
    n4a=0
    n5a=0
    n6a=0
    n7a=0
    n1b=0
    n2b=0
    n3b=0
    n4b=0
    n5b=0
    n6b=0
    n7b=0
    while n1a<t1a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n1a=n1a+5
        dibujar()

    while n2a<t2a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n2a=n2a+5
        dibujar()

    while n3a<t3a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n3a=n3a+5
        dibujar()

    while n4a<t4a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n4a=n4a+5
        dibujar()

    while n5a<t5a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n5a=n5a+5
        dibujar()

    while n6a<t6a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n6a=n6a+5
        dibujar()

    while n7a<t7a+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n7a=n7a+5
        dibujar()


    while n1b<t1b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n1b=n1b+5
        dibujar()

    while n2b<t2b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n2b=n2b+5
        dibujar()

    while n3b<t3b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n3b=n3b+5
        dibujar()

    while n4b<t4b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n4b=n4b+5
        dibujar()

    while n5b<t5b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n5b=n5b+5
        dibujar()

    while n6b<t6b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n6b=n6b+5
        dibujar()

    while n7b<t7b+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        n7b=n7b+5
        dibujar()

    while nb<tb+0.01:
        ax.cla()
        setaxis(15)
        motoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
        nb=nb+5
        dibujar()

nb=0
n1a=0
n2a=0
n3a=0
n4a=0
n5a=0
n6a=0
n7a=0
n1b=0
n2b=0
n3b=0
n4b=0
n5b=0
n6b=0
n7b=0
sbrazo=False
pasar=False


RDK=Robolink()
robotb=RDK.Item('base')
robotd=RDK.Item('der')
roboti=RDK.Item('izq')

axnb=plt.axes([0.1,0.2,0.3,0.03])
axn1=plt.axes([0.1,0.15,0.3,0.03])
axn2=plt.axes([0.1,0.1,0.3,0.03])
axn3=plt.axes([0.1,0.05,0.3,0.03])
axn4=plt.axes([0.55,0.2,0.3,0.03])
axn5=plt.axes([0.55,0.15,0.3,0.03])
axn6=plt.axes([0.55,0.1,0.3,0.03])
axn7=plt.axes([0.55,0.05,0.3,0.03])
axcb1=plt.axes([0.7,0.25,0.23,0.12])


snb=Slider(axnb, 'rot b', -180, 180.0, valinit=0)
sn1=Slider(axn1, 'rot 1', -180, 180.0, valinit=0)
sn2=Slider(axn2, 'rot 2', -180, 180.0, valinit=0)
sn3=Slider(axn3, 'rot 3', -180, 180.0, valinit=0)
sn4=Slider(axn4, 'rot 4', -180, 180.0, valinit=0)
sn5=Slider(axn5, 'rot 5', -180, 180.0, valinit=0)
sn6=Slider(axn6, 'rot 6', -180, 180.0, valinit=0)
sn7=Slider(axn7, 'rot 7', -180, 180.0, valinit=0)
chkbox1=CheckButtons(axcb1,['cambiar brazo'],[False])

def update(val):
    global nb
    global n1a
    global n2a
    global n3a
    global n4a
    global n5a
    global n6a
    global n7a
    global n1b
    global n2b
    global n3b
    global n4b
    global n5b
    global n6b
    global n7b
    global sbrazo
    if not pasar:
        if (not sbrazo):
            ax.cla()
            setaxis(1500)
            nb=snb.val
            n1a=sn1.val
            n2a=sn2.val
            n3a=sn3.val
            n4a=sn4.val
            n5a=sn5.val
            n6a=sn6.val
            n7a=sn7.val
            accmotoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
            valoresb=[nb]
            valoresd=[n1a,n2a,n3a,n4a,n5a,n6a,n7a]
            valoresi=[n1b,n2b,n3b,n4b,n5b,n6b,n7b]
            robotb.MoveJ(valoresb)
            robotd.MoveJ(valoresd)
            roboti.MoveJ(valoresi)
            dibujar()
        else:
            ax.cla()
            setaxis(1500)
            nb=snb.val
            n1b=sn1.val
            n2b=sn2.val
            n3b=sn3.val
            n4b=sn4.val
            n5b=sn5.val
            n6b=sn6.val
            n7b=sn7.val
            accmotoman(nb,n1a,n2a,n3a,n4a,n5a,n6a,n7a,n1b,n2b,n3b,n4b,n5b,n6b,n7b)
            valoresb=[nb]
            valoresd=[n1a,n2a,n3a,n4a,n5a,n6a,n7a]
            valoresi=[n1b,n2b,n3b,n4b,n5b,n6b,n7b]
            robotb.MoveJ(valoresb)
            robotd.MoveJ(valoresd)
            roboti.MoveJ(valoresi)
            dibujar()


def seleccionbrazo(label):
    global sbrazo
    sbrazo=not sbrazo
    global pasar
    global nb
    global n1a
    global n2a
    global n3a
    global n4a
    global n5a
    global n6a
    global n7a
    global n1b
    global n2b
    global n3b
    global n4b
    global n5b
    global n6b
    global n7b
    pasar=True
    if (not sbrazo):
        sn1.set_val(n1a)
        sn2.set_val(n2a)
        sn3.set_val(n3a)
        sn4.set_val(n4a)
        sn5.set_val(n5a)
        sn6.set_val(n6a)
        sn7.set_val(n7a)
    else:
        sn1.set_val(n1b)
        sn2.set_val(n2b)
        sn3.set_val(n3b)
        sn4.set_val(n4b)
        sn5.set_val(n5b)
        sn6.set_val(n6b)
        sn7.set_val(n7b)
    pasar=False
    


ax.cla()
setaxis(1500)
accmotoman(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
snb.on_changed(update)
sn1.on_changed(update)
sn2.on_changed(update)
sn3.on_changed(update)
sn4.on_changed(update)
sn5.on_changed(update)
sn6.on_changed(update)
sn7.on_changed(update)
chkbox1.on_clicked(seleccionbrazo)
dibujar()


#Motoman CSDA10F






