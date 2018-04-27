from skimage.feature import hog
import numpy as np
import cv2
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from skopt import gp_minimize
import glob
from datetime import datetime
import time


# feature extraction
def colour_hist(input_image, nbins=32):
    #print(input_image[:,:])
    ch1 = np.histogram(input_image[:,:,0], bins = nbins, range = (0, 256))[0] # [0] is because we need only the histogram, not bins edges
    ch2 = np.histogram(input_image[:,:,1], bins = nbins, range = (0, 256))[0]
    ch3 = np.histogram(input_image[:,:,2], bins = nbins, range = (0, 256))[0]
    return np.hstack((ch1, ch2, ch3))


def bin_spatial(img, size=(16,16)):
    return cv2.resize(img, size).ravel()


def get_features_single(img):
    spatial_size = (32, 32)
    hist_bins = 32

    img_features = [] # define empty list to receive features
    feature_img = np.copy(img)

    # compute spatial features
    spatial_features = bin_spatial(feature_img, size=spatial_size)
    # append to list of img features
    img_features.append(spatial_features)

    # compute colour histogram
    hist = colour_hist(feature_img, nbins=hist_bins)
    # append to list of img features
    img_features.append(hist)

    return img_features


def get_features(images):
    features = []

    # iterate through list of images
    for file_p in images:
        file_features = []
        img = cv2.imread(file_p) # 0 = read as grayscale

        feature_img = np.copy(img)
        file_features = get_features_single(feature_img)
        features.append(np.concatenate(file_features))
        feature_img = cv2.flip(feature_img,1) # augment dataset with flipped images ??
        file_features = get_features_single(feature_img)
        features.append(np.concatenate(file_features))

    return features  # return list of feature vectors


def classify(dir):
    # load data
    images = glob.glob(dir)
    pos_list = []
    neg_list = []

    for image in images:
        if 'wool' in image:
            pos_list.append(image)
        elif 'leather' in image:
            neg_list.append(image)

    # get wool features
    wool_features = get_features(pos_list)
    # get leather features
    leather_features = get_features(neg_list)

    x = np.vstack((wool_features, leather_features)).astype(np.float64)
    # fit a per-column scaler
    x_scaler = StandardScaler().fit(x)
    # apply the scaler to x
    scaled_x = x_scaler.transform(x)
    # define the labels vector
    y = np.hstack((np.ones(len(wool_features)), np.zeros(len(leather_features))))

    # split data into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(scaled_x, y, test_size=0.2)
    svc = LinearSVC(loss='hinge')
    t0 = time.time()
    svc.fit(x_train, y_train)  # train
    print svc.predict(x_test[0:26])
    t2 = time.time()
    print(round(t2-t0, 2), 'seconds to train svc')
    print('accuracy of svc: ', round(svc.score(x_test, y_test,), 4))

    return round(svc.score(x_test, y_test,), 4)


def iterate(iterations):
    avg = 0.000
    t0 = time.time()
    for _ in range(iterations):
        avg += classify(new_dir)
    t2 = time.time()

    print('Average accuracy over ' + str(iterations) + ' iterations: ' + str(avg/iterations))
    print('Time taken: ' + str(round(t2-t0, 2)) + ' seconds')



# pos_dir = "res/wool/*"
# neg_dir = "res/leather/*"
new_dir = "res/new/*"
iterate(500)
#classify(pos_dir, neg_dir)
