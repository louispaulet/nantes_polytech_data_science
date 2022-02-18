import numpy as np
from sklearn.metrics import accuracy_score

def main():
    #load the data and labels
    X = np.loadtxt(".\OutputDir\window_matrix.csv", delimiter=",", dtype=float)
    Y = np.loadtxt(".\OutputDir\window_matrix_terms_labeled.txt", delimiter=",", dtype=str)
    #split the data between training and testing
    from sklearn.model_selection import train_test_split
    data_train, data_test, labels_train, labels_test, couples_train, couples_test = train_test_split(X, Y[:, 1], Y[:, 0], test_size=0.20)

    #build the Knn model
    from sklearn.neighbors import KNeighborsClassifier
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(data_train, labels_train)

    #predict for the testing data
    y = neigh.predict(data_test)
    #pring the results
    print ("accuracy:")
    print (accuracy_score(labels_test, y))
    i = 0
    for couple in couples_test:
        if int(y[i]) - int(labels_test[i]) == 0:
            print(couple + ", " + str(labels_test[i]) + ", " + str(y[i]))
        else:
            print(couple + ", " + str(labels_test[i]) + ", " + str(y[i]))
        i += 1


if __name__ == '__main__':
    main()

