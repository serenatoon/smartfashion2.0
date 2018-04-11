import numpy as np 
import matplotlib.pyplot as plt
import scipy.io

# Load dataset in .mat format
im_dataset = scipy.io.loadmat('test-200p-fixed-index.mat')

print(im_dataset['data'].shape)
print(im_dataset['data'])
print(im_dataset['label'].shape)
print(im_dataset['label'])

# Splitting Data into Training and Test Sets
from sklearn.model_selection import train_test_split
#get_ipython().magic('matplotlib inline')

# Reshape the array to solve length issue before splitting the dataset into training and testing
im_dataset['label'] = im_dataset['label'].reshape(im_dataset['label'].shape[1:])
print(im_dataset['data'].shape)
print(im_dataset['label'].shape)

# test_size: what proportion of original data is used for test set
train_img, test_img, train_lbl, test_lbl = train_test_split(im_dataset['data'], im_dataset['label'], test_size=1/7.0, random_state=0)

# Showing Training Digits and Labels
plt.figure(figsize=(20,4))
for index, (image, label) in enumerate(zip(train_img[0:5], train_lbl[0:5])):
    plt.subplot(1, 5, index + 1)
    plt.imshow(np.reshape(image, (200,200)), cmap=plt.cm.gray)
    plt.title('Training: %i\n' % label, fontsize = 20)


print(train_img[1])

# Import Logistic Regression model
from sklearn.linear_model import LogisticRegression 
# Step 2: Make an instance of the Model

# all parameters not specified are set to their defaults, default solver is incredibly slow thats why we change it
logisticRegr = LogisticRegression(solver = 'lbfgs')

# Step 3: Training the model on the data, storing the information learned from the data
# Model is learning the relationship between x (digits) and y (labels)
logisticRegr.fit(train_img, train_lbl)

# Step 4: Predict the labels of new data (new images)
# Uses the information the model learned during the model training process

# Returns a NumPy Array
# Predict for One Observation (image)
logisticRegr.predict(test_img[0].reshape(1,-1))

# Predict for Multiple Observations (images) at Once
logisticRegr.predict(test_img[0:10])

# Measuring Model Performance
# accuracy (fraction of correct predictions): correct predictions / total number of data points
score = logisticRegr.score(test_img, test_lbl)
print(score)

# [Logistic Regression Sklearn Documentation](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) <br>
# One thing I like to mention is the importance of parameter tuning. While it may not have mattered much for the toy digits dataset, it can make a major difference on larger and more complex datasets you have. Please see the parameter: solver

'''
# ## Confusion Matrix
# Used for Confusion Matrix
from sklearn import metrics
import seaborn as sns
# A confusion matrix is a table that is often used to describe the performance of a classification model (or "classifier") on a set of test data for which the true values are known. 

# Note: Seaborn needs to be installed for this portion 

# In[41]:

# !conda install seaborn -y


# In[42]:

# Make predictions on test data
predictions = logisticRegr.predict(test_img)


# In[43]:

cm = metrics.confusion_matrix(test_lbl, predictions)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


# In[44]:

plt.figure(figsize=(9,9))
sns.heatmap(cm_normalized, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {:.3f}'.format(score) 
plt.title(all_sample_title, size = 15);


# ## Display Misclassified images with Predicted Labels

# In[45]:

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

# [youtube video](https://www.youtube.com/watch?v=71iXeuKFcQM)'''
