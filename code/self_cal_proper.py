# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 17:18:53 2019

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
    
    def distance(self,td,noise=False,size=1):
        ''' Calculates distance between this transducer and a given one. 
        If noise is set to True then noise is added to the distance calculated.
        The size of the noise can be varied by 'size' (random value added 
        between -size and size, default is set to 1) '''
        if noise==True:
            n=2*size*rdm.random()-size
        else:
            n=0
        return np.linalg.norm(self.pos-td.pos)+n
    
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
#This case only transducers on opposite boards can be seen, n is the number   #
#of transducers on one board and k the other                                  # 
###############################################################################  
        
sys=TransducerSystem() # Initialise system

n = 10 # number of transducer on one board 
k = 10 # number of transducer on other board

# setting up som transducers for test
td1=Transducer(np.array([0,0,0]),board=1)
td2=Transducer(np.array([0,0,1]),board=1)
td3=Transducer(np.array([4,0,4]),board=1)
td4=Transducer(np.array([1,0.1,5]),board=1)
td5=Transducer(np.array([2,1.5,3]),board=1)
td6=Transducer(np.array([7.4,1,6]),board=1)
td7=Transducer(np.array([4.1,0.9,3]),board=1)
td8=Transducer(np.array([1.2,1.4,5.4]),board=1)
td9=Transducer(np.array([1,1,1]),board=1)
td10=Transducer(np.array([2,0.5,4]),board=1)
td11=Transducer(np.array([4,4,0]),board=2)
td12=Transducer(np.array([1,3.5,5]),board=2)
td13=Transducer(np.array([2,3,2]),board=2)
td14=Transducer(np.array([3,4.5,1]),board=2)
td15=Transducer(np.array([3,2.9,3]),board=2)
td16=Transducer(np.array([5,4.6,1]),board=2)
td17=Transducer(np.array([2.8,3.7,6]),board=2)
td18=Transducer(np.array([8,4,2]),board=2)
td19=Transducer(np.array([5.6,3.7,7]),board=2)
td20=Transducer(np.array([1,4.6,5]),board=2)


#sys.appendTD([td1,td2,td3,td4,td5,td11,td12,td13,td14,td15]) #adds TDs to system
sys.appendTD([td1,td2,td3,td4,td5,td6,td7,td8,td9,td10,td11,td12,td13,td14,td15,td16,td17,td18,td19,td20]) #adds TDs to system

# Sets up lists that holds the TDs on the respective board
board1=[]
board2=[]

#adds TDs to their respective board list
for td in sys.tds:
    if td.board==1:
        board1.append(td)
    else: 
        board2.append(td)
        
# Transducer on opposite boards see each other        
for i in board1:
    i.see(board2)
    
for j in board2:
    j.see(board1)
        


#setting up solver
m=GEKKO()

#Setting up variables,  no of variables -> 3(n+k)
p=[[m.Var(lb=0) for g in range(n+k)] for s in range(3)]

#Random values for initial guesses
for l in range(3):
    for h in range(n+k):
        p[l][h].value=7*rdm.random()
        

# Assigning arbitrary origin and axes
for a in range(3):
    m.Equation(p[a][0]==0) # Origin 
    if a<2:
        m.Equation(p[a][1]==0) #z-axis
        
m.Equation(p[1][2]==0) # y-plane

# =============================================================================
# m.Equation(sum([sum([((p[0][td1]-p[0][td2])**2+(p[1][td1]-p[1][td2])**2+(p[2][td1]-p[2][td2])**2-sys.tds[td1].distance(sys.tds[td2],True)**2)**2 
#        for td2 in range(len(board1),len(board1)+len(board2))])
#        for td1 in range(len(board1))])<10)
# =============================================================================


# Objective function to minimise
m.Obj(sum([sum([((p[0][td1]-p[0][td2])**2+(p[1][td1]-p[1][td2])**2+(p[2][td1]-p[2][td2])**2-sys.tds[td1].distance(sys.tds[td2])**2)**2 
       for td2 in range(len(board1),len(board1)+len(board2))])
       for td1 in range(len(board1))]))

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
        
        
# =============================================================================
# #Shows real and calculated distances between transducers
# for x in range(len(tds)):
#     for y in range(x+1,len(tds)):
#         real=sys.tds[x].distance(sys.tds[y])
#         calc=tds[x].distance(tds[y])
#         print('td{0} to td{1} \n real: {2}  \t calc: {3} \n {4} \t {5}'.format(x,y,real,calc,sys.tds[x].pos,sys.tds[y].pos))
# =============================================================================
        
        
    
    

    
    


