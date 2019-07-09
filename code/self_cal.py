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
    def __init__(self,pos,drn=np.array([0,1,0])):
        self.pos=pos # Position of td
        self.drn=drn # direction of td
        self.sees=[] #tds that can be seen by this td
        
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
x = 10*rand(3*(n+k-2))
#x = np.zeros(3*(n+k-2))

# setting arbitrary coordinate system points

x1 = 0.0
y1 = 0.0
z1 = 0.0

x2 = 1.0
y2 = 1.0

z3 = 0.0

def function(x): # x -> 3(n+k)-6 elements
    fitness_sum = 0
    board1=[]
    board2=[]
    sys.appendTD(Transducer(np.array([x1, y1, z1]))) # setting origin 
    sys.appendTD(Transducer(np.array([x2, y2, x[0]]))) # setting z axis
    sys.appendTD(Transducer(np.array([x[1], x[2],z3]))) # setting y plane
    for i in range(0,3*(n+k)-9,3):
        sys.appendTD(Transducer(np.array([x[i], x[i+1], x[i+2]]))) # Creating all other transducers
        
    # allocating transducers to respective boards
    for i in range((n+k)//2):
        board1.append(sys.tds[i])
        board2.append(sys.tds[-i-1])
    
    # Transducers see each other 
    for tds1 in board1:
        tds1.see(board2)
    
    for tds2 in board2:
        tds2.see(board1) 
    
    for i in range(len(board1)):
        for j in range(len(board2)):
            error=((board1[i].pos[0]-board2[j].pos[0])**2+
            (board1[i].pos[1]-board2[j].pos[1])**2+
            (board1[i].pos[2]-board2[j].pos[2])**2-distances[i+j])**2
            fitness_sum+=error

    return fitness_sum

res = minimize(function, x)

print("res:", res['fun'])



# =============================================================================
# #setting up solver
# m=GEKKO()
# 
# #Setting up variables 
# p=m.Array(m.Var,(3,10))
# 
# #Random values for initial guesses
# for l in range(3):
#     for h in range(10):
#         p[l][h].value=rdm.random()
# 
# # Assigning arbitrary origin and axes
# for i in range(3):
#     m.Equation(p[i,0]==0) # Origin 
#     if i<2:
#         m.Equation(p[i,1]==0) #z-axis
#         
# m.Equation(p[2,2]==0) # y-plane
# 
# trial= [[((p[0,j]-p[0,k])**2+(p[1,j]-p[1,k])**2+(p[2,j]-p[2,k])**2-sys.tds[j].sees[i][1])**2 for k in range(len(bottomboard))] for j in range(len(bottomboard),len(bottomboard+topboard))]
# 
# # =============================================================================
# # # Setting up equations
# # for j in range(len(topboard)):
# #     for k in range(len(bottomboard)):
# #         d=sys.tds[j].sees[i][1]
# #         m.Equation((p[0,j]-p[0,k])**2+(p[1,j]-p[1,k])**2+(p[2,j]-p[2,k])**2==d)
# #         
# # m.Obj([[(p[0,j]-p[0,k])**2+(p[1,j]-p[1,k])**2+(p[2,j]-p[2,k])**2 for k in range(len(bottomboard))] for j in range(len(bottomboard),len(bottomboard+topboard))])
# #     
# # m.solve() # Solves it hopefully 
# # 
# # for i in range(len(sys.tds)):
# #     pos=(p[0,i],p[1,i].p[2,i])
# #     print('real position: ', sys.tds[i].pos, 'calculated position: ', pos, '\n')
# # =============================================================================
#     
# 
# 
# =============================================================================


        