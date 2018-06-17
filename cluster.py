from sklearn.cluster import KMeans
from plot import getTsne
import numpy as np
from data_helper import loadTSV

def kmeans(filename, clusters):
    matrix = loadTSV(filename)
    k = KMeans(n_clusters=clusters).fit_predict(matrix)
    getTsne(filename, "tSNE with kMean", k)

if __name__ == "__main__":
    kmeans("./data/filtered_Airway.txt", 7)

