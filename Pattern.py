# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 22:35:03 2019

@author: Redha
"""

board = 1
from Controller import *
import Functions
import pickle 
import numpy as np
from UltrasonicLevitator import *

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
offsets=pickle.load(open('opt_phi_ring.pkl'))

tdsys.focus(Vector([0,0,0]))

with Controller() as com:
    command = {"CMD":2}
    reply = com.send_json(command)
    print(reply)

    # Send Power setting command
    command_power = Functions.create_board_command_power(board, 511)
    reply = com.send_json(command_power)
    if reply["Status"] != "Success":
        raise Exception("Failed to start conversion", reply)
        
        
    
    choose=input('Press h for haptic \n or p for pattern')
    
    if choose == 'p':
        
        for i in range(100):
            # Send offset commands
            command = Functions.create_board_command_offset(board, i, offsets[i])
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion", reply)
        
    if choose == 'h':
        
        for i in range(100):
            # Send offset commands
            command = Functions.create_board_command_offset(board, i, tdsys.transducers[i].phi)
            reply = com.send_json(command)
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion", reply)
                
                
    # Send load offset command
    command = Functions.create_board_command_load_offsets(board)
    reply = com.send_json(command)
    if reply["Status"] != "Success":
        raise Exception("Failed to start conversion 1", reply)
