from sklearn.cluster import KMeans
from plot import getTsne
import numpy as np
from sklearn.manifold import TSNE
from data_helper import loadTSV

def kmeans(filename, target_name, clusters=8):
    # use kmeans on tsne
    matrix = tsne(filename)

    # get kmeans labels
    k = KMeans(n_clusters=clusters).fit_predict(matrix)

    # generate graph
    getTsne(filename, target_name, k)
    return KMeans(n_clusters=clusters)

def tsne(filepath):
    # get tsne coordinates
    return TSNE(random_state=0).fit_transform(loadTSV(filepath))

def getClosest(lst, centroid):
    # calculate the closest point to the centroid
    min = 100000
    index = -1
    for i in range(len(lst)):
        c = np.linalg.norm(lst[i] - centroid)
        if c < min:
            min = c
            index = i
    return index

def getCentroids(k, matrix):
    # get index of Centroids
    locs = k.fit(matrix).cluster_centers_
    index = []
    for loc in locs:
        index.append(getClosest(matrix, loc))
    return index

def getGeneofCentroids(filename, target, index):
    # save gene lists of centroid cells
    matrix = loadTSV(filename)
    result = np.zeros(shape=(len(index), len(matrix[0])))
    num = 0
    for i in index:
        result[num, :] = matrix[i, :]
    np.savetxt(target, result, delimiter="\t")

if __name__ == "__main__":
    a = getCentroids(kmeans("./data/mincell=50_mingene=100/filtered.txt",
                            "./process_images/mincell=50_mingene=100/Tsne-Kmeans.png", 7),
                     tsne("./data/mincell=50_mingene=100/filtered.txt"))
    getGeneofCentroids("./data/mincell=50_mingene=100/filtered.txt", "./data/mincell=50_mingene=100/centroidCells.txt"
                       , a)

