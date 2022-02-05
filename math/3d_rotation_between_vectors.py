#calculate rotation to align 3d vectors

import numpy as np
import math
v1 = [1,1,1]
v2 = [0,0,1]

v1mag = np.sqrt((v1[0])**2+(v1[1])**2+(v1[2])**2)
v2mag = np.sqrt((v2[0])**2+(v2[1])**2+(v2[2])**2)

#1: project onto XY plane 
v1xyProjection = np.sqrt((v1[0]**2)+(v1[1]**2))
v1xyAngle = math.asin(v1[0]/v1xyProjection) #denom only 0 if x and y components both 0
print(v1xyProjection)
print(v1xyAngle)
if v1xyAngle<0 and v1[1]<0:
    #in q3 (negative X, negative Y)
    angle_from_y = (-np.pi/2)+v1xyAngle

elif v1xyAngle>0 and v1[1]<0:
    #in q4 (positive X, negative Y)
    angle_from_y = (np.pi/2)+v1xyAngle

else:
    angle_from_y = v1xyAngle

print("angle1xy: "+ str(angle_from_y))

v2xyProjection = np.sqrt((v2[0]**2)+(v2[1]**2))
v2xyAngle = math.asin(v2[0]/v2xyProjection) # denom only 0 if x and y components both 0
print(v2xyProjection)
print(v2xyAngle)

if v2xyAngle<0 and v2[1]<0:
    #in q3 (negative X, negative Y)
    angle_from_y2 = (-np.pi/2)+v2xyAngle

elif v2xyAngle>0 and v2[1]<0:
    #in q4 (positive X, negative Y)
    angle_from_y2 = (np.pi/2)+v2xyAngle

else:
    angle_from_y2 = v2xyAngle

print("angle2xy: "+ str(angle_from_y2))

v1zAngle = math.acos(v1xyProjection/v1mag)
v2zAngle = math.acos(v2xyProjection/v2mag) 

if math.isnan(v1xyAngle) or math.isnan(v2xyAngle): #handles case where no XY projection (only Z) in either vector
    xyplane_rotation = 0
else:
    xyplane_rotation = angle_from_y2-angle_from_y
print("rotate this much in XY plane: "+str(round(np.rad2deg(xyplane_rotation),2)))

zrotation = v2zAngle-v1zAngle
print("rotate this much in Z direction: "+str(round(np.rad2deg(zrotation),2)))