import plot
import data_helper
import cluster
import autoencoder
import os
from data_helper import scanpy

def trial(filepath, mingene, mincell, cnum=8):
    # make dir
    data_dir = "./data/" + "mincell=" + str(mincell) + "_mingene=" + str(mingene) + "/"
    graph_dir = "./process_images/" + "mincell=" + str(mincell) + "_mingene=" + str(mingene) + "/"
    model_dir = './model/' + "mincell=" + str(mincell) + "_mingene=" + str(mingene) + "/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # filter data
    filtered = data_dir + "filtered.txt"
    sc = scanpy(filepath, mingenes=mingene, mincells=mincell)
    sc.getScanpy(filtered)

    # train autoencoder
    # autoencoder.train(filtered, model_dir, learning_rate=0.1, batch_size=100, epoch=800)

    # generate tsne
    plot.getTsne(filtered, graph_dir + "tsne.png")

    # generate kmeans
    k, _ = cluster.kmeans(filtered, graph_dir + "tsne with kmeans.png", cnum)

    # generate centroid values
    c = cluster.getCentroids(k, cluster.tsne(filtered), )
    cluster.getGeneofCentroids(filtered, graph_dir + "centroid gene matrix.txt", c)

    # get cell index of centroids
    cindex = [sc.getFilteredCellList()[i] for i in c]
    with open(graph_dir + "centroidCellIndex.txt", "w") as out:
        out.write(str(cindex))

    # get latent space
    autoencoder.getLatentSpace(filtered, data_dir, model_dir)
    latent = data_dir + "latentSpace.txt"

    # generate graphs for latent space
    # generate tsne
    plot.getTsne(latent, graph_dir + "tsne_latent.png")

    # generate kmeans
    cluster.kmeans(latent, graph_dir + "tsne with kmeans_latent.png", cnum)

    # generate centroid values
    c = cluster.getCentroids(k, cluster.tsne(latent), )
    cluster.getGeneofCentroids(latent, graph_dir + "centroid gene matrix_latent.txt", c)

    # get cell index of centroids
    cindex = [sc.getFilteredCellList()[i] for i in c]
    with open(graph_dir + "centroidCellIndex_latent.txt", "w") as out:
        out.write(str(cindex))


if __name__ == "__main__":
    trial("./data/data_indexed_with_label_transposed.csv", mincell=3, mingene=200)
