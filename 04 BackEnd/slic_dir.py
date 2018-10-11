# slic_dir.py performs background removal on the input image. The largest object
# within the image is preserved in the output image (presumably the clothing piece).
# Author: Ira Sukimin (isuk218@aucklanduni.ac.nz)

import numpy as np
import scipy.misc
from skimage.io import imread
from skimage.measure import regionprops
from skimage.segmentation import slic, mark_boundaries, find_boundaries
from skimage.future import graph
import warnings
warnings.filterwarnings("ignore")

#these variables can be customised, suggested values that 
#are compatible for this project are as indicated
rag_sigma = 230
slic_sigma = 0.55
compactness = 90 #ideally 90~130
n_seg = 100 # ideally 1800~2000 (changed from 1800 to 300 just to speed up processing)
max_iter = 10
runs = 3

#segmentation() selects the largest clustered segment and masks the background
def segmentation(img_source, slic_bounds, index):
	masked_img = np.full_like(img_source, 255)
	for i in range(len(slic_bounds)):
		for j in range(len(slic_bounds[i])):
			if slic_bounds[i][j] == index:
				masked_img[i][j] = img_source[i][j]
	return masked_img

#remove_background() performs segmentation, clustering and masking in order
#to remove the background of the input image
def remove_background(filename):

	print("----------------------")
	print('rag_sigma : ' + str(rag_sigma))
	print('slic_sigma : ' + str(slic_sigma))
	print('n_seg : ' + str(n_seg))
	print('compactness : ' + str(compactness))

	#step 1: load the image
	#path = 'dataset-not_jackets/' + str(filename) + '.jpg'
	path = filename
	img1 = imread(path)
	print('processing ' + str(filename))
	print("----------------------")

	#step 2: segmentation using SLIC
	#compactness balances color proximity and space proximity. 
	#higher values give more weight to space proximity, making superpixel shapes more square/cubic (edges becomes more pixelated) 
	slic1 = slic(img1, n_segments = n_seg , compactness=compactness, max_iter = max_iter,sigma=slic_sigma, enforce_connectivity=1)

	#step 3: find boundaries between segments
	#return bool array where boundaries between labeled regions are True
	slic1_bound = find_boundaries(slic1)

	#step 4: mark boundaries between segments
	slic1_marked = mark_boundaries(img1, slic1)

	#step 5: RAG clustering (Region Adjacency Graph using mean colors)
	rags = [np.zeros_like(slic1)]*runs
	rag_labels = [np.zeros_like(slic1)]*runs
	rag_marked = [np.zeros_like(img1)]*runs

	#used for multiple images
	i = 0
	areas = []
	labels_props = []

	#RAG clustering of superpixels
	#A very large value of sigma could make any two colors behave as though they were similar.
	#for noisy backgrounds, use high sigma, for good plain backgrounds, use low sigma
	rags[i] = graph.rag_mean_color(img1, slic1, mode='similarity', sigma=rag_sigma)
	rag_labels[i] = graph.cut_normalized(slic1, rags[i])

	#N.B regionprops doesnt use label 0 so must offset labels
	rag_labels[i] = rag_labels[i] + 1
	rag_marked[i] = mark_boundaries(img1, rag_labels[i])

	#properties for individual clusters
	properties = regionprops(rag_labels[i])

	for j,prop in enumerate(properties):
		areas.append(prop.area)
		labels_props.append(prop.label)

	out = segmentation(img1, rag_labels[i], labels_props[areas.index(max(areas))])
	
	#outputs the image with its background removed
	scipy.misc.imsave('removed_bg.png', out)



