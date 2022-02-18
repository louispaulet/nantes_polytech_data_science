from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def main():
    #load the matrix and the terms of the matrix
    X = np.loadtxt(".\OutputDir\window_matrix.csv", delimiter=",")
    Y = np.loadtxt(".\OutputDir\window_matrix_terms.txt", delimiter="\t", dtype=str)

    #initialize the core concepts
    CoreConcepts = ["navy", "war", "ship"]

    coreConceptsDict = dict()
    coreConceptsSpecializationDict = {core:[] for core in CoreConcepts}
    otherConceptsDict = dict()
    i = 0
    #seperate the matirx data between core concepts data and other concepts data
    for y in Y:
        if y in CoreConcepts:
            coreConceptsDict[y] = X[i]
        else:
            otherConceptsDict[y] = X[i]
        i += 1

    #calculate the similarity between each other concept and each concept
    # then attach other concept to the core concept with highest similarity
    for con, x in otherConceptsDict.items():
        maxVal = 0
        conCluster = ""
        for coreCon, y in coreConceptsDict.items():
            val = cosine_similarity(x.reshape(1, -1), y.reshape(1, -1))
            if val > maxVal:
                maxVal = val
                conCluster = coreCon
        coreConceptsSpecializationDict[conCluster].append(con)

    for core_concept, cluster in coreConceptsSpecializationDict.items():
        print("cluster: " + core_concept)
        print(cluster)



if __name__ == '__main__':
    main()