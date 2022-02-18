# Assignment 2 - Negative and Positive Reviews

## How to run

### Path variable

The path variable is set by default to work with my Google Drive path :   

`path = '/content/drive/MyDrive/nantes/tspm/assignment2'`  

It must point to the `assignment2` folder to link all dependencies loading and pickle files to load the long computations faster.

### Neg and Pos folders
These two folders are included in the `assignment2` folder. If they do not work or disappear for some reason, they can be generated again by selecting the text corpus from the original `train-pos` and `train-neg` folders.  

These two folders contain the corpus slices of 7500 documents and a generated file called `export.csv` that contains all the files as well as their filename in two columns. This csv file allows easy and fast import at the beginning of the notebook.  

To re-run the generation (not advised : only do it if `export.csv` files disappeared), run the Notebook `zip_to_csv_tspm_project.ipynb`.  

## How long to run

### 1000 first reviews

This notebook can be executed in less than one hour (approx 45 mins) from start to finish :  
*   prefixSpan of positive and negative datasets with a min frequency of 200 takes around 10 minutes  
*   tokenization takes around 15 minutes for positive and negative datasets combined  
*    closed and maximal patterns use the prefixSpan output and take each 10 minutes  

`whole_review_pos_tokenized_list` and `whole_review_neg_tokenized_list` are pickles (serialized objects) that contain the tokenized first 1000 lines of the dataset. You can load these by following instructions inside to notebook to make the notebook run faster as the tokenization step can be skipped.

### The full dataset

This version runs on the full dataset (7500 reviews) and takes several hours to run to completion.  
The min frequency of prefixSpan is set to 2000 to speed things up, and gives results similar to the previous notebook.  

A folder named `whole` contains `whole_review_pos_tokenized_list` and `whole_review_neg_tokenized_list`. These two files are pickles (serialized objects) that contain the tokenized full dataset. You can load these by following instructions inside to notebook to make the notebook run faster as the tokenization step can be skipped.