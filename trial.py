import plot
import data_helper
import cluster
import autoencoder
import os


def trial(filepath, mingene, mincell):
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
    filter = data_dir + "filtered.txt"
    data_helper.getScanpy(filepath, filter, mincells=mincell, mingenes=mingene)

    # generate tsne
    plot.getTsne(filter, graph_dir + "tsne.png")

    # generate kmeans
    cluster.kmeans(filter, graph_dir + "tsne with kmeans.png")

    # train the autoencoder
    autoencoder.train(filter, model_dir, learning_rate=0.1, batch_size=100, epoch=800)
    autoencoder.getLatentSpace(filter, data_dir, model_dir)
    latent = data_dir + "latentSpace.txt"

    # generate graphs for latent space
    # generate tsne
    plot.getTsne(latent, graph_dir + "tsne_latent.png")

    # generate kmeans
    cluster.kmeans(latent, graph_dir + "tsne with kmeans_latent.png")


if __name__ == "__main__":
    trial("./data/transposed_Airway.csv", mincell=10, mingene=100)