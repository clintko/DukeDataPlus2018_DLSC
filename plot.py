import matplotlib.pyplot as plt
from data_helper import data
import numpy as np

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

if __name__ == "__main__":
    getGeneValue("./data/Airway.tsv")
