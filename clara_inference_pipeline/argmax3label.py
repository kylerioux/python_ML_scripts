"""
This script converts network output probbabilities to segmentation labelmaps. Ie, in 3-label semantic segmentation, output after final layer could be [0.1,0.2,0.7], this script would correspond that voxel to label '2' via argmax.
"""

import os
import numpy as np
import SimpleITK as sitk

def postprocess():

	#list names of files inference is being run on
	list_files = [ 
	'Case 1 pre spherecrop' 
	]

	for file_name in list_files:	
		if os.path.exists("../eval/154um_IE_binary/"+file_name+'/'+file_name+'_background.nii.gz'):
			img = sitk.ReadImage('../eval/154um_IE_binary/'+file_name+'/'+file_name+'_background.nii.gz') #probabilities for background class
			img2 = sitk.ReadImage('../eval/154um_IE_binary/'+file_name+'/'+file_name+'_prediction.nii.gz') #probabilities for first (1) class
	
			raw_scan = sitk.ReadImage('../../inner_ear_50um_segmentation_data/test/154um/'+file_name+'.nii')

			#maintain scan metadata
			original_origin = raw_scan.GetOrigin()
			original_spacing = raw_scan.GetSpacing()
			original_direction = raw_scan.GetDirection()

			data = sitk.GetArrayFromImage(img)
			data2 = sitk.GetArrayFromImage(img2)

			data = np.expand_dims(data, axis=0)
			data2 = np.expand_dims(data2, axis=0)

			x = np.vstack((data, data2)) #stack the probabilities for each class to one array, allowing for argmax operation to run.

			final = np.argmax(x, axis = 0)
			final=final.astype('uint16')
			sitk_img = sitk.GetImageFromArray(final)			
			
			sitk_img.SetOrigin(original_origin)
			sitk_img.SetSpacing(original_spacing)	
			sitk_img.SetDirection(original_direction)									
			sitk.WriteImage(sitk_img,'../eval/154um_IE_binary/'+file_name+'/'+file_name+'_pred_labelmap.nii.gz')			

			#delete probability files 
			os.remove("../eval/154um_IE_binary/"+file_name+"/"+file_name+"_background.nii.gz")
			os.remove("../eval/154um_IE_binary/"+file_name+"/"+file_name+"_prediction.nii.gz")
					
		else:
			print("the file: "+file_name+" does not exist")

def main():
    postprocess()

if __name__ == "__main__":
    main()
