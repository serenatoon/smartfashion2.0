import matplotlib.pyplot as plt
import numpy as np
import scipy.misc
import sys
from skimage import data
from skimage.io import imread
from skimage.measure import regionprops
from skimage.util import img_as_bool, img_as_float, img_as_uint
from skimage.segmentation import slic, mark_boundaries, find_boundaries, relabel_sequential, felzenszwalb, watershed
from skimage import filters
from skimage.color.adapt_rgb import adapt_rgb, each_channel, hsv_value
from skimage.future import graph
import warnings
warnings.filterwarnings("ignore")

def segmentation(img_source, slic_bounds, index):
	masked_img = np.full_like(img_source, 255)
	for i in range(len(slic_bounds)):
		for j in range(len(slic_bounds[i])):
			if slic_bounds[i][j] == index:
				masked_img[i][j] = img_source[i][j]
	return masked_img;


rag_sigma = 230
slic_sigma = 0.55
max_n_seg = 1800
max_iter = 10

runs = 3
filename = 'blackjacket'

compactness = 130 #90~130	
fileindex = 1
n_seg = 1800 #1800~2000


print("----------------------")
print('rag_sigma : ' + str(rag_sigma))
print('slic_sigma : ' + str(slic_sigma))
print('n_seg : ' + str(n_seg))
print('compactness : ' + str(compactness))

path = str(filename) + '.jpg'
img1 = imread(path)
print('processing ' + str(filename))
print("----------------------")

#step 2: segmentation using SLIC
#compactness -> Balances color proximity and space proximity. Higher values give more weight to space proximity, making superpixel shapes more square/cubic.
slic1 = slic(img1, n_segments = n_seg , compactness=compactness, max_iter = max_iter,sigma=slic_sigma, enforce_connectivity=1)

#step 3: find boundaries between segments
#return bool array where boundaries between labeled regions are True
slic1_bound = find_boundaries(slic1)

#step 4: mark boundaries between segments
print("marking boundaries..")
slic1_marked = mark_boundaries(img1, slic1)

fig, subplotArray = plt.subplots(1, 3, sharex=True, sharey=True,  subplot_kw={'adjustable': 'box-forced'})
fig1 = plt.figure("Image Plot")
sub1 = fig1.add_subplot(1,3,1)
sub1.imshow(img1)


sub2 = fig1.add_subplot(1,3,2)
sub2.imshow(slic1_bound)

sub3 = fig1.add_subplot(1,3,3)
sub3.imshow(slic1_marked)	
plt.show()
#step 5: RAG clustering (Region Adjacency Graph using mean colors)
rags = [np.zeros_like(slic1)]*runs
rag_labels = [np.zeros_like(slic1)]*runs
rag_marked = [np.zeros_like(img1)]*runs

subplotArray[0].imshow(slic1_marked)
subplotArray[0].set_title('(a)')

print("done plotting..")
#used for multiple images
i = 0
areas = []
labels_props = []

#rag clustering of superpixels
#A very large value of sigma could make any two colors behave as though they were similar.
#for noisy backgrounds, use high sigma
#for good plain backgrounds, use low sigma
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

subplotArray[1].imshow(rag_marked[i])
subplotArray[1].set_title("(b)")

#extract the largest segment


out = segmentation(img1, rag_labels[i], labels_props[areas.index(max(areas))])
subplotArray[2].imshow(segmentation(img1, rag_labels[i], labels_props[areas.index(max(areas))]))
subplotArray[2].set_title("(c)")

for a in subplotArray.ravel():
	a.set_axis_off()

scipy.misc.imsave(str(filename) + 'rag_sigma' + str(rag_sigma) + '-slic_sigma' + str(slic_sigma) + '-n_seg' + str(n_seg) + '-compactness' + str(compactness) + '.png', out)	

	
plt.tight_layout()
plt.show()
