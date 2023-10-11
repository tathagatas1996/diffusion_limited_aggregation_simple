#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 19:41:10 2023

@author: tathagata
"""

import os
import numpy as np
import matplotlib.pyplot as plt



def save_the_plot(x, y, L, file, t):
    plt.clf()
    plt.figure(figsize=(8,8))
    plt.plot(x,y, 'h', color='b', markersize=2.5)
    plt.xlim(-L-0.75,L+0.75)
    plt.ylim(-L-0.75,L+0.75)
    plt.xticks(fontsize=15, fontweight="bold")
    plt.yticks(fontsize=15, fontweight="bold")
    plt.xlabel("Lattice X", fontsize=15, fontweight="bold")
    plt.ylabel("Lattice Y", fontsize=15, fontweight="bold")
    plt.savefig(file+"t"+str(t)+".png", bbox_inches="tight")
    return


def cond_dist(xx,yy):
    u = 0
    n = len(xx)
    del_x = xx - xx[n-1]
    del_y = yy - yy[n-1]
    dist = del_x**2 + del_y**2
    for i in range(n-1):
        if dist[i] == 1 or dist[i] == 2 :
            u = 1
            break
    return(u)


def simple_random_walk():
    cc = np.random.randint(0,2)
    if cc == 0:
        stepx = np.random.choice([-1,1])
        stepy = 0
    elif cc == 1:
        stepx = 0
        stepy = np.random.choice([-1,1])
    return(np.array([stepx,stepy]))


def biased_random_walk(xp,yp):
    if xp > 0 and yp > 0:
        cc = np.random.randint(0,2)
        if cc == 0:
            stepx = -1
            stepy = 0
        elif cc == 1:
            stepx = 0
            stepy = -1
    elif xp > 0 and yp < 0:
        cc = np.random.randint(0,2)
        if cc == 0:
            stepx = -1
            stepy = 0
        elif cc == 1:
            stepx = 0
            stepy = +1            
    elif xp < 0 and yp < 0:
        cc = np.random.randint(0,2)
        if cc == 0:
            stepx = +1
            stepy = 0
        elif cc == 1:
            stepx = 0
            stepy = +1                   
    elif xp < 0 and yp > 0:
        cc = np.random.randint(0,2)
        if cc == 0:
            stepx = +1
            stepy = 0
        elif cc == 1:
            stepx = 0
            stepy = -1
    elif xp == 0:
        stepx = 0
        if yp > 0:
            stepy = -1
        elif yp < 0:
            stepy = +1
    elif yp == 0:
        stepy = 0
        if xp > 0:
            stepx = -1
        elif xp < 0:
            stepx = +1     
    return(np.array([stepx,stepy]))
    


def main_diffusion_aggregation( L   ,  r0, 
                                time,  directory):
    """ Main function for diffusion limited aggregation. """
    xx = np.array([0]) # X-position array for final position of the particle
    yy = np.array([0]) # Y-position array for final position of the particle
    r  = r0 # initially the boundary where a new particle is created  
    theta = 2*np.pi*np.random.random()
    xx = np.append(xx, int(r*np.cos(theta) + 1))
    yy = np.append(yy, int(r*np.sin(theta) + 1))
    
    for t in range(1, time):
        n = len(xx)
        u = cond_dist(xx,yy)
        if u == 0:                   
            # perform random walk
            rj = np.sqrt( xx[n-1]**2 + yy[n-1]**2 )
            if rj < np.sqrt(4*r**2 - 1) :   
                #perform a simple random walk
                step = simple_random_walk()
            elif rj >= np.sqrt(4*r**2 - 1): 
                #perform a biased random walk
                step = biased_random_walk( xx[n-1], yy[n-1] )
            xx[n-1] = xx[n-1] + step[0]
            yy[n-1] = yy[n-1] + step[1]
    
        elif u == 1: 
            #create new particle
            r_all = np.sqrt(xx**2 + yy**2) 
            if max(r_all) > r0:
                r = max(r_all) + 1     # The distance at which a new particle is created           
            theta = 2*np.pi*np.random.random()
            
            x_new = int(r*np.cos(theta)) 
            y_new = int(r*np.sin(theta))
        
            save_the_plot(xx, yy, L, directory, t)
            xx = np.append(xx,x_new)
            yy = np.append(yy,y_new)
            
    return (xx,yy)


L  = 100 # Lattice length
r0 = 10 # initially the boundary where a new particle is created
time = 1200000 # the total number of iterations
directory = "set5_1/"

if os.path.isdir(directory) == False:
    os.mkdir( directory )
    
(xx,yy) = main_diffusion_aggregation( L, r0, time, directory)