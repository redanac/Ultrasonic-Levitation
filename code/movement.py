#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 13:24:00 2019

@author: redha
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:35:03 2019

@author: Redha
"""

# Import stuff

board = 1
from Controller import *
import Functions
import pickle 
import numpy as np
from UltrasonicLevitator import *

def get_angle(x,y):
    if x==0:
        ang=0
    
    elif y==0 and x!=0:
        ang=np.pi/2
        
    else:    
        ang=np.arctan2(x,y)%(2*np.pi)
        
        
    return ang

def create_twin_trap(tdsys,point):
    '''Returns list  of offsets for a twin trap when given td system with td positions'''
    
    offsets=[] # list to store offsets
    
    tdsys.focus(point) # focus system at point
    
    angle=get_angle(point[0],point[1]) 

    for i, td in enumerate(tdsys.transducers):
        ang=get_angle(td.pos[0],td.pos[1])
        if angle<np.pi:
            if ang>(angle-np.pi)%(2*np.pi) or ang<angle:
                offsets.append(td.phi)
            else:
                offsets.append(td.phi+np.pi)
        else:
            if ang<(angle-np.pi)%(2*np.pi) or ang>angle:
                offsets.append(td.phi)
            else:
                offsets.append(td.phi+np.pi)
    
    return offsets

R=0.0725 # Radius of ring in m
n=25 # Number of tds in a ring

point=np.array([0,0,-0.01])

tdsys=ParticleSystem() #Initialise particle system

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
        
        
        pos=np.array([x,y,z]) # Position and director of transducer
        
        tdsys.appendTransducer(pos,-pos) # adds Transducer to system
        
#Load in offsets for pattern
twin=np.array(pickle.load(open('opt_phi_ring.pkl','rb')))
twin=twin%(2*np.pi)
vortex=pickle.load(open('opt_phi_ring_vortex.pkl','rb'))
antivort=vortex[::-1]
                    
tdsys.focus(Vector([0,0,0])) #Focuses td system at origin

with Controller() as com:
    command = {"CMD":2}
    reply = com.send_json(command)
    print(reply)

    # Send Power setting command
    command_power = Functions.create_board_command_power(board, 511)
    reply = com.send_json(command_power)
    if reply["Status"] != "Success":
        raise Exception("Failed to start conversion", reply)
                   
      

    for i in range(100):
        # Send offset commands
        command = Functions.create_board_command_offset(board, i, twin[i]) # Sets offsets of each TD for twin trap
        reply = com.send_json(command) #Checks if succesful
        if reply["Status"] != "Success":
            raise Exception("Failed to start conversion", reply)
                
    # Send load offset command
    command = Functions.create_board_command_load_offsets(board)
    reply = com.send_json(command)
    if reply["Status"] != "Success":
        raise Exception("Failed to start conversion 1", reply)
        
    print(point)
    
    while 1:
        
        
        choose=input('move trap \n')
        
       
        
        if choose=='w':
            
            
            point[1]+=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
                
        elif choose=='s':
            
            point[1]-=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
        
        elif choose=='a':
            
            point[0]-=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
                
        elif choose=='d':
            
            point[0]+=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
            
            
        elif choose=='u':
            
            point[2]+=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
                
        elif choose=='i':
            
            point[2]-=0.005
            
            offset=create_twin_trap(tdsys,point)
            
            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, offset[i]) # Sets offsets of each TD for twin trap
                reply = com.send_json(command) #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
                        
            # Send load offset command
            command = Functions.create_board_command_load_offsets(board)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion 1", reply)
            
            
        elif choose=='q':
            break
            
        else:
            print('press valid key')
        
        print(point)
        print('')
