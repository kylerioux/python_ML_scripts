# File Structure:
# //isolate_label_islandremoval_Kmeans.py
# 	//lab_directrory

# this script applies PCA to a 3d segmentation


import nibabel as nib
import SimpleITK as sitk
import os, sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

lab_directrory = "lab" # directory with input labelmaps
	
def IE_localize_smooth_select_largest(filename):

	#read image and get relevant image 'header' info
	sitk_img = sitk.ReadImage(lab_directrory+'/'+filename)
	sitk_img_origin = sitk_img.GetOrigin()
	sitk_img_spacing = sitk_img.GetSpacing()
	sitk_img_direction = sitk_img.GetDirection()

	#select some label from the labelmap
	np_sitk_img = sitk.GetArrayFromImage(sitk_img) # convert to np array
	print(np_sitk_img)
	print(np.max(np_sitk_img))
	np_sitk_img[np_sitk_img > 2] = 0 # set values greater than specified label to 0
	np_sitk_img[np_sitk_img < 2] = 0 # set values less than specified label to 0
	sitk_img = sitk.GetImageFromArray(np_sitk_img) # np array back to sitk image

	np_sitk_img_cca = sitk.GetArrayFromImage(sitk_img) # convert to np array

	array_to_cluster_IE_positions = []
	searchval = 2 #looking for this labelmap value	
	x_coords = np.where(np_sitk_img_cca == searchval)[0] #x coordinates for defined labelmap value
	y_coords = np.where(np_sitk_img_cca == searchval)[1]
	z_coords = np.where(np_sitk_img_cca == searchval)[2]

	#create one 3-tuple list of coordinates for specified labelmap value ie ([x,y,z],[x2,y2,z2])
	for index, num in enumerate(x_coords, start=0):
        	array_to_cluster_IE_positions.append([x_coords[index],y_coords[index],z_coords[index]])

	#fit kmeans clustering based on indices of specified labelmap
	#kmeans.fit(array_to_cluster_IE_positions)
	pca = PCA(n_components=3)
	print(array_to_cluster_IE_positions)
	pca.fit(array_to_cluster_IE_positions)

	#set values of output labelmap based on clustering results
	#for index, num in enumerate(array_to_cluster_IE_positions, start=0):
        	#np_sitk_img_cca[num[0],num[1],num[2]] =  kmeans.labels_[index]+1

	print(pca.explained_variance_ratio_)
	print(pca.components_)

	#sitk_img = sitk.GetImageFromArray(np_sitk_img_cca) # np array back to sitk image
	#sitk_img.SetOrigin(sitk_img_origin)
	#itk_img.SetSpacing(sitk_img_spacing)
	#sitk_img.SetDirection(sitk_img_direction)

	#sitk.WriteImage(sitk_img,lab_save_directrory+"/"+filename)


	
# iterate through directory of labels
dir=os.listdir(lab_directrory)
for i in range(0,len(dir)):
	IE_localize_smooth_select_largest(dir[i])


