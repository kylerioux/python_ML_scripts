"""
This script along with isolate_label_islandremoval.py implements taubin smoothing and island removal for network output labelmaps. Spatiial resolution and orin are maintained.

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
import time
import os, sys
import SimpleITK as sitk

from isolate_label_islandremoval import IE_localize_smooth_select_largest #to run island removal and find correct spatial resolution lost during taubin smoothing
	
def main():

	inference_folders = ['Case 1 pre spherecrop/'] #list of folders containing network output inferences 

	for foldername in inference_folders:
		filename_noslash = foldername.split('/')[0] #get file name corresponding to folder (remove '/' suffix)

		execution_start_time = time.time()

		#load the predicted labelmap with nibabel - the shape of this is used 
		img = nib.load(foldername+filename_noslash+'_pred_labelmap.nii.gz')
		data = img.get_fdata()

		#create a vtk NIFTI reader and read in the predicted labelmap
		reader=vtk.vtkNIFTIImageReader()
		reader.SetFileName(foldername+filename_noslash+'_pred_labelmap.nii.gz')
		reader.Update()

		raw_im_sitk = sitk.ReadImage(foldername+filename_noslash+'_pred_labelmap.nii.gz')
		raw_spacing = raw_im_sitk.GetSpacing()
		raw_origin = raw_im_sitk.GetOrigin()

		hdr = reader.GetNIFTIHeader()

		#specify the labels corresponding to segmentation masks
		start_label = 1
		end_label = 2

		#create vtk objects 
		smoother = vtk.vtkWindowedSincPolyDataFilter()
		selector = vtk.vtkThreshold()
		scalars_off = vtk.vtkMaskFields()
		geometry = vtk.vtkGeometryFilter()
		writer = vtk.vtkXMLPolyDataWriter()
		histogram = vtk.vtkImageAccumulate()
		discrete_cubes = vtk.vtkDiscreteMarchingCubes()

		#used as a check later for if a label exists
		histogram.SetInputConnection(reader.GetOutputPort())
		histogram.SetComponentExtent(0, end_label, 0, 0, 0, 0)
		histogram.SetComponentOrigin(0, 0, 0)
		histogram.SetComponentSpacing(1, 1, 1)
		histogram.Update()

		#discrete cubes turns labelmap to poly mesh data
		discrete_cubes.SetInputConnection(reader.GetOutputPort())
		discrete_cubes.GenerateValues(end_label - start_label + 1, start_label, end_label)

		#taubin smooothing params
		file_prefix = 'Label'
		smoothing_iterations = 100
		pass_band = pow(10.0, -4.0*0.5) # gives a nice range of 1-0.0001 from a user input of 0-1
		feature_angle = 90.0

		#taubin smoothing specifications
		smoother.SetInputConnection(discrete_cubes.GetOutputPort())
		smoother.SetNumberOfIterations(smoothing_iterations)
		smoother.BoundarySmoothingOff()
		smoother.FeatureEdgeSmoothingOff()
		smoother.SetFeatureAngle(feature_angle)
		smoother.SetPassBand(pass_band)
		smoother.NonManifoldSmoothingOn()
		smoother.NormalizeCoordinatesOn()
		smoother.Update()
		
		#threshold extracts cells where scalar value in cell satisfies threshold criterion
		selector.SetInputConnection(smoother.GetOutputPort())
		selector.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject().FIELD_ASSOCIATION_CELLS, vtk.vtkDataSetAttributes().SCALARS)

	    	# Strip the scalars from the output - mask fields used to mark which fields in the input dataset get copied to the output
		scalars_off.SetInputConnection(selector.GetOutputPort())
		scalars_off.CopyAttributeOff(vtk.vtkMaskFields().POINT_DATA,
		                         vtk.vtkDataSetAttributes().SCALARS)
		scalars_off.CopyAttributeOff(vtk.vtkMaskFields().CELL_DATA,
		                         vtk.vtkDataSetAttributes().SCALARS)

		# general-purpose filter to extract dataset boundary geometry, topology, and associated attribute data from any type of dataset.
		geometry.SetInputConnection(scalars_off.GetOutputPort())

		#island removal
		connected_components = vtk.vtkPolyDataConnectivityFilter()
		connected_components.SetInputConnection(geometry.GetOutputPort())
		connected_components.SetExtractionModeToLargestRegion()

		dataToStencil = vtk.vtkPolyDataToImageStencil()
		dataToStencil.SetInputConnection(connected_components.GetOutputPort())

		dataToStencil.SetOutputSpacing(raw_spacing)
		#dataToStencil.SetOutputOrigin(raw_origin)

		#create an empty VTK image object
		emptyBinaryLabelMap = vtk.vtkImageData()

		#use the size of the labelmap to specify size of empty object
		extent = [0,data.shape[0],0,data.shape[1],0,data.shape[2]]
		emptyBinaryLabelMap.SetExtent(extent) #set the extent of this empty labelmap based on extent of input
		emptyBinaryLabelMap.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

		#a stencil combines multiple objects- use one as the empty object so only the smoothed volume is considered. This is done to get data to desired type for saving
		stencil = vtk.vtkImageStencil()
		stencil.SetInputData(emptyBinaryLabelMap)
		stencil.SetStencilConnection(dataToStencil.GetOutputPort())
		stencil.ReverseStencilOn()
		
		writer2=vtk.vtkNIFTIImageWriter()
		writer2.SetNIFTIHeader(hdr) #maintain origin - not spatial resolution.
		writer2.SetInputConnection(stencil.GetOutputPort())

		for i in range(start_label, end_label + 1):
			
			# see if the label exists, if not skip it
			frequency = histogram.GetOutput().GetPointData().GetScalars().GetTuple1(i)
			if frequency == 0.0:
				continue

			# select the cells for a given label
			selector.ThresholdBetween(i, i)

			# output the polydata
			output_fn = '{:s}{:d}.vtp'.format(file_prefix, i)
			output_fn2 = '{:s}{:d}.nii'.format(file_prefix, i)
			print('{:s} writing {:s}'.format(os.path.basename(sys.argv[0]), output_fn2))

			writer2.SetFileName(filename_noslash+output_fn2)
			writer2.Write()
		print("--- %s seconds ---" % (time.time() - execution_start_time))
	
		#then run ITK script which does island removal and fixes spacing
		IE_localize_smooth_select_largest(filename_noslash+output_fn2,filename_noslash)
    	

if __name__ == "__main__":
    	main()
