from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def main():
    nbClusters = 5 #number of clusters
    #load the data
    X = np.loadtxt(".\OutputDir\window_matrix.csv", delimiter=",")
    #data shuffling
    # np.random.shuffle(X)
    #apply k-means
    kmeans = KMeans(n_clusters=nbClusters, random_state=0).fit_predict(X)
    print(kmeans)
    plt.figure()
    X = PCA(n_components=2).fit_transform(X)
    plt.scatter(X[:, 0], X[:, 1], c=kmeans)
    plt.show()
    clusters = dict()
    for i in range(0, nbClusters):
        clusters[i] = []
    i = 0
    #get the clusters
    with open(".\OutputDir\window_matrix_terms.txt", "r") as f:
        for line in f:
            term = line.strip()
            clusterNb = kmeans[i]
            i += 1
            clusters[clusterNb].append(term)
    for cluster_id, cluster  in clusters.items():
        print("cluster: " + str(cluster_id))
        print(cluster)

if __name__ == '__main__':
    main()