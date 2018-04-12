import numpy as np
import cv2
from helper_functions import create_matrix, percentage_match, resize
from PIL import Image, ImageTk

def create_svm(pos_dir, neg_dir):
    # cvsvm param setup 
    svm_params = dict(kernel_type=cv2.SVM_LINEAR,
                      svm_type=cv2.SVM_C_SVC,
                      C=2.67, gamma=5.383)
    affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR


    # create training matrix info 
    training_info = create_matrix(pos_dir, neg_dir)
    training_mat = training_info[0]
    num_of_img = training_info[1]
    neg_num = training_info[2]

    # set up array of labels 
    pos_array = np.ones(num_of_img, dtype=np.int32)
    neg_array = np.ones(neg_num, dtype=np.int32)
    neg_array.fill(-1)
    labels = np.concatenate((pos_array, neg_array), axis=0)

    # create svm
    svm = cv2.SVM()
    training_mat_float = np.float32(training_mat)
    #labels = np.zeros(1)
    #print labels.size
    svm.train(training_mat_float, labels, params=svm_params)

    # test
    test_img = np.float32(training_mat)
    predic_mat = svm.predict_all(test_img)
    predic_mat_1d = predic_mat.ravel()
    percentage = percentage_match(labels, predic_mat_1d)
    print "MATCH RATE = " + str(percentage)

    return svm


pos_dir = "res/wool/training/"
neg_dir = "res/leather/training/"
#resize(neg_dir, neg_dir, 200, 200)
svm_dir = "res/svm/"
svm = create_svm(pos_dir, neg_dir)
svm.save(svm_dir + "wool.data")