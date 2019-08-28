# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:23:40 2019

@author: Redha
"""

import numpy as np
from UltrasonicLevitator import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pickle 

origin=[0,0,0] # Point where all TDs are facing set as origin
R=72.5 # Radius of sphere that mould is made from in mm

tdsys=ParticleSystem() # Initiates transducer system that contains our transducers

xs, ys, zs =[], [], [] # Coordinates to plot to make sure positions are right

count=0

n=25 #number of transducer in one ring

tds=[]


for i in range(25): # 25 tds in each circle
    for theta in np.radians([72.5,67.5,61.5,55]): # angle of td along hemisphere face
        # cylindrical coordinates 
        r = R*np.sin(theta)
        z = -R*np.cos(theta)
        phi = 2*np.pi/n*i
        
        # offsetting transducers for tighter packing 
        if theta == np.radians(67.5) or theta == np.radians(55):
            phi += np.radians(7.25)
    
        # Cartesian coordinates
        x = r*np.cos(phi)
        y = r*np.sin(phi)
        # z=z here 
        
        # Adds to coordinates for plotting
        xs.append(x)
        ys.append(y)
        zs.append(z)
        
        pos=np.array([x,y,z]) # Position and director of transducer
        
        tds.append(pos)
        
        tdsys.appendTransducer(pos,-pos) # adds Transducer to system

pickle.dump(tds,open('td_placement.pkl','wb'))

tdsys.focus(Vector([0,0,0]))
        
point = np.array([2,2,0])

angle= np.arc()

for td in tds:
   
# =============================================================================
# pickle.dump(tds,open('ring_td_placement.pkl','wb'))
# =============================================================================
        
        
# Plotting 
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xs[0:4], ys[0:4], zs[0:4], color='red')
ax.scatter(xs[5:], ys[5:], zs[5:])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()



