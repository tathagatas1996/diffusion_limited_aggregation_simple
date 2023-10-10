#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
New versio created on Tue Oct 10 20:36:27 2023
@author: tathagata
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import plot,show

def save_the_plot(x, y, L, file, t):
    plt.clf()
    plt.figure(figsize=(8,8))
    plt.plot(x,y, 'h', color='b')
    plt.xlim(-0.75,L+0.75)
    plt.ylim(-0.75,L+0.75)
    plt.xticks(fontsize=15, fontweight="bold")
    plt.yticks(fontsize=15, fontweight="bold")
    plt.xlabel("Lattice X", fontsize=15, fontweight="bold")
    plt.ylabel("Lattice Y", fontsize=15, fontweight="bold")
    plt.savefig(file+"t"+str(t)+".png", bbox_inches="tight")
    return

def diffusion_limited_aggregation_main(time, L, directory):
    # time: number of iterations
    # L   : lattice dimensions
    # dir : directory
    #-----------------------------------------------------------------------------------------#
    xx = np.array([int(L/2)]) # x-Position
    yy = np.array([int(L/2)]) # y-Position.
    break_loop = 0
    #--------------------------------Main loop-------------------------------#
    for t in range(1,time):
        n = len(xx) # Number of particles at t th iteration
        file = "set1/"
        if xx[n-1] == 0 or xx[n-1] == L or yy[n-1] == 0 or yy[n-1] == L : 
            # Particle sticks to the lattice boundary       
            save_the_plot(xx, yy, L, directory, t)
            xx = np.append(xx,int(L/2))
            yy = np.append(yy,int(L/2))
         
        elif (xx[n-1] != 0 or xx[n-1] != L or yy[n-1] != 0 or yy[n-1] != L) :
            # check the distance from other stuck particles
            if n-1 > 0:
                #Calculating the distance of the random walking prticle from all others
                d = (xx - xx[n-1])**2 + (yy - yy[n-1])**2
                # d^2 = 1; particles stick along the direction of one of the axis
                # d^2 = 2; particles stick diaginally 
                if (2 in d) or (1 in d) and xx[n-1] != int(L/2) and yy[n-1] != int(L/2) :
                    # Particles sticks to other particles 
                    save_the_plot(xx, yy, L, directory, t)
                    xx = np.append(xx,int(L/2))
                    yy = np.append(yy,int(L/2))
                elif (2 in d) or (1 in d) and xx[n-1] == int(L/2) and yy[n-1] == int(L/2) :
                    # Even if the particles stick to one another the final particle has reached 
                    # origin point, which stops the whole loop.
                    break_loop = 1
                else:
                    c = np.random.randint(0,2) #Chose which dimension to move in the random walk
                    if c == 0:
                        stepx = np.random.choice([-1,1])
                        stepy = 0
                    elif c == 1:
                        stepx = 0
                        stepy = np.random.choice([-1,1])
                    xx[n-1] = xx[n-1] + stepx
                    yy[n-1] = yy[n-1] + stepy
            else:
                c = np.random.randint(0,2)
                if c == 0:
                    stepx = np.random.choice([-1,1])
                    stepy = 0
                elif c == 1:
                    stepx = 0
                    stepy = np.random.choice([-1,1])
                xx[n-1] = xx[n-1] + stepx
                yy[n-1] = yy[n-1] + stepy
        if break_loop == 1:
            break
    return


L = 100
time = 2000000
directory = "set2/" # Change this
os.mkdir(directory)

diffusion_limited_aggregation_main( time, L, directory )
