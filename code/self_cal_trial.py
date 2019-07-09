# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:31:25 2019

@author: Redha
"""

import numpy as np 
from scipy.optimize import minimize
import random as rdm
from numpy.random import rand
from gekko import GEKKO

class Transducer:
    ''' initialises transducer with position and direction. Make sure position
    and direction are numpy arrays'''
    def __init__(self,pos,drn=np.array([0,1,0]),board=0):
        self.pos=pos # Position of td
        self.drn=drn # direction of td
        self.sees=[] #tds that can be seen by this td
        self.board=board # which board transducer is on, 0 means unassigned
        
    def __str__(self):
        return('position: {0} \n direction: {1} \n board: {2}'.format(self.pos,self.drn, self.board))
    
    def distance(self,td):
        ''' Calculates distance between this transducer and a given one'''
        return np.linalg.norm(self.pos-td.pos)
        
    def see(self,tds):
        ''' adds the transducer that can be seen to list and stores the distance between '''
        for td in tds:
            dist=self.distance(td) # Calculates distance between tds
            self.sees.append([td,dist]) #adds distance and transducer to tds sees list
    

class TransducerSystem:
    '''System of transducers whose relative positions are to be calculates'''
    def __init__(self):
        self.tds=[] # Empty list to be populated with transducers in system 
        
    def __str__(self):
        return self.tds
    
    def appendTD(self,tds):
        ''' Adds transducer(s) to system'''
        self.tds.extend(tds)
        
###############################################################################
#This case is where all transducers can see eachother, so all distances       #
#are known.                                                                   # 
###############################################################################  
        
sys=TransducerSystem() # Initialise system

n = 5 # number of transducer on one board 
k = 5 # number of transducer on other board

# setting up som transducers for test
td1=Transducer(np.array([0,0,0]),board=1)
td2=Transducer(np.array([0,0,1]),board=1)
td3=Transducer(np.array([4,0,4]),board=1)
td4=Transducer(np.array([1,3,5]),board=1)
td5=Transducer(np.array([2,1,3]),board=1)
td6=Transducer(np.array([4,4.3,0]),board=2)
td7=Transducer(np.array([1,3.5,5]),board=2)
td8=Transducer(np.array([2,3,2]),board=2)
td9=Transducer(np.array([3,4.5,1]),board=2)
td10=Transducer(np.array([3,2.9,3]),board=2)

sys.appendTD([td1,td2,td3,td4,td5]) #adds TDs to system


#setting up solver
m=GEKKO()


#Setting up variables,  no of variables -> 3(n+k)
p=[[m.Var(lb=0) for g in range(n)] for s in range(3)]

# Objective function to minimise, case where all transducers can see each other
m.Obj(sum([sum([((p[0][td1]-p[0][td2])**2+(p[1][td1]-p[1][td2])**2+(p[2][td1]-p[2][td2])**2-sys.tds[td1].distance(sys.tds[td2])**2)**2 
       for td2 in range(td1+1 ,len(sys.tds))])
       for td1 in range(len(sys.tds))]))

# Assigning arbitrary origin and axes
for a in range(3):
    m.Equation(p[a][0]==0) # Origin 
    if a<2:
        m.Equation(p[a][1]==0) #z-axis
        
m.Equation(p[1][2]==0) # y-plane

m.solve() # Solves it hopefully

tds=[] # To store locations of optimised transducers


#shows some results
for psn in range(len(sys.tds)):
    pos=np.array([p[0][psn][0],p[1][psn][0],p[2][psn][0]])
    tds.append(Transducer(pos)) # New list of transducers with positions calculated by optimiser
    print('td{2} \n real position: {0} \t calculated position: {1} \n '.format(sys.tds[psn].pos,pos,psn+1))

#Shows real and calculated distances between transducers
for x in range(len(tds)):
    for y in range(x+1,len(tds)):
        real=sys.tds[x].distance(sys.tds[y])
        calc=tds[x].distance(tds[y])
        print('td{0} to td{1} \n real: {2}  \t calc: {3} \n '.format(x+1,y+1,real,calc))
