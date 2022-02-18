import matplotlib.pyplot as plt
import numpy as np

def main():
    X = np.loadtxt(".\OutputDir\window_matrix.csv", delimiter=",")
    sparsity = 1.0 - np.count_nonzero(X) * 1.0 / X.size
    print(sparsity)
    plt.matshow(X)
    plt.show()

if __name__ == '__main__':
    main()