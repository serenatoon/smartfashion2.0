import numpy as np
import cv2 as cv
import skimage.io as skio

from skimage.segmentation import slic, find_boundaries, relabel_sequential
from skimage.future import graph
from skimage.measure import regionprops

import matplotlib.pyplot as plt

def readImageCvRGB(path):
    """
    Reads image using opencv2

    Args:
        path: the file path of image

    Returns:
        image as numpy array 
    """
    img = cv.imread(path)
    return img[:,:,::-1]

def readImageSkRGB(path):
    """
    Reads image using scikit-image
    
    Args:
        path: the file path of image

    Returns:
        image as numpy array 
    """
    img = skio.imread(path)
    return img

def mask_segment(image, labels, index, mask):
    """
    given a labelled image, the function masks unwanted segments
    by replacing it with the specified mask colour
    
    Args:
        image: source image
        boundaries: boundaries from segmentation
        index: label of segment to keep
        mask: RGB colour of mask
    
    Returns:
        masked image 
    """

    # consider using np.where() as alternative
    
    new_img = np.copy(image)
    for i in range(len(labels)):
        for j in range(len(labels[i])):
            if labels[i][j] != index:
                new_img[i][j] = mask
    return new_img;

def removeBackgroundSeg(image, no_of_segments=400, mask_colour=[255,255,255]):
    """
    Removes the background using SLIC segmentation and RAG clustering to 
    group segments and selecting the largest cluster as the region of interest

    Args:
        image: source image
        no_of_segments: approximate number of segments in algorithm
        mask_colour: RGB colour of mask (default is white)

    Returns:
        foreground image as numpy array 
    """
    # slic segmentation
    sigma_slic = 0.8

    segments = slic(image, no_of_segments, compactness=15, sigma=sigma_slic, enforce_connectivity=1)
    boundaries = find_boundaries(segments)

    # rag clustering
    sigma_rag = 400
    rags = graph.rag_mean_color(image, segments, mode='similarity', sigma=sigma_rag)
    rag_labels = graph.cut_normalized(segments, rags) + 1

    properties = regionprops(rag_labels)
    areas = [prop.area for prop in properties] 
    labels = [prop.label for prop in properties] 

    largest_label = labels[areas.index(max(areas))]
    result = mask_segment(image, rag_labels, largest_label, mask_colour)
    
    return result

def removeBackgroundGrabCut(image, mask_colour=[255,255,255], iterCnt=5):
    """
    removes the background using GrabCut algorithm by using a predefined
    rectangle as the initial mask for the region of interest

    Args:
        image: source image
        mask_colour: RGB colour of mask (default is white)
        iterCnt: number of iterations for the GrabCut algorithm

    Returns:
        foreground image as numpy array 
    """
    height = image.shape[0]
    width = image.shape[1]

    # Set up mask of same dimensions to image
    mask = np.zeros((height, width), np.uint8)

    # arrays used by GrabCut algorithm
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    
    # approx boundary of ROI
    h_brdr = 5
    v_brdr = 50
    rect = (h_brdr,v_brdr,width-h_brdr,height-v_brdr) 
    # prcnt_w = 0.9
    # prcnt_h = 0.9
    # xc1 = np.int(0.5*width*(1-prcnt_w)) 
    # yc1 = np.int(0.5*height*(1-prcnt_h)) 
    # xc2 = np.int(0.5*height*(1+prcnt_h))
    # yc2 = np.int(0.5*width*(1+prcnt_w))
    # rect = (xc1, yc1, xc2, yc2)

    # Performing grabcut algorithm
    cv.grabCut(image, mask, rect, bgdModel, fgdModel, iterCnt, cv.GC_INIT_WITH_RECT)
    
    # convert BGD and FGD possibilities into binary mask
    # 1 is background, 0 is foreground
    mask = np.where((mask==2)|(mask==0),1,0).astype('uint8')

    # replace background with mask colour
    result = np.copy(image)
    result[np.where(mask)] = mask_colour

    return result

def displayImages(Images):
    img_cnt = len(Images)

    if (img_cnt < 2):
        fig = plt.imshow(Images[0])

    else:
        fig, ax = plt.subplots(1, img_cnt, subplot_kw={'adjustable': 'box-forced'})

        for i in range(0,img_cnt):       
            ax[i].imshow(Images[i])

        for a in ax.ravel():
            a.set_axis_off()

    plt.show()

#---------------------------------------------------------#

# path = "Query_Image/002.png"
# imgCv = readImageCvRGB(path)
# imgSk = readImageSkRGB(path)

# imgBlur = cv.medianBlur(imgCv, 5)
# imgGaus = cv.GaussianBlur(imgBlur,(5,5),0)

# imgA = removeBackgroundSeg(imgCv, 400)
# imgB = removeBackgroundGrabCut(imgCv)

# display plot
# fig, ax = plt.subplots(1, 2, subplot_kw={'adjustable': 'box-forced'})

# ax[0].imshow(imgCv)    
# ax[0].set_title('CV')
# ax[1].imshow(imgB)    
# ax[1].set_title('Result')

# for a in ax.ravel():
#     a.set_axis_off()

# plt.show()
