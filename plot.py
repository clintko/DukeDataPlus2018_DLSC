import matplotlib.pyplot as plt
from data_helper import data
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd

# draw hotmap
def getHeatmap(filename):
    a = data(filename).getMatrix()
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()

def getGeneValue(filename):
    matrix = data(filename).getMatrix()
    y = []
    for row in matrix[0:]:
        y.append(np.sum(row))
    fig = plt.figure()
    plt.plot(range(0, matrix.shape[0]), y, "r-")
    plt.title("Sum of gene expressions vs. cell num")
    plt.xlabel("cell")
    plt.ylabel("gene sum")
    fig.savefig("geneValue.png")

def getTsne(filename):
    data = pd.read_table(filename).values
    X_tsne = TSNE().fit_transform(data)
    Xtsne = X_tsne[:, 0]
    Ytsne = X_tsne[:, 1]
    lisXtsne = Xtsne.tolist()
    lisYtsne = Ytsne.tolist()
    fig = plt.figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(lisXtsne)):
        plt.scatter(lisXtsne[i], lisYtsne[i], s=10,)
        plt.title('Autoencoder-100d-tSNE')
        plt.xlabel('x')
        plt.ylabel('y')
    fig.savefig("Autoencoder-100-tSNE.png")

if __name__ == "__main__":
    getTsne("latentSpace.txt")
