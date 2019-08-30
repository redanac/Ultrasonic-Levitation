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

R=0.0725 # Radius of ring in m
n=25 # Number of tds in a ring

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
                   
    # Choose type of trap to generate    

    print('\n \n t for twin trap')
    print('v for votex trap \n \n')

    choose=input('Select Trap \n\n')
                   
    if choose == 't':


        print('twin', np.degrees(twin)-360 )


        for i in range(100):
            # Send offset commands
            command = Functions.create_board_command_offset(board, i, twin[i]) # Sets offsets of each TD for twin trap
            reply = com.send_json(command) #Checks if succesful
            if reply["Status"] != "Success":
                raise Exception("Failed to start conversion", reply)

    elif choose =='v':

        while 1:

            for i in range(100):
                # Send offset commands
                command = Functions.create_board_command_offset(board, i, vortex[i])  # Sets offsets of each TD for vortex trap
                reply = com.send_json(command)  #Checks if succesful
                if reply["Status"] != "Success":
                    raise Exception("Failed to start conversion", reply)
            

    else:
        raise Exception('Please select an option from the above choices')
    
    
                
    # Send load offset command
    command = Functions.create_board_command_load_offsets(board)
    reply = com.send_json(command)
    if reply["Status"] != "Success":
        raise Exception("Failed to start conversion 1", reply)
