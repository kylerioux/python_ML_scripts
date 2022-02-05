#calculate rotation required to align 3d vectors

import numpy as np
import math

def calc_vecmag(vec):
    #calculate the magnitude of vectors
    return np.sqrt((vec[0])**2+(vec[1])**2+(vec[2])**2)

def calc_XYproj(vec):
    #calculate vector's projection onto the XY plane
    return np.sqrt((vec[0]**2)+(vec[1]**2))

def calc_rotation_from_Yaxis(vec,XYproj):
    #calculate rotational distance from y-axis to vector
    ang = math.asin(vec[0]/XYproj) #denom only 0 if x and y components both 0
    
    if ang<0 and vec[1]<0:
        #handle case where negative X, negative Y -> need additional 90deg from y-axis
        ang = (-np.pi/2)+ang

    elif ang>0 and vec[1]<0:
        #handle case where positive X, negative Y -> need additional 90deg from y-axis
        ang = (np.pi/2)+ang
    return ang

# define vectors to align
v1 = [-1,-1,1] 
v2 = [1,0,0]

v1mag = calc_vecmag(v1)
v2mag = calc_vecmag(v2)

v1xyProjection = calc_XYproj(v1)
v2xyProjection = calc_XYproj(v2)

v1angFromYax = calc_rotation_from_Yaxis(v1,v1xyProjection)
v2angFromYax = calc_rotation_from_Yaxis(v2,v2xyProjection)

v1_angfromXYplane = math.acos(v1xyProjection/v1mag)
v2_angfromXYplane = math.acos(v2xyProjection/v2mag)

if math.isnan(v1angFromYax) or math.isnan(v2angFromYax): #handles case where eithe vec has no XY projection (only Z) in either vector
    xyplane_rotation = 0
else:
    xyplane_rotation = v2angFromYax-v1angFromYax

zrotation = v2_angfromXYplane-v1_angfromXYplane
print("rotate this much around Z-axis: "+str(round(np.rad2deg(xyplane_rotation),2)))
print("rotate this much with respect to XY plane: "+str(round(np.rad2deg(zrotation),2)))