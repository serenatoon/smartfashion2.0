import matplotlib.pyplot as plt
import numpy as np
import scipy.misc
import sys
from skimage import data
from skimage.io import imread
from skimage.measure import regionprops
from skimage.util import img_as_bool, img_as_float, img_as_uint
from skimage.segmentation import slic, mark_boundaries, find_boundaries, relabel_sequential
from skimage.future import graph
import warnings
warnings.filterwarnings("ignore")

fig, subplotArray = plt.subplots(1, 3, sharex=True, sharey=True,  subplot_kw={'adjustable': 'box-forced'})

#to try -- sigma between 220 and 230 (230 -- too much detail)
filetotal = 30
sigma = 170

while sigma < 251:
	print("----------------------------------------")
	print('sigma : ' + str(sigma))
	fileindex = 1
	while fileindex < (filetotal + 1):
		#step 1: load the image
		filename = 'leather (' + str(fileindex) + ')'
		path = 'dataset-v4/' + str(filename) + '.jpg'
		img1 = imread(path)
		print('processing ' + str(filename))

		#step 2: segmentation using SLIC
		#print("segmentation..")
		slic1 = slic(img1, 400 , compactness=15, sigma=0.9, enforce_connectivity=1)

		#step 3: find boundaries between segments
		#print("finding boundaries..")
		slic1_bound = find_boundaries(slic1)

		#step 4: mark boundaries between segments
		#print("marking boundaries..")
		slic1_marked = mark_boundaries(img1, slic1)

		#step 5: create range of sigma values for RAG clustering (Region Adjacency Graph using mean colors)
		#print("RAG..")

		trials = 3
		rags = [np.zeros_like(slic1)]*trials
		rag_labels = [np.zeros_like(slic1)]*trials
		rag_marked = [np.zeros_like(img1)]*trials

		subplotArray[0].imshow(slic1_marked)
		subplotArray[0].set_title('(a)')

		#used for multiple images
		#higher sigma threshold allows high diff in colour mean
		i = 0
		areas = []
		labels_props = []

		#rag clustering of superpixels
		rags[i] = graph.rag_mean_color(img1, slic1, mode='similarity', sigma=sigma)
		rag_labels[i] = graph.cut_normalized(slic1, rags[i])

		#N.B regionprops doesnt use label 0 so must offset labels 
		rag_labels[i] = rag_labels[i] + 1
		rag_marked[i] = mark_boundaries(img1, rag_labels[i])

		#properties for individual clusters
		properties = regionprops(rag_labels[i])

		for j,prop in enumerate(properties):
			areas.append(prop.area)
			labels_props.append(prop.label)

		subplotArray[1].imshow(rag_marked[i])
		subplotArray[1].set_title("(b)")

		#extract the largest segment
		def extract_segment(img_source, slic_bounds, index):
			masked_img = np.full_like(img_source, 255)
			for i in range(len(slic_bounds)):
				for j in range(len(slic_bounds[i])):
					if slic_bounds[i][j] == index:
						masked_img[i][j] = img_source[i][j]
			return masked_img;

		out = extract_segment(img1, rag_labels[i], labels_props[areas.index(max(areas))])
		subplotArray[2].imshow(extract_segment(img1, rag_labels[i], labels_props[areas.index(max(areas))]))
		subplotArray[2].set_title("(c)")

		for a in subplotArray.ravel():
			a.set_axis_off()

		scipy.misc.imsave('sigma' + str(sigma) + '/' + str(filename) + '.png', out)	
		fileindex += 1
		
	sigma += 10
	
#plt.tight_layout()
#plt.show()
