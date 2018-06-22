from skimage import io as skio
from skimage import filters
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import ndimage as ndi
from skimage import morphology

#step 1: load the image
url = 'http://i.stack.imgur.com/SYxmp.jpg'
#url = 'https://upload.wikimedia.org/wikipedia/commons/e/ee/Nine_steps_stair_in_Lysekil_-_bw.jpg'
#img = skio.imread(url)
img = scipy.ndimage.imread('SYxmp.jpg')
print("shape of image: {}".format(img.shape))
print("dtype of image: {}".format(img.dtype))

#step 2: detect edges
sobel = filters.sobel(img)

#step 3: matplotlib inline
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['figure.dpi'] = 200

plt.imshow(sobel)

blurred = filters.gaussian(sobel, sigma=2.0)
plt.imshow(blurred) #blur this image a bit to make the edges thicker

#step 4: obtaining seeds for the watershed transform
light_spots = np.array((img > 245).nonzero()).T

print("shape of light_spots: {}".format(light_spots.shape))

plt.plot(light_spots[:, 1], light_spots[:, 0], 'o')
plt.imshow(img)
plt.title('light spots in image')

dark_spots = np.array((img < 3).nonzero()).T
print("shape of light_spots: {}".format(dark_spots.shape))

plt.plot(dark_spots[:, 1], dark_spots[:, 0], 'o')
plt.imshow(img)
plt.title('dark spots in image')

#step 5: making a seed mask
bool_mask = np.zeros(img.shape, dtype=np.bool)
bool_mask[tuple(light_spots.T)] = True
bool_mask[tuple(dark_spots.T)] = True
seed_mask, num_seeds = ndi.label(bool_mask)
num_seeds

#step 6: applying the watershed
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

#step 7: picking another group
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
 
#step 8: manually inputting seeds
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
