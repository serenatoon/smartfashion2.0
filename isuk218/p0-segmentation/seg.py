#load the image
from skimage import io as skio
#url = 'http://i.stack.imgur.com/SYxmp.jpg'
url = 'https://images.unsplash.com/photo-1508273838848-8d6f5162b102?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=d3fe6235fa5000f4acbe827b83ddeaab&auto=format&fit=crop&w=500&q=60'
img = skio.imread(url)

print("shape of image: {}".format(img.shape))
print("dtype of image: {}".format(img.dtype))

#detect edges
from skimage import filters
sobel = filters.sobel(img)

import matplotlib.pyplot as plt
#matplotlib inline
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['figure.dpi'] = 200

plt.imshow(sobel)

blurred = filters.gaussian(sobel, sigma=2.0)
plt.imshow(blurred) #blur this image a bit to make the edges thicker

#obtaining seeds for the watershed transform
import numpy as np
light_spots = np.array((img > 245).nonzero()).T

light_spots.shape

plt.plot(light_spots[:, 1], light_spots[:, 0], 'o')
plt.imshow(img)
plt.title('light spots in image')

dark_spots = np.array((img < 3).nonzero()).T
dark_spots.shape

plt.plot(dark_spots[:, 1], dark_spots[:, 0], 'o')
plt.imshow(img)
plt.title('dark spots in image')

#making a seed mask
from scipy import ndimage as ndi
bool_mask = np.zeros(img.shape, dtype=np.bool)
bool_mask[tuple(light_spots.T)] = True
bool_mask[tuple(dark_spots.T)] = True
seed_mask, num_seeds = ndi.label(bool_mask)
num_seeds

#applying the watershed
from skimage import morphology
ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)

background = max(set(ws.ravel()), key=lambda g: np.sum(ws == g))
background

background_mask = (ws == background)

plt.imshow(~background_mask)

cleaned = img * ~background_mask
plt.imshow(cleaned)

plt.imshow(cleaned, cmap='gray') #apply a red color to the background to check
plt.imshow(background_mask.reshape(background_mask.shape + (1,)) * np.array([1, 0, 0, 1]))

#picking another group
def draw_group_as_background(ax, group, watershed_result, original_image):
    "Draws a group from the watershed result as red background."
    background_mask = (watershed_result == group)
    cleaned = original_image * ~background_mask
    ax.imshow(cleaned, cmap='gray')
    ax.imshow(background_mask.reshape(background_mask.shape + (1,)) * np.array([1, 0, 0, 1]))
  
background_candidates = sorted(set(ws.ravel()), key=lambda g: np.sum(ws == g), reverse=True)

N = 3
fig, axes = plt.subplots(N, N, figsize=(6, 8))
for i in range(N*N):
    draw_group_as_background(axes.ravel()[i], background_candidates[i], ws, img)
plt.tight_layout()
 
#manually inputting seeds
seed_mask = np.zeros(img.shape, dtype=np.int)
seed_mask[0, 0] = 1 # background
seed_mask[600, 400] = 2 # foreground

ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)

fig, ax = plt.subplots()
draw_group_as_background(ax, 1, ws, img)

seed_mask = np.zeros(img.shape, dtype=np.int)
seed_mask[0, 0] = 1 # background
seed_mask[600, 400] = 2 # foreground
seed_mask[1000, 150] = 2 # left arm

ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)

fig, ax = plt.subplots(1, 2)
ax[0].imshow(img)
draw_group_as_background(ax[1], 1, ws, img)

    
plt.show()
