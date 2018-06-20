from sklearn.cluster import KMeans
from plot import getTsne
from sklearn.manifold import TSNE
from data_helper import loadTSV

def kmeans(filename, target_name, clusters=8):
    matrix = tsne(filename)
    k = KMeans(n_clusters=clusters).fit_predict(matrix)
    getTsne(filename, target_name, k)

def tsne(filepath):
    return TSNE(random_state=0).fit_transform(loadTSV(filepath))


if __name__ == "__main__":
    kmeans("./data/filtered_Gland.txt", "Tsne-Kmeans_Gland.png", 10)

