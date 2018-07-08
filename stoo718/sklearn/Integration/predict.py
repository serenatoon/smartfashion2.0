from sklearn.externals import joblib # load svm
from svm import get_features_single
import cv2
import numpy as np

def get_prediction(input_image_filename, param):
    #input_image_filename = 'wool2.png'
    input_image = cv2.imread(input_image_filename)
    img_features = np.concatenate(get_features_single(input_image)).reshape(1,-1)

    if (param == "material"):
        svc = joblib.load('svc2.pkl')
        prediction_label = svc.predict(img_features[0:1])
        if (prediction_label[0] == 0):
            return "leather"
        else:
            return "not leather"
    elif (param == "clothing_type"):
        svc = joblib.load('svc_jacket.pkl')
        prediction_label = svc.predict(img_features[0:1])
        if (prediction_label[0] == 0):
            return "jacket"
        else:
            return "not jacket"