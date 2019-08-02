# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:40:32 2018

@author: Raven
"""

import numpy as np
from math import tan, pi, cos, sin, sqrt, radians, degrees
import pygame as pg

#_____DEFINITIONS_____

def loadlights(filename='runway_lights.dat'):
    
    data   = np.genfromtxt(filename, delimiter=",", autostrip=True)
    
    #print(np.shape(data))
    
    zrow     = np.zeros(697)              #z-row
    row0     = data[:,0]                  #y-row
    row1     = data[:,1]                  #x-row
    
    lightpos =np.array([row1,row0,zrow])  #light position xyz
    
    rcol     = data[:,2]
    gcol     = data[:,3]
    bcol     = data[:,4]
    
    lightcol = np.column_stack((rcol.astype(int),gcol.astype(int),bcol.astype(int))) #light color RGB

    return lightpos, lightcol


accor =  loadlights()[0]


def convertcoordinates(accor):           #convert ac coordinates to screen coordinates
    
    scrcor=np.array([accor[0],accor[2],accor[1]])
    
    return scrcor #x[(1,2,0),:]

#scrcor=convertcoordinates(accor)         

def movepoints(scrcor, bodypos, phi, theta, psi):
    
    relpos      = scrcor-bodypos
    
    return relpos



def projection(relpos, pz, xmax, ymax):
        
    ys    = pz*(relpos[2]/relpos[0])+ymax/2
    xs    = pz*(relpos[1]/relpos[0])+xmax/2
    dist  = np.linalg.norm(relpos, axis=0)

    
    return xs , ys, dist



#______PyGAME VALUES AND CALCULATIONS______
    

xmax    = 3000  #1000                  #max x coordinate screen
ymax    = 2400  #800                   #max y coordinate screen
reso    = (xmax,ymax)
beta    = 10                           #max elevation angle in deg
pz      = ymax/2/tan(beta*pi/180)

bodypos = (-1850,0.,-100.)
bodypos = np.array([bodypos]*697).T


#______PyGAME______

pg.init()

#______CLOCK_INIT_____

t0    = 0.001*pg.time.get_ticks()
maxdt = 0.5

#_____SCREEN_INIT_____

scr   = pg.display.set_mode(reso)
black = (0,0,0)
white = (255,255,255)
clrs  = loadlights()[1]
p1    = np.array([0,ymax/2])
p2    = np.array([xmax,ymax/2])
diagv = sqrt(xmax**2+ymax**2)

#_____STARTVALUES_____

phi   = 0.0*pi/180     #[rad]
theta = -3.0*pi/180    #[rad]
psi   = 0.0*pi/180     #[rad]
V     = 150.           #[m/s]
omega = 15*pi/180      #[rad/s]
ax    = 40.            #[m/s**2]

running= True

while running:
    pg.event.pump()
    
    t = 0.001*pg.time.get_ticks()
    dt= min(t-t0,maxdt)
    
    if dt>0:
      
        t0          = t
        bodypos[0]  = bodypos[0]+V*dt*cos(psi)*cos(theta)
        bodypos[1]  = bodypos[1]+V*dt*sin(psi)*cos(theta)
        bodypos[2]  = bodypos[2]-V*dt*sin(theta)
        psi         = psi+omega*dt*tan(phi)
        t           = t+dt
        
        
        #____POINT_ROTATE____
        
        relpos      = movepoints(accor,bodypos,phi, theta, psi)
        phi         = -phi
        theta       = -theta
        psi         = -psi
        Rx          = np.array([[1.,0.,0.],[0.,cos(phi),-sin(phi)],[0.,sin(phi),cos(phi)]])
        Ry          = np.array([[cos(theta),0.,sin(theta)],[0.,1.,0.],[-sin(theta),0.,cos(theta)]])
        Rz          = np.array([[cos(psi),-sin(psi),0.],[sin(psi),cos(psi),0.],[0.,0.,1]])
        Rt          = np.dot(Rx,np.dot(Ry,Rz))
        phi         = -phi
        theta       = -theta
        psi         = -psi
        
        bodyposrot  = np.dot(Rt,relpos) 
       
        xs, ys, dist= projection(bodyposrot,pz,xmax,ymax)
     


    #____HORIZON_____
    
    dx          = diagv*cos(phi)
    dy          = -diagv*sin(phi)
    delev       = beta*pi/180
    dazim       = beta*pi/180*xmax/ymax
    xc          = theta*sin(phi)*xmax/(dazim*2)+xmax/2
    yc          = theta*cos(phi)*ymax/(delev*2)+ymax/2
    p1          = np.array([xc-dx,yc-dy])
    p2          = np.array([xc+dx,yc+dy])


    
    scr.fill(black)
    
    pg.draw.aaline(scr,white,p1,p2,True)
    #pg.draw.rect(scr,(0,191,255),(0,0,xmax,ymax/2),0)
    
    #____LIGHTS_INIT_____
    
    for i in range(0,697):
        if 0.<=xs[i]<=xmax and 0<=ys[i]<=ymax and bodyposrot[0][i]>0:
            if bodyposrot[2][i]>=5000:
                scr.set_at((int(xs[i]),int(ys[i])),clrs[i])    
            else:
                pg.draw.circle(scr,clrs[i],(int(xs[i]),int(ys[i])),int(max(1,(5000-dist[i])/1500)))


    
    pg.display.flip()


    
    keys= pg.key.get_pressed()
    
    #____KEY_COMMANDS____
    
    if keys[pg.K_ESCAPE]:
        running= False
    
    if keys[pg.K_UP]:
        theta= theta-0.025*pi/180
     
    if keys[pg.K_DOWN]:
        theta= theta+0.025*pi/180
      
    if keys[pg.K_RCTRL]:
        V= V+2.5
        
    if keys[pg.K_RALT]:
        V= V-2.5
    
    if keys[pg.K_LEFT]:
        phi= phi-0.10*pi/180
    
    if keys[pg.K_RIGHT]:
        phi= phi+0.10*pi/180
        
        

pg.quit()



