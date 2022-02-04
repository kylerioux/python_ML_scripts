'''
This script resamples volumes with nearest neighbor interpolation - intended for segmentation labelmaps, as NN interpolation is appropriate for segmentation masks.

file structure:
python script 
	labels folder 
	resampled labels folder (where they will be saved)
'''

import os
import SimpleITK as sitk
import numpy as np

resample_dir = 'lab' #directory of labels to be resampled

save_dir= 'lab_save' #directory to save resampled labels

def BSpline50umUpsample(file):

	output_spacing = 0.150 #desired voxel size

	im=sitk.ReadImage(resample_dir+'/'+file)

	f=sitk.ResampleImageFilter();

	InputSize=np.array(im.GetSize());
	InputSpacing=np.array(im.GetSpacing());


	f.SetOutputSpacing((output_spacing,output_spacing,output_spacing))
	f.SetInterpolator(sitk.sitkNearestNeighbor)
	f.SetDefaultPixelValue(0) 
	OutputSize=np.round(InputSpacing*InputSize/output_spacing).astype(int);

	f.SetSize(OutputSize.tolist())
	f.SetOutputDirection(im.GetDirection())
	f.SetOutputOrigin(im.GetOrigin())

	im2=f.Execute(im)

	sitk.WriteImage(im2,save_dir+"/"+file.replace('.nii','_resampled.nii'))


dir=os.listdir(resample_dir)

for i in range(0,len(dir)):
	BSpline50umUpsample(dir[i])






