#calculate rotation to align 3d vectors

import numpy as np
import math
v1 = [-0.2,-0.2,0]
v2 = [0.2,0.2,0]

#1: project onto XY plane 
v1xyProjection = np.sqrt((v1[0]**2)+(v1[1]**2))
v1xyAngle = math.asin(v1[0]/v1xyProjection) # denom only 0 if x and y components both 0
print(v1xyProjection)
print(v1xyAngle)
if v1xyAngle<0 and v1[1]<0:
    #in q3 (negative X, negative Y)
    angle_from_y = (-np.pi/2)+v1xyAngle

if v1xyAngle<0 and v1[1]>0:
    #in q4 (positive X, negative Y)
    angle_from_y = (np.pi/2)+v1xyAngle
print("angle1: "+ str(angle_from_y))

v2xyProjection = np.sqrt((v2[0]**2)+(v2[1]**2))
v2xyAngle = math.asin(v2[0]/v2xyProjection) # denom only 0 if x and y components both 0
print(v2xyProjection)
print(v2xyAngle)
if v2xyAngle<0 and v2[1]<0:
    #in q3 (negative X, negative Y)
    angle_from_y2 = (-np.pi/2)+v2xyAngle

if v2xyAngle<0 and v2[1]>0:
    #in q4 (positive X, negative Y)
    angle_from_y2 = (np.pi/2)+v2xyAngle
print("angle2: "+ str(angle_from_y2))

xyplane_rotation = angle_from_y2-angle_from_y
print(xyplane_rotation)