# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:53:34 2019

@author: Redha
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:37:57 2019

@author: Redha
"""

import numpy as np 
from scipy.optimize import minimize
import random as rdm
from numpy.random import rand

class Transducer:
    ''' initialises transducer with position and direction. Make sure position
    and direction are numpy arrays'''
    def __init__(self,pos,drn=np.array([0,1,0]),board=0):
        self.pos=pos # Position of td
        self.drn=drn # direction of td
        self.sees=[] #tds that can be seen by this td
        self.board=board # which board transducer is on, 0 means unassigned
        
    def __str__(self):
        return('position: {0} \n direction: {1}'.format(self.pos,self.drn))
        
    def see(self,tds):
        ''' adds the transducer that can be seen to list and stores the distance between '''
        for td in tds:
            dist=np.linalg.norm(self.pos-td.pos) # Calculates distance between tds
            self.sees.append([td,dist]) #adds distance and transducer to tds sees list
    

class TransducerSystem:
    '''System of transducers whose relative positions are to be calculates'''
    def __init__(self):
        self.tds=[] # Empty list to be populated with transducers in system 
        
    def __str__(self):
        return self.tds
    
    def appendTD(self,tds):
        ''' Adds transducer(s) to system'''
        self.tds.extend([tds])
        
sys=TransducerSystem() # Initialise system

n = 5 # number of transducer on one board 
k = 5 # number of transducer on other board

# setting up random distances 
distances=10*rand(n*k)

# setting up array to store positions
x = np.zeros(3*(n+k-2))

# setting arbitrary coordinate system points

x1 = 0.0
y1 = 0.0
z1 = 0.0

x2 = 1.0
y2 = 1.0

z3 = 0.0

def function(x): # x -> 3(n+k)-6 elements
    fitness_sum = 0
    sys.appendTD(Transducer(np.array([x1, y1, z1]),board=1)) # setting origin 
    sys.appendTD(Transducer(np.array([x2, y2, x[0]]),board=1)) # setting z axis
    sys.appendTD(Transducer(np.array([x[1], x[2],z3]),board=1)) # setting y plane
    
    for i in range(0,3*(n+k)-9,3):
        if i<((3*(n+k)-9)//2)-4:
            sys.appendTD(Transducer(np.array([x[i], x[i+1], x[i+2]]),board=1)) # Creating other transducers on board 1
        else:
            sys.appendTD(Transducer(np.array([x[i], x[i+1], x[i+2]]),board=2)) # Creating other transducers on board 2
    
    # Set up boards to assign transducers to 
    board1=[] 
    board2=[]
    
    for td in sys.tds:
        if td.board==1:
            board1.append(td)
        else:
            board2.append(td)
    
    print(board1)
    print(board2)
    

    for td1 in range(5):
        for td2 in range(5):
            error=((board1[td1].pos[0]-board2[td2].pos[0])**2+
            (board1[td1].pos[1]-board2[td2].pos[1])**2+
            (board1[td1].pos[2]-board2[td2].pos[2])**2-distances[td1+td2])**2
            fitness_sum+=error

    return fitness_sum, board1, board2

a=function(x)

res = minimize(function, x)

print("res:", res)
