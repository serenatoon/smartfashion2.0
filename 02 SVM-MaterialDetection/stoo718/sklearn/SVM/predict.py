from sklearn.externals import joblib # load svm
from svm import get_features_single
import cv2
import numpy as np

input_image_filename = 'leather.png'
input_image = cv2.imread(input_image_filename)
img_features = np.concatenate(get_features_single(input_image)).reshape(1,-1)

svc = joblib.load('svc.pkl')
prediction_label = svc.predict(img_features[0:1])
if (prediction_label[0] == 0):
	print "leather"
else:
	print "not leather"