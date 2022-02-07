"""
This script is called by a smoothing script to perform island removal for network output labelmaps. Spatiial resolution and orin are maintained.

# inspiration from: https://kitware.github.io/vtk-examples/site/Python/Medical/GenerateModelsFromLabels/
# as well as: https://kitware.github.io/vtk-examples/site/Python/PolyData/PolyDataToImageDataStencil/

Folder structure
vtksmoother(*).py
isolate(*).py
	inference_folders
		scan1
			scan1_label.nii
		scan2
			scan2_label.nii

lab_save_directrory
"""

import nibabel as nib
import vtk
import SimpleITK as sitk
import time
import os, sys
import numpy as np

# inspiration from: https://kitware.github.io/vtk-examples/site/Python/Medical/GenerateModelsFromLabels/
# as well as: https://kitware.github.io/vtk-examples/site/Python/PolyData/PolyDataToImageDataStencil/

lab_save_directrory = "save"
	
def IE_localize_smooth_select_largest(filename_smoothed,filename_original):
	"""
	params: 
	filename_smoothed: Name of the file saved during the run of vtk_taubin_smoother.py
	filename_original Name of the unsmoothed file (used as input to vtk_taubin_smoother.py)
	"""

	execution_start_time = time.time()

	reference_image = sitk.ReadImage(filename_original+'/'+filename_original+'_pred_labelmap.nii.gz')

	sitk_img = sitk.ReadImage(filename_smoothed)
	sitk_img_origin = reference_image.GetOrigin()
	sitk_img_spacing = reference_image.GetSpacing()
	sitk_img_direction = reference_image.GetDirection()

	#select specific label from the labelmap
	np_sitk_img = sitk.GetArrayFromImage(sitk_img) # convert to np array
	np_sitk_img[np_sitk_img > 1] = 0 # modifies the value
	np_sitk_img[np_sitk_img < 1] = 0 # modifies the value
	np_sitk_img[np_sitk_img == 1] = 1 # modifies the value
	sitk_img = sitk.GetImageFromArray(np_sitk_img) # np array back to sitk image

	#connecteds component filter identifies spatially continuous 3d structures in labelmap
	conn_comp = sitk.ConnectedComponentImageFilter()
	cca_image = conn_comp.Execute(sitk_img)
	np_sitk_img_cca = sitk.GetArrayFromImage(cca_image) # convert to np array

	unique, counts =  np.unique(np_sitk_img_cca, return_counts=True)
	max_position = np.argmax(counts) # find position of largest connected component (background)- should be position 0 as it's first encountered in volume scan
	unique = np.delete(unique, max_position) # get rid of background connected component - not useful
	counts = np.delete(counts, max_position)

	max_position = np.argmax(counts) 
	val_largest_island = unique[max_position]

	#get rid of all islands not corresponding to the largest 
	np_sitk_img_cca[np_sitk_img_cca > val_largest_island] = 0 # modifies the value
	np_sitk_img_cca[np_sitk_img_cca < val_largest_island] = 0 # modifies the value
	np_sitk_img_cca[np_sitk_img_cca == val_largest_island] = 1 # modifies the value

	sitk_img = sitk.GetImageFromArray(np_sitk_img_cca) # np array back to sitk image

	#maintain metadata
	sitk_img.SetOrigin(sitk_img_origin)
	sitk_img.SetSpacing(sitk_img_spacing)
	sitk_img.SetDirection(sitk_img_direction)

	sitk.WriteImage(sitk_img,lab_save_directrory+"/"+filename_smoothed+".nii")

