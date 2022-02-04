'''
this script isolates a specific label from the labelmap, applies island removal, and then applies K-means clustering

File Structure:
  isolate_label_islandremoval_Kmeans.py
  resample_dir
  save_dir

use-case: after a multi-label inference where clustering a single label may be useful for some geometric analysis 
'''

import nibabel as nib
import SimpleITK as sitk
import os, sys
import numpy as np
from sklearn.cluster import KMeans

lab_directrory = "lab" # directory with input labelmaps
lab_save_directrory = "lab_save"
	
def IE_localize_smooth_select_largest(filename):

	#read image and get relevant image 'header' info
	sitk_img = sitk.ReadImage(lab_directrory+'/'+filename)
	sitk_img_origin = sitk_img.GetOrigin()
	sitk_img_spacing = sitk_img.GetSpacing()
	sitk_img_direction = sitk_img.GetDirection()

	#select some label from the labelmap
	np_sitk_img = sitk.GetArrayFromImage(sitk_img) # convert to np array
	np_sitk_img[np_sitk_img > 1] = 0 # set values greater than specified label to 0
	np_sitk_img[np_sitk_img < 1] = 0 # set values less than specified label to 0
	sitk_img = sitk.GetImageFromArray(np_sitk_img) # np array back to sitk image

	conn_comp = sitk.ConnectedComponentImageFilter()
	cca_image = conn_comp.Execute(sitk_img)
	np_sitk_img_cca = sitk.GetArrayFromImage(cca_image) # convert to np array

	unique, counts =  np.unique(np_sitk_img_cca, return_counts=True)
	max_position = np.argmax(counts) # find position of largest connected comp (background)- should be position 0 as it's first encountered in volume scan
	unique = np.delete(unique, max_position)
	counts = np.delete(counts, max_position)

	max_position = np.argmax(counts)
	val_largest_island = unique[max_position]

	np_sitk_img_cca[np_sitk_img_cca > val_largest_island] = 0 # any voxels not part of largest island set to background
	np_sitk_img_cca[np_sitk_img_cca < val_largest_island] = 0 
	np_sitk_img_cca[np_sitk_img_cca == val_largest_island] = 1 

	#kmeans clustering
	kmeans = KMeans( init="random",n_clusters=2,max_iter=1000)

	array_to_cluster_IE_positions = []
	searchval = 1 #looking for this labelmap value	
	x_coords = np.where(np_sitk_img_cca == searchval)[0] #x coordinates for defined labelmap value
	y_coords = np.where(np_sitk_img_cca == searchval)[1]
	z_coords = np.where(np_sitk_img_cca == searchval)[2]

	#create one 3-tuple list of coordinates for specified labelmap value ie ([x,y,z],[x2,y2,z2])
	for index, num in enumerate(x_coords, start=0):
        	array_to_cluster_IE_positions.append([x_coords[index],y_coords[index],z_coords[index]])

	#fit kmeans clustering based on indices of specified labelmap
	kmeans.fit(array_to_cluster_IE_positions)

	#set values of output labelmap based on clustering results
	for index, num in enumerate(array_to_cluster_IE_positions, start=0):
        	np_sitk_img_cca[num[0],num[1],num[2]] =  kmeans.labels_[index]+1

	sitk_img = sitk.GetImageFromArray(np_sitk_img_cca) # np array back to sitk image
	sitk_img.SetOrigin(sitk_img_origin)
	sitk_img.SetSpacing(sitk_img_spacing)
	sitk_img.SetDirection(sitk_img_direction)

	sitk.WriteImage(sitk_img,lab_save_directrory+"/"+filename)
	
# iterate through directory of labels
dir=os.listdir(lab_directrory)
for i in range(0,len(dir)):
	IE_localize_smooth_select_largest(dir[i])


