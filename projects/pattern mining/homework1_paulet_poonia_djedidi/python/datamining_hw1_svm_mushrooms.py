# -*- coding: utf-8 -*-
"""DataMining HW1 SVM Mushrooms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fcEsMXGQ_f7_JD2-tlTIQBzDgMG4V_Hb

First we load the libraries we will need for reading and formatting the input data (pandas for the dataframe structure, train_test_split from sklearn to split the data into test and training sets). 
Then we load SVC (a kind of SVM, Support Vector Machine).
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

"""Then we load the text file into google drive so Google colab can access the data.

The loaded data is parsed like a csv file into a pandas dataframe structure
"""

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

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3) #separate the data into train (70%) and test (30%) variables

"""As stated in the libraries import section, we need a SVC model, I chose "linear" as it is the recommended option."""

model = SVC(kernel='linear') #load a model

"""We train the model on the training set with the x inputs and desired y predictions"""

model.fit(X_train, y_train) #train the model

"""First validation : we display a vector containing the predicted classes of the test data. For each "x" input, we ouput a "y" value."""

predictions = model.predict(X_test) #show predictions (0 = poisonous, 1 = comestible) for test set
print(predictions)

"""Here we use the score function to compare predictions to the truth and output a percentage of successful predictions."""

percentage = model.score(X_test, y_test) #show a percentage of accuracy
percentage

"""Then we display a confusion matrix (notice how most predictions fall on the diagonal) and display the size of the test set, as well as the previously observed accuracy to have a nice summary."""

from sklearn.metrics import confusion_matrix
res = confusion_matrix(y_test, predictions) #create a confusion matrix to display TN/TP/FP/FN
print("Confusion Matrix : ")
print(res)
print(f"Test Set : {len(X_test)}")
print(f"Accuracy = {percentage*100} %")

"""There is an imbalance between the classes we are trying to predict (only 6/24 poisonous mushrooms) and the dataset is quite small, so we can expect a high variance and maybe some bad surprises if we were to add poisonous mushrooms with features that match the previously edible ones."""