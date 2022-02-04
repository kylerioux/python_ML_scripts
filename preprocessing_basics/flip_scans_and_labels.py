"""
file structure:
flip_labels_and_scans.py
	 scan_directrory - raw scans folder
	 label_directrory - labels folder 
	 save_dir_scan - flipped scans folder (where they will be saved)
	 save_dir_labels - flipped labels folder (where they will be saved)

This script flips nii (nifti) labels and scans along the sagittal plane. The plane flipping occurs on can be modified by changing the transformation matrix in the flip3dlabel and flip3dscan functions.

This script assumes the following file naming conventions:
scans: "scanIdentifier_somesuffix.nii"
labels: "scanIdentifier_50um_segmentation_IE-label.nii", the suffix can be modified by altering "label_name" in the "scan_flip_iterator" function.
note that scanIdentifier should be unique.
"""

#imports
import numpy as np
import SimpleITK as sitk
import os

#specify directory of scans you would like to flip
scan_directrory = 'scan_154um'

#specify directory of where labelmaps are 
label_directrory = 'lab'

#specify directory where you want to save flipped scans
save_dir_scan = 'scan_save'

#specify directory where you want to save flipped labels
save_dir_labels = 'lab_save'

def get_center(img):
	"""
	This function returns the physical center point of a 3d sitk image
	:param img: The sitk image we are trying to find the center of
	:return: The physical center point of the image
	"""

	width, height, depth = img.GetSize()
	return img.TransformIndexToPhysicalPoint((int(np.ceil(width/2)),
		                          int(np.ceil(height/2)),
		                          int(np.ceil(depth/2))))

def flip3dlabel(img):
	"""
	This function flips the sitk label passeed to it with NN interpolation
	:param img: An sitk labelmap
	:return: The flipped label
	"""

	affineTrans = sitk.AffineTransform(3)
	image_center = get_center(img)
	affineTrans.SetMatrix([-1,0,0,0,1,0,0,0,1])
	affineTrans.SetCenter(image_center)
	flipped = sitk.Resample(img, affineTrans,sitk.sitkNearestNeighbor)
	return flipped

def flip3dscan(img,lab):
	"""
	This function flips the sitk image passeed to it with BSpline interpolation
	:param img: An sitk image
	:param lab: An sitk label associated with the given image - used to maintain alignment
	:return: The flipped image
	"""

	affineTrans = sitk.AffineTransform(3)
	image_center = get_center(lab)
	affineTrans.SetMatrix([-1,0,0,0,1,0,0,0,1])
	affineTrans.SetCenter(image_center)
	interpolator = sitk.sitkBSpline
	flipped = sitk.Resample(img, img, affineTrans,
		     interpolator, -2000)
	return flipped

def label_flip_iterator(file):
	"""
	This function is called each time a label is flipped. Naming and saving is done here.
	:param file: filename of label
	"""
	
	prefix = file.split("_")[0] #get the sample prefix IE '1932L'
	name_without_filetype = file.split(".nii")[0] #file name before the extension (.nii)
	newname = name_without_filetype+"_flipped.nii"
	
	lab = sitk.ReadImage(label_directrory+'/'+file)
	flipped_lab = flip3dlabel(lab)
	sitk.WriteImage(flipped_lab,save_dir_labels+"/"+newname)#labels are saved with _flipped appended to their original names

def scan_flip_iterator(file):
	"""
	This function is called each time a scan is flipped. Naming and saving is done here.
	:param file: filename of scan
	"""
	
	prefix = file.split("_")[0] #get the scan prefix IE '1932L'
	name_without_filetype = file.split(".nii")[0] #everything before the extension (.nii)
	newname = name_without_filetype+"_flipped.nii"
	label_name = prefix+"_50um_segmentation_IE-label_flipped.nii" #labels corresponding to scans need this naming convention following prefix

	im = sitk.ReadImage(scan_directrory+"/"+file)	
	lab = sitk.ReadImage(save_dir_labels+'/'+label_name)
	flipped_im = flip3dscan(im,lab) #flip the image with respect to its already flipped label
	sitk.WriteImage(flipped_im,save_dir_scan+"/"+newname) #scans are saved with _flipped appended to their original names


dir=os.listdir(label_directrory)
for i in range(0,len(dir)): #iterate through the directory of labels
	label_flip_iterator(dir[i])

dir=os.listdir(scan_directrory)
for i in range(0,len(dir)): #iterate through the directory of raw scans
	scan_flip_iterator(dir[i])






