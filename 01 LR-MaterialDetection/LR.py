#This script is intended to perform Logistic Regression on a dataset
#in .mat format in the current directory. To obtain the .mat dataset,
#the matlab script included can be used.
#Author: Ira Sukimin (isuk218@aucklanduni.ac.nz)

import numpy as np 
import matplotlib.pyplot as plt
import scipy.io
import time
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

#0 is splitTest 
#1 is for crossVal 
mode = 0

#set the num of iterations are required
num_iterations = 2

dataset_used = 'mat-datasets/dataset-v3-bw-1.mat'

#for split-testing, change this value accordingly (i.e. 0.1 is 10% testing)
c_test_size = 0.3
solver_type = 'lbfgs'
n = 0
accumulate = []

#initialisation steps - load, reshape, split
im_dataset = scipy.io.loadmat(dataset_used)
im_dataset['label'] = im_dataset['label'].reshape(im_dataset['label'].shape[1:])
logisticRegr = LogisticRegression(solver = solver_type) #make instance of the model

def splitTest():
	
	logisticRegr.fit(train_img, train_lbl)	
	
	#uncomment line below to print a specific prediction, n = image index
	#logisticRegr.predict(test_img[n].reshape(1,-1))
	
	predictions = logisticRegr.predict(test_img) 
	score = logisticRegr.score(test_img, test_lbl)	
	matrix = confusion_matrix(test_lbl, predictions,labels=[0,1])
	
	#uncomment lines below to view each data within the .mat file as the script is running
	#print(matrix)
	#print(predictions)
	#print(test_lbl)
	#print(im_dataset['data'].shape)
	#print(im_dataset['label'].shape)
	
	print('accuracy: ' + str(score))
	#print('test ran on: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	return score
	
def crossValidation():
	score = cross_val_score(logisticRegr, im_dataset['data'], im_dataset['label'], cv=10)
	print('accuracy: ' + str(score.mean()))
	return score.mean()

def misclassified(predictions):
	index = 0
	misclassifiedIndexes = []
	for label, predict in zip(test_lbl, predictions):
		if label != predict: 
			print(misclassifiedIndexes.append(index))
			index +=1

start = time.clock()
while n < num_iterations:
	train_img, test_img, train_lbl, test_lbl = train_test_split(im_dataset['data'], im_dataset['label'], test_size=c_test_size)
	if mode == 0:
		accumulate.append(splitTest())
	elif mode == 1:
		accumulate.append(crossValidation())
	n = n + 1
accumulate = np.array(accumulate)
if mode == 0:
	print('average accuracy over ' + str(num_iterations) + ' iterations: ' + str(accumulate.mean()))
elif mode == 1:
	print('average accuracy over ' + str(num_iterations) + ' iterations: ' + str(accumulate.mean()))
print('time taken(s): ' + str(time.clock() - start))

