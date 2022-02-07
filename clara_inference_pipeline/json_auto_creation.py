"""
This script automatically creates a json file corresponding to prepared training data (scans and labels).
Nvidia clara requires a json file of this type which would be too time-consuming to do manually for large data sets.
"""

#imports
import numpy as np
import os
import os.path
import json

raw_dir = 'scan' #directory corresponding to scans
label_dir = 'label' #directory corresponding to labels

#used in json creation
data = {}
data['train'] = []
data['validation'] = []

#denote which samples are to be included in validation and test-sets, samples not listed will be in the training set.
val_scans = ['1741L','1741R','1744L','1745R','1751L','1775L','1781R','1781L','1782L','1782R','1787L','1787R','1793R','1793L','1963L','1963R','UNK12R','UNK13R']
test_scans = ['1779L','1780L','1792R']


def json_name(file):
	if "rotate" in file: #handle rotated samples
		prefix = file.split('_label')[0]

		prefix_sample = file.split('_')[0]

		if os.path.isfile(raw_dir+"/"+prefix+".nii") == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+prefix+".nii")
		
		if prefix_sample in val_scans:
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+prefix+".nii",
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
		elif prefix_sample not in test_scans:
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+prefix+".nii",
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})



	else: #label is not rotated
		prefix = file.split('-label')[0]
		prefix_sample = file.split('-')[0]
		
		#identify names of scans which should correspond to each label - handling flipped and non flipped labels
		if "flip" not in file: 
			fn1 = prefix + "_CBCT_CAT_300um_US.nii"
			fn2 = prefix + "_clinical_slice625um_SoftTissueProtocol_US.nii"
			fn3 = prefix + "_clinical_slice625um_TemporalBoneProtocol_US.nii"
			fn4 = prefix + "_clinical_slice1250um_SoftTissueProtocol_US.nii"
			fn5 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_US.nii"
			fn6 = prefix + "_CBCT_CAT_300um_addnoise_130_240_US.nii"
			fn7 = prefix + "_CBCT_CAT_300um_addnoise_240_350_US.nii"
			fn8 = prefix + "_clinical_slice625um_SoftTissueProtocol_addnoise_130_240_US.nii"
			fn9 = prefix + "_clinical_slice625um_SoftTissueProtocol_addnoise_240_350_US.nii"
			fn10 = prefix + "_clinical_slice625um_TemporalBoneProtocol_addnoise_130_240_US.nii"
			fn11 = prefix + "_clinical_slice625um_TemporalBoneProtocol_addnoise_240_350_US.nii"
			fn12 = prefix + "_clinical_slice1250um_SoftTissueProtocol_addnoise_130_240_US.nii"
			fn13 = prefix + "_clinical_slice1250um_SoftTissueProtocol_addnoise_240_350_US.nii"
			fn14 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_addnoise_130_240_US.nii"
			fn15 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_addnoise_240_350_US.nii"
		else:
			fn1 = prefix + "_CBCT_CAT_300um_flip_US.nii"
			fn2 = prefix + "_clinical_slice625um_SoftTissueProtocol_flip_US.nii"
			fn3 = prefix + "_clinical_slice625um_TemporalBoneProtocol_flip_US.nii"
			fn4 = prefix + "_clinical_slice1250um_SoftTissueProtocol_flip_US.nii"
			fn5 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_flip_US.nii"
			fn6 = prefix + "_CBCT_CAT_300um_flip_addnoise_130_240_US.nii"
			fn7 = prefix + "_CBCT_CAT_300um_flip_addnoise_240_350_US.nii"
			fn8 = prefix + "_clinical_slice625um_SoftTissueProtocol_flip_addnoise_130_240_US.nii"
			fn9 = prefix + "_clinical_slice625um_SoftTissueProtocol_flip_addnoise_240_350_US.nii"
			fn10 = prefix + "_clinical_slice625um_TemporalBoneProtocol_flip_addnoise_130_240_US.nii"
			fn11 = prefix + "_clinical_slice625um_TemporalBoneProtocol_flip_addnoise_240_350_US.nii"
			fn12 = prefix + "_clinical_slice1250um_SoftTissueProtocol_flip_addnoise_130_240_US.nii"
			fn13 = prefix + "_clinical_slice1250um_SoftTissueProtocol_flip_addnoise_240_350_US.nii"
			fn14 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_flip_addnoise_130_240_US.nii"
			fn15 = prefix + "_clinical_slice1250um_TemporalBoneProtocol_flip_addnoise_240_350_US.nii"

		#check that raw scans all exist - good for validating that preprocessing ran as intended.
		if os.path.isfile(raw_dir+"/"+fn1) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn1)
		if os.path.isfile(raw_dir+"/"+fn2) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn2)
		if os.path.isfile(raw_dir+"/"+fn3) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn3)
		if os.path.isfile(raw_dir+"/"+fn4) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn4)
		if os.path.isfile(raw_dir+"/"+fn5) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn5)
		if os.path.isfile(raw_dir+"/"+fn6) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn6)
		if os.path.isfile(raw_dir+"/"+fn7) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn7)
		if os.path.isfile(raw_dir+"/"+fn8) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn8)
		if os.path.isfile(raw_dir+"/"+fn9) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn9)
		if os.path.isfile(raw_dir+"/"+fn10) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn10)
		if os.path.isfile(raw_dir+"/"+fn11) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn11)
		if os.path.isfile(raw_dir+"/"+fn12) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn12)
		if os.path.isfile(raw_dir+"/"+fn13) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn13)
		if os.path.isfile(raw_dir+"/"+fn14) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn14)
		if os.path.isfile(raw_dir+"/"+fn15) == False:
			print("The following does not exist: ")
			print(raw_dir+"/"+fn15)

		if prefix_sample in val_scans: #handle validation set data
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn1,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn2,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn3,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn4,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn5,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn6,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn7,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn8,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn9,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn10,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn11,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn12,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn13,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn14,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['validation'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn15,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
		elif prefix_sample not in test_scans:  #handle training set data
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn1,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn2,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn3,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn4,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn5,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn6,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn7,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn8,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn9,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn10,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn11,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn12,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn13,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn14,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})
			data['train'].append({
			    'image': '154um_SphericalCrop_IE_segmentation_data/raw/'+fn15,
			    'label': '154um_SphericalCrop_IE_segmentation_data/label/'+file,
			})

#iterate through label file - one or more scans may correspond to the same labelmap
dir=os.listdir(label_dir)
for i in range(0,len(dir)):
	json_name(dir[i])

#write the json file
with open('154um_datalist_50umgt.json', 'w') as outfile:
    json.dump(data, outfile,indent=4)


