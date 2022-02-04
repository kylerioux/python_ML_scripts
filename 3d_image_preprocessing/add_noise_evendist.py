'''
this script creates noisy images by adding additive gaussian noise to nii (nifti) data with noise standard deviation uniformly sampled within a specified range.
noise documentation: https://simpleitk.org/doxygen/latest/html/classitk_1_1simple_1_1AdditiveGaussianNoiseImageFilter.html

File Structure:
add_noise_evendist.py
 	scan_directrory - scans which noise will be added to
 	save_dir - where noisy scans will be saved
'''

#imports
import numpy as np
import SimpleITK as sitk
import os

#specify the range of noise you would like to add (standard deviations of noise)
noise_min = 130
noise_max = 240

#specify directory of scans you would like to add noise to
scan_directrory = 'scan'

#specify directory where you would like to save noisy images
save_dir= 'scan_save'

def add_noise(file):
    rand_noise_sd = np.random.uniform(low=noise_min, high=noise_max, size=1) #draw sample from uniform distribution

    im=sitk.ReadImage(scan_directrory+'/'+file)

    f=sitk.AdditiveGaussianNoiseImageFilter()
    f.SetMean(0)
    f.SetStandardDeviation(rand_noise_sd[0])

    im2=f.Execute(im)

    sitk.WriteImage(im2,save_dir+"/"+file.replace('.nii','_addnoise_130_240.nii'))

#iterate through directory of scans
dir=os.listdir(scan_directrory)
for i in range(0,len(dir)):
	add_noise(dir[i])






