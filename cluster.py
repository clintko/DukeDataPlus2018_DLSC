from sklearn.cluster import KMeans
from plot import getTsne
import numpy as np
from data_helper import loadTSV

def kmeans(filename, target_name, clusters):
    matrix = loadTSV(filename)
    k = KMeans(n_clusters=clusters).fit_predict(matrix)
    getTsne(filename, target_name, k)

if __name__ == "__main__":
    kmeans("./data/filtered_Gland.txt", "Tsne-Kmeans_Gland.png", 10)

