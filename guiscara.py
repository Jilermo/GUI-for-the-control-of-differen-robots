import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.widgets import Slider

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

def sistemafijo():
    x=[0,1]
    y=[0,1]
    z=[0,1]
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
    


def sistemamovil(r):
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
    
    ax.plot3D([px,px+ux],[py,py+uy],[pz,pz+uz],color='red') #Dibuja eje movil u
    ax.plot3D([px,px+vx],[py,py+vy],[pz,pz+vz],color='green') #Dibuja eje movil v
    ax.plot3D([px,px+wx],[py,py+wy],[pz,pz+wz],color='blue') #Dibuja eje movil w
    
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

axn1=plt.axes([0.2,0.2,0.65,0.03])
axn2=plt.axes([0.2,0.15,0.65,0.03])
axn3=plt.axes([0.2,0.1,0.65,0.03])
axn4=plt.axes([0.2,0.05,0.65,0.03])

sn1=Slider(axn1, 'rotacion 1', 0, 360.0, valinit=0)
sn2=Slider(axn2, 'rotacion 2', -175, 175.0, valinit=0)
sn3=Slider(axn3, 'rotacion 3', 0, 360.0, valinit=0)
sn4=Slider(axn4, 'traslacion 1', 0, 6.0, valinit=3)

def update(val):
    ax.cla()
    setaxis(10)
    n1=sn1.val
    n2=sn2.val
    n4=sn3.val
    n3=sn4.val
    scara(n1,n2,n3,n4)
    dibujar()

ax.cla()
setaxis(10)
scara(0,0,3,0)
sn1.on_changed(update)
sn2.on_changed(update)
sn3.on_changed(update)
sn4.on_changed(update)
dibujar()
















