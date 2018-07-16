import matplotlib.pyplot as plt
from data_helper import data
from data_helper import loadTSV, loadCSV
import numpy as np
from sklearn.manifold import TSNE
from seaborn import heatmap


def getGeneValue(filename):
    matrix = data(filename).getMatrix()
    y = []
    for row in matrix[0:]:
        y.append(np.sum(row))

    plt.plot(range(0, matrix.shape[0]), y, "r-")
    plt.title("Sum of gene expressions vs. cell num")
    plt.xlabel("cell")
    plt.ylabel("gene sum")
    plt.savefig("geneValue.png")
    plt.close()

def getTsne(filepath, targetname='', cluster_label=[]):
    try:
        data = loadTSV(filepath)
    except:
        data = loadCSV(filepath)
    X_tsne = TSNE(learning_rate=200, random_state=0).fit_transform(data)
    Xtsne = X_tsne[:, 0]
    Ytsne = X_tsne[:, 1]
    lisXtsne = Xtsne.tolist()
    lisYtsne = Ytsne.tolist()
    if not targetname == '':
        colors = ['black', 'purple', 'red', 'yellow', 'pink', 'grey', 'green', 'bisque', 'blanchedalmond', 'blue',
                  'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate']
        if len(cluster_label) == 0:
            cluster_label = [0] * len(lisXtsne)
        fig = plt.figure(figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
        for i in range(len(lisXtsne)):
            plt.scatter(lisXtsne[i], lisYtsne[i], c=colors[cluster_label[i]])
        plt.title(targetname)
        plt.xlabel('x')
        plt.ylabel('y')
        fig.savefig(targetname)
    return (lisXtsne, lisYtsne)

if __name__ == "__main__":
    getTsne("./data/fakedata_latent.txt", "./process_images/tnse_on_fakedata_latent.png")
