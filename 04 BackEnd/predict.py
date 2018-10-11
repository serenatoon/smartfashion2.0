# This script outputs predictions on material and clothing-type using SVM
# of the input image(s)
# Author: Serena Toon (stoo718@aucklanduni.ac.nz)

from sklearn.externals import joblib # load svm
from svm import get_features_single
import cv2
import numpy as np

def get_prediction(input_image_filename, param):
    input_image = cv2.imread(input_image_filename)
    img_features = np.concatenate(get_features_single(input_image)).reshape(1,-1)

    if (param == "material"):
        svc = joblib.load('svc2.pkl')
        prediction_label = svc.predict(img_features[0:1])
        if (prediction_label[0] == 1):
            return "leather"
        else:
            return ""
    elif (param == "clothing_type"):
        svc = joblib.load('svc_jacket.pkl')
        prediction_label = svc.predict(img_features[0:1])
        if (prediction_label[0] == 0):
            return "jacket"
        else:
            return "clothing"