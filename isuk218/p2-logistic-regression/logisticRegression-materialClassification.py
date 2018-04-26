import numpy as np 
import matplotlib.pyplot as plt
import scipy.io
import time
from datetime import datetime

start = time.clock()
#Set parameters
dataset_used = 'dataset-v3-bw.mat'
c_test_size = 0.3
c_solver = 'lbfgs'
num_iteration = 10
iteration_count = 0
#Load dataset in .mat format
im_dataset = scipy.io.loadmat(dataset_used)

print('\n======PREVIEW OF DATASET======\n')
#Print out dataset preview and labels
print('dimension of data: ' + str(im_dataset['data'].shape))
print('preview of data: \n' + str(im_dataset['data']))
print('dimension of label: ' + str(im_dataset['label'].shape))
print('1 = leather 0 = wool')
print('preview of label: \n' + str(im_dataset['label']))

from sklearn.model_selection import train_test_split

#Reshape the array to solve length issue before splitting the dataset into training and testing
im_dataset['label'] = im_dataset['label'].reshape(im_dataset['label'].shape[1:])

print('\n=======RESHAPED DATASET=======\n')
#Print out dataset 'data' and 'label' sizes
print('dimension of data after reshaping: ' + str(im_dataset['data'].shape))
print('dimension of label after reshaping: ' + str(im_dataset['label'].shape))

#Splitting Data into Training and Test Sets (set train-test parameters)
train_img, test_img, train_lbl, test_lbl = train_test_split(im_dataset['data'], im_dataset['label'], test_size=c_test_size, random_state=0)

#Import Logistic Regression model
from sklearn.linear_model import LogisticRegression 
logisticRegr = LogisticRegression(solver = c_solver)

#Model is learning the relationship between x (digits) and y (labels)
logisticRegr.fit(train_img, train_lbl)

#Model predict the labels of new data (new images) using the information learned during training process
logisticRegr.predict(test_img[0].reshape(1,-1))

#Predict for Multiple Observations (images) at Once
logisticRegr.predict(test_img[0:10])

print('\n============RESULTS============\n')
#Measuring Model Performance - accuracy (fraction of correct predictions): correct predictions / total number of data points
score = logisticRegr.score(test_img, test_lbl)
print('dataset file used: ' + str(dataset_used))
print('solver used: ' + str(c_solver))
print('test_size: ' + str(c_test_size))
print('accuracy: ' + str(score))
print('time taken(s): ' + str(time.clock() - start))
print('test ran on: ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


'''
# [Logistic Regression Sklearn Documentation](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) <br>
# One thing I like to mention is the importance of parameter tuning. While it may not have mattered much for the toy digits dataset, it can make a major difference on larger and more complex datasets you have. Please see the parameter: solver

# ## Confusion Matrix
# Used for Confusion Matrix
from sklearn import metrics
import seaborn as sns
# A confusion matrix is a table that is often used to describe the performance of a classification model (or "classifier") on a set of test data for which the true values are known. 

# Note: Seaborn needs to be installed for this portion 


!conda install seaborn -y

# Make predictions on test data
predictions = logisticRegr.predict(test_img)

cm = metrics.confusion_matrix(test_lbl, predictions)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


plt.figure(figsize=(9,9))
sns.heatmap(cm_normalized, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {:.3f}'.format(score) 
plt.title(all_sample_title, size = 15);


# ## Display Misclassified images with Predicted Labels


index = 0
misclassifiedIndexes = []
for label, predict in zip(test_lbl, predictions):
    if label != predict: 
        misclassifiedIndexes.append(index)
    index +=1


# In[49]:

plt.figure(figsize=(20,4))
for plotIndex, badIndex in enumerate(misclassifiedIndexes[0:5]):
    plt.subplot(1, 5, plotIndex + 1)
    plt.imshow(np.reshape(test_img[badIndex], (28,28)), cmap=plt.cm.gray)
    plt.title('Predicted: {}, Actual: {}'.format(predictions[badIndex], test_lbl[badIndex]), fontsize = 15)


# ## Checking Performance Based on Training Set Size

# A confusion matrix is a table that is often used to describe the performance of a classification model (or "classifier") on a set of test data for which the true values are known. 

# In[47]:

regr = LogisticRegression(solver = 'lbfgs')


# In[48]:

fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (24,8));
plt.tight_layout()

for plotIndex, sample_size in enumerate([100, 1000, 60000]):
    X_train = train_img[:sample_size].reshape(sample_size, 784)
    y_train = train_lbl[:sample_size]
    regr.fit(X_train, y_train)
    predicted = regr.predict(test_img)
    cm = metrics.confusion_matrix(test_lbl, predicted)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    sns.heatmap(cm_normalized, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r', ax = axes[plotIndex], cbar = False);
    accuracyString = '{:g} Training Samples Score: {:.3f}'.format(sample_size, regr.score(test_img, test_lbl)) 
    axes[plotIndex].set_title(accuracyString, size = 25);

axes[0].set_ylabel('Actual label', fontsize = 30);
axes[1].set_xlabel('Predicted label', fontsize = 30);


# if this tutorial doesn't cover what you are looking for, please leave a comment on the youtube video and I will try to cover what you are interested in. 

# [youtube video](https://www.youtube.com/watch?v=71iXeuKFcQM)
'''