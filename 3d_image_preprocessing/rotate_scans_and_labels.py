'''
This script rotates scans and their associated labelmaps randomly along 3 axis - can specify range of rotational angles with a1_min, a1_max, a2_min, a2_max variables

file structure:
python script 
	raw scans folder
	labels folder 
	rotated raw scans folder (where they will be saved)
	rotated labels folder (where they will be saved)

input scans and labels need not be the same resolution. Output rotated scans and labels will match input label resolution.

This script assumes the following file naming conventions:
scans: "scanIdentifier_somesuffix.nii"
labels: "scanIdentifier_50um_segmentation_IE-label.nii", the suffix can be modified by altering "label_name" in the "scan_flip_iterator" function.
'''

#imports
import numpy as np
import SimpleITK as sitk
import os

#specify directory of scans you would like to rotate
scan_directrory = 'scan_154um'

#specify directory of where labelmaps are (to ensure rotated scans maintain alignment)
label_directrory = 'lab'

#specify directory where you want to save scans
save_dir = 'scan_save'

#specify directory where you want to save labels
save_dir_labels = 'lab_save'

#specify restrictions for how many degrees scan can be rotated by - a1 rotation applied in X direction, a2 in Y and Z, due to some 
#proprocessing methods including the horizontal flipping of scans
a1_min = -90
a1_max = 90
a2_min = -90
a2_max = 90

def resample(image, transform,is_label):
	"""
	This function resamples an image using a specified transform
	:param image: The sitk image we are trying to transform
	:param transform: An sitk transform (ex. resizing, rotation, etc.
	:return: The transformed sitk image
	"""
	reference_image = image

	if is_label:
		interpolator = sitk.sitkNearestNeighbor
		default_value = 0
	else:
		interpolator = sitk.sitkBSpline
		default_value = -3000

	return sitk.Resample(image, reference_image, transform, interpolator, default_value)

def resample_labelmap(image,label):
	"""
	this function resamples the labelmap to match the scan grid. This is essential to allow alignment to be maintained when rotation is applied.
	"""
	return sitk.Resample(label, image, sitk.Transform(), sitk.sitkNearestNeighbor, 0, label.GetPixelID())


def upsample(im,res):
	"""
	this function upsamples the raw scan to match the resolution of the labelmap
	"""
	f=sitk.ResampleImageFilter();

	InputSize=np.array(im.GetSize());
	InputSpacing=np.array(im.GetSpacing());

	f.SetOutputSpacing((res[0],res[1],res[2]))
	f.SetInterpolator(sitk.sitkBSpline)
	f.SetDefaultPixelValue(-3000) # pad with black instead of gray
	#OutputSize=np.round(InputSpacing*InputSize/res[0]).astype(int);
	OutputSizeX=np.round(InputSpacing[0]*InputSize[0]/res[0]).astype(int);
	OutputSizeY=np.round(InputSpacing[1]*InputSize[2]/res[1]).astype(int);
	OutputSizeZ=np.round(InputSpacing[2]*InputSize[2]/res[2]).astype(int);
	OutputSize = [OutputSizeX,OutputSizeY,OutputSizeZ]

	#f.SetSize(OutputSize.tolist())
	OutputSize = np.array(OutputSize, dtype='int').tolist()
	f.SetSize(OutputSize)
	f.SetOutputDirection(im.GetDirection())
	f.SetOutputOrigin(im.GetOrigin())

	im2=f.Execute(im)
	return im2

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

def rotation3d(image, theta_x, theta_y, theta_z,is_label):
	"""
	This function rotates an image across each of the x, y, z axes by theta_x, theta_y, and theta_z degrees
	respectively
	:param image: An sitk image
	:param theta_x: The amount of degrees the user wants the image rotated around the x axis
	:param theta_y: The amount of degrees the user wants the image rotated around the y axis
	:param theta_z: The amount of degrees the user wants the image rotated around the z axis
	:return: The rotated image
	"""
	theta_x = np.deg2rad(theta_x)
	theta_y = np.deg2rad(theta_y)
	theta_z = np.deg2rad(theta_z)
	euler_transform = sitk.Euler3DTransform(get_center(image), theta_x, theta_y, theta_z, (0, 0, 0))
	image_center = get_center(image)
	euler_transform.SetCenter(image_center)
	euler_transform.SetRotation(theta_x, theta_y, theta_z)
	resampled_image = resample(image, euler_transform,is_label)
	return resampled_image

def main_iterator(file):
	prefix = file.split("_")[0] #get the scan identifier IE '1932L'
	
	if "flip" in file: #in my case, flipping occured before rotation - this check handles both cases
		label_name = prefix+"_flip_50um_segmentation_IE-label.nii" #to work, labels need this naming convention
	else:
		label_name = prefix+"_50um_segmentation_IE-label.nii" #to work, labels need this naming convention
	
	#load image and associated labelmap
	lab = sitk.ReadImage(label_directrory+'/'+label_name)
	im = sitk.ReadImage(scan_directrory+"/"+file)

	lab_res = lab.GetSpacing()

	img_resample = upsample(im,lab_res) #upsamples the image 

	lab_resample = resample_labelmap(img_resample,lab) #matches the labels to the upsampledscan -> aligns them 

	#randomly select angles to rotate by in each axis
	angle_1 = np.random.uniform(low=a1_min, high=a1_max, size=1)[0]
	angle_2 = np.random.uniform(low=a2_min, high=a2_max, size=1)[0]
	angle_3 = np.random.uniform(low=a2_min, high=a2_max, size=1)[0]

	is_label=1 #can set this based on name of file
	rotated_lab = rotation3d(lab_resample, angle_1, angle_2, angle_3,is_label)

	is_label=0 #can set this based on name of file
	rotated_im = rotation3d(img_resample, angle_1, angle_2, angle_3,is_label)

  	#uncommenting the following line limits the label to just the bounding box of rotated labelmap to save space - otherwise saving full labelmap resampled to scan
	#rotated_lab = crop_labelmap(rotated_lab)

	sitk.WriteImage(rotated_lab,save_dir_labels+"/"+file.replace('.nii','_rotate_label.nii'))
	sitk.WriteImage(rotated_im,save_dir+"/"+file.replace('.nii','_rotate.nii'))

dir=os.listdir(scan_directrory)
for i in range(0,len(dir)): #iterate through the directory of raw scans
	main_iterator(dir[i])












