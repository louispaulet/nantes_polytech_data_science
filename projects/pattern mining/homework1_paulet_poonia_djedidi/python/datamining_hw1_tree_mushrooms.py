# -*- coding: utf-8 -*-
"""DataMining HW1 Tree Mushrooms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v9hmFMrh2P5_eBIFonX92sAkKuPBayB1

First we load the libraries we will need for reading and formatting the input data (pandas for the dataframe structure, train_test_split from sklearn to split the data into test and training sets). 
Then we load DecisionTreeClassifier from Sklearn to use the decision tree model.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

"""The loaded data is parsed like a csv file into a pandas dataframe structure"""

df = pd.read_csv('Mushrooms.01.txt', sep="	", encoding='latin-1')  #invisible separator is some kind of utf arrow in the source file
df

"""We then isolate the label "Comestible" as the desired predictions "y" :"""

y = df.Comestible #these are the labels we want to predict
y

"""Here, we drop useless input columns from our dataset x."""

x = df.drop("Comestible", axis=1) #this is the input data, so we remove the "truth" column (now stored in "y" variable)
x = x.drop("Id", axis=1) #the id is useless as we already have ids and it is not a mushroom caracteristic
x

"""Our data has been cleaned up and separated into x (inputs) and y (desired outputs). We must split it for cross-validation."""

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3) #separate the data into train and test variables

"""Our clean mushroom data is then used to fit the decision tree"""

clf = DecisionTreeClassifier().fit(X_train, y_train)

"""We then display the decision tree"""

from sklearn import tree
tree.plot_tree(clf)

print("We compare the predicted with true results : ")
print("Predicted : " + str(clf.predict(X_test)) + " \n Truth :    "  + str(y_test.values))

percentage = clf.score(X_test, y_test)
percentage

"""We can then show a confusion matrix : in this case, we have a lot of predictions falling outside of the diagonal, which indicate a low accuracy (as the accuracy score confirms)."""

from sklearn.metrics import confusion_matrix
res = confusion_matrix(y_test, clf.predict(X_test)) #create a confusion matrix to display TN/TP/FP/FN
print("Confusion Matrix : ")
print(res)
print(f"Test Set : {len(X_test)}")
print(f"Accuracy = {percentage*100} %")

"""The decision tree gives worse results than the SVM as the split between test and train samples is decisive in the tree classifier structure fitting process. Depending on this split, the accuracy varies between 30% and 85%. This indicates an unbalanced dataset (not enough poisonous mushrooms) and not enough data. If we run this notebook several times, we can emultate a ksplit validation and observe that the variance is too high."""