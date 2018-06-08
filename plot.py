import matplotlib.pyplot as plt
from data_helper import data

# draw hotmap
def getHeatmap(filename):
    a = data(filename).getMatrix()
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()

if __name__ == "__main__":
    getHeatmap("./data/Airway.tsv")
