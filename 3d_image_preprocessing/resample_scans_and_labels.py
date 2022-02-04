'''
This script resamples scans and labels to ensure all are registered (necessary step before used as DL training data)

file structure:
python script 
	raw_directory - scans folder
	label_directory - labels folder 
	save_dir_raw - resampled scans folder (where they will be saved)
	save_dir_labels - resampled labels folder (where they will be saved)

resampling occurs relative to the "resample_basedon" object
This script assumes the following file naming conventions:
scans: "scanIdentifier_CBCT_CAT_300um_US.nii"
       "scanIdentifier_clinical_slice625um_SoftTissueProtocol_US.nii"
	... 3 more suffixes the suffixes can be modified by altering "raw_name" variables in the "main_iterator" function. note that scanIdentifier should be unique.

labels: "scanIdentifier_somesuffix.nii", 
'''

#imports
import numpy as np
import SimpleITK as sitk
import os

#specify directory of where raw scans are 
raw_directory = 'scan_154um'

#specify directory of where labelmaps are (to ensure rotated scans maintain alignment)
label_directory = 'lab'

#specify directory where you want to save raw 
save_dir_raw = 'scan_save'

#specify directory where you want to save labels
save_dir_labels = 'lab_save'

def main_iterator(file):
	prefix = file.split('_')[0]

	#in my case, each sample had 6 registered scans sharing one labelmap
	if "flip" not in file: #as 'flip' augmentation was done in a previous step, have to check if label currently considered is a flipped one.
		raw_name = prefix+'_CBCT_CAT_300um_US.nii'
		raw_name2 = prefix+'_clinical_slice625um_SoftTissueProtocol_US.nii' 
		raw_name3 = prefix+'_clinical_slice625um_TemporalBoneProtocol_US.nii'
		raw_name4 = prefix+'_clinical_slice1250um_SoftTissueProtocol_US.nii' 
		raw_name5 = prefix+'_clinical_slice1250um_TemporalBoneProtocol_US.nii'

	else:
		raw_name = prefix+'_flip_CBCT_CAT_300um_US.nii'
		raw_name2 = prefix+'_flip_clinical_slice625um_SoftTissueProtocol_US.nii' 
		raw_name3 = prefix+'_flip_clinical_slice625um_TemporalBoneProtocol_US.nii'
		raw_name4 = prefix+'_flip_clinical_slice1250um_SoftTissueProtocol_US.nii' 
		raw_name5 = prefix+'_flip_clinical_slice1250um_TemporalBoneProtocol_US.nii'
		
	#load labelmap
	lab = sitk.ReadImage(label_directory+'/'+file)

	#load raw scans
	raw = sitk.ReadImage(raw_directory+'/'+raw_name)
	raw2 = sitk.ReadImage(raw_directory+'/'+raw_name2)
	raw3 = sitk.ReadImage(raw_directory+'/'+raw_name3)
	raw4 = sitk.ReadImage(raw_directory+'/'+raw_name4)
	raw5 = sitk.ReadImage(raw_directory+'/'+raw_name5)

	resample_basedon = raw #specify scan you want other scans to be resampled to - can also select to resample based on label.
	
	#get metadata on scan others are being resampled with respect to
	origin = resample_basedon.GetOrigin()
	spacing = resample_basedon.GetSpacing()
	direction = resample_basedon.GetDirection()
	size = resample_basedon.GetSize()

	#define resample filter and assign above specified values
	f = sitk.ResampleImageFilter() 
	f.SetOutputOrigin(origin)
	f.SetOutputSpacing(spacing)
	f.SetSize(size)
	f.SetOutputDirection(direction)

	f.SetInterpolator(sitk.sitkNearestNeighbor) #NN interpolation always used for labelmaps
	resampled_lab = f.Execute(lab) #execute resampling for label

	f.SetInterpolator(sitk.sitkBSpline) #BSpline interpolation for scans
	#execute resampling for all scans
	resampled_raw = f.Execute(raw)
	resampled_raw2 = f.Execute(raw2)
	resampled_raw3 = f.Execute(raw3)
	resampled_raw4 = f.Execute(raw4)
	resampled_raw5 = f.Execute(raw5)
	
	#save resampled scans and label
	sitk.WriteImage(resampled_raw,save_dir_raw+"/"+raw_name)
	sitk.WriteImage(resampled_raw2,save_dir_raw+"/"+raw_name2)
	sitk.WriteImage(resampled_raw3,save_dir_raw+"/"+raw_name3)
	sitk.WriteImage(resampled_raw4,save_dir_raw+"/"+raw_name4)
	sitk.WriteImage(resampled_raw5,save_dir_raw+"/"+raw_name5)

	sitk.WriteImage(resampled_lab,save_dir_labels+"/"+file)
	
#iterate through the label directory- done this way as one label may have multiple corresponding scans
dir=os.listdir(label_directory)
for i in range(0,len(dir)): #iterate through the directory of raw scans
	main_iterator(dir[i])

