#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 17:48:10 2020

@author: max
"""

###
# Read .json file of annotation coordinates select object and compute motion
###

# Load libraries
import json 
import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
# Custom function to compute centroid
import geometry

# Define an object to be plotted and extracted
object_select = 'Body_Face'

# Define frame rate for plotting
fr = 30

# Select range of frames to plot (be carefull not to make too large)
frame_range = np.arange(1, 21)

# Run setup file (contains data directories)
exec(open('setup_object_motion.py').read())

# Load all possible colors from matplotlib
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = list(colors.keys())

##### TO-Do #####
# Make a dictionary of all objects and assign a color to each
#####
    
# Random reshuffle of colors
np.random.seed(1)
idx = np.random.permutation(len(colors))
colors = [colors[i] for i in idx]

# Load all files 
annotion_files = sorted(glob.glob(f'{annot_dir}/{present_dir}/present_*.json'))
frames = sorted(glob.glob(f'{annot_dir}/{present_dir}/present_*.jpg'))

# Create figure
fig = plt.figure()

# Pre-allocate the array of coordinates
Cx = np.zeros(len(frame_range))
Cy = np.zeros(len(frame_range))
motion = np.zeros(len(frame_range)) * np.nan

# Load the annotation data
for i, n_fr in enumerate(frame_range):
    
    print(i)
    print(n_fr)
    
    with open(annotion_files[n_fr]) as f:
      annotation = json.load(f)
      
    # Load the current frame
    frame = cv2.imread(frames[n_fr])
    
    ##### TO-Do #####
    # Colors of frames are messed up
    #####
    
    # Clear figure
    fig.clear()
    
    # Plot frame
    plt.imshow(frame)
      
    ##### TO-Do #####
    # Select a specific object (e.g. faces)
    #####
    
    annotation_names = [None] * len(annotation['shapes']);
    
    # Extract the names of all annotated objects in the frame
    for shape in range(len(annotation['shapes'])): 
        annotation_names[shape] = annotation['shapes'][shape]['label']
        
    # Find if the current annotation is present in this frame
    indices = [i for i,x in enumerate(annotation_names) if x == object_select]
    
    # Check if there are any objects in this frame 
    if indices:
        
        # Copy the coordinated of the annotations from the past frame 
        if i == 0:
            coords_last = np.nan
        else:
            coords_last = coords_current
        
        # Create a list for the objects in the current frame 
        coords_current = [None] * len(indices)
        
        # Loop over all shapes in this frame 
        for j, shape in enumerate(indices):  
                
            # Convert coordinates of annotation to numpy array
            point_coords = np.asarray(annotation['shapes'][shape]['points'])
            
            # Compute centroid
            coords_current[j] = geometry.centroid(point_coords)
            
            # Plot outline of current object annotation on the frame
            plt.fill(point_coords[:,0], point_coords[:,1], \
                     facecolor='none', edgecolor=colors[shape])
            
            # Plot the centroid 
            plt.plot(coords_current[j][0], coords_current[j][1], \
                     marker='o', color=colors[shape], \
                     label=annotation['shapes'][shape]['label'])
            
            # Don't show axes
            plt.axis('off')
        
            # Show the legend
            plt.legend()
            
            # Make fullscreen
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            
            # Tile 
            plt.title(f'Frame {n_fr}')
            
            # Show plot and pause
            plt.show()
            plt.pause(1/fr)
            
    else:
        
        if i == 0:
            coords_last = np.nan
        else:
            coords_last = coords_current
        coords_current = np.nan
    
    ## Compute the motion as the displacement of the centroids from the last tp the current frame 
    # There may be multiple objects of the same type on a frame
    # Find the ones that are closest to each other
    if np.sum(np.isnan(coords_current)) == 0 \
        and np.sum(np.isnan(coords_last)) == 0:
        
        distance = np.zeros((len(coords_current), len(coords_last)))
        
        for curr in range(len(coords_current)):
            for last in range(len(coords_last)):
                distance[curr, last] = np.sqrt(np.sum( \
                        (np.asarray(coords_current[curr]) \
                         - np.asarray(coords_last[last]))**2))
                
        idx_match = np.zeros(len(coords_current))
        for curr in range(len(coords_current)):
            idx_match[curr] = np.argmin(distance[curr,:])
            
        # Compute the displacement for each objects
        motion_all = np.zeros(len(coords_current))
        for obj in range(len(coords_current)):
            motion_all[obj] = np.sqrt(np.sum( \
                        (np.asarray(coords_current[obj]) \
                         - np.asarray(coords_last[int(idx_match[obj])]))**2))
            
        # The total motion for this frame is the sum of the motion of all objects
        motion[i] = np.sum(motion_all)

## Plot the coordinates
plt.figure()
plt.plot(motion)
    