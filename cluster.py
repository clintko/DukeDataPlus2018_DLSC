from sklearn.cluster import KMeans
from plot import getTsne
import numpy as np
from sklearn.mixture import BayesianGaussianMixture
from sklearn.manifold import TSNE
from data_helper import loadTSV, loadCSV
from sklearn.decomposition import IncrementalPCA
import pandas as pd
from sklearn.metrics import adjusted_rand_score


def kmeans(filename, target_name="", clusters=8, raw=False):
    # use kmeans on tsne
    if not raw:
        matrix = tsne(filename)
    else:
        matrix = loadTSV(filename)

    # get kmeans labels
    k = KMeans(n_clusters=clusters).fit_predict(matrix)

    # generate graph
    if not target_name=="":
        getTsne(filename, target_name, k)
    return KMeans(n_clusters=clusters), k


def PCA(data, component):
    X = data
    ipca = IncrementalPCA(n_components=component, batch_size=500)
    X_ipca = ipca.fit_transform(X)
    return X_ipca


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


def getAccuracy(truth_path, label):
    df = pd.read_csv(truth_path, header='infer', index_col=0, sep='\t')
    truth = np.array(list(df.index.values)[2:])
    truth_relation = np.zeros((len(truth), len(truth)))
    label_relation = np.zeros((len(label), len(label)))

    for i in range(len(truth)):
        for j in range(len(truth)):
            if truth[i] == truth[j]:
                truth_relation[i][j] = 0.5
            else:
                truth_relation[i][j] = -0.5

    for i in range(len(label)):
        for j in range(len(label)):
            if label[i] == label[j]:
                label_relation[i][j] = 0.5
            else:
                label_relation[i][j] = -0.5

    accuracy = np.mean(np.abs(truth_relation+label_relation))
    accuracy_rand = adjusted_rand_score(truth, label)

    print("The BDSM accuracy is: {}".format(accuracy))
    print("The RAND accuracy is: {}".format(accuracy_rand))


def getBayesianGaussian(filename, targetname):
    # use Bayesian Gaussian model on tsne
    matrix = tsne(filename)

    # fit the model
    model = BayesianGaussianMixture(n_components=8).fit(matrix)
    label = model.predict(matrix)
    print(label)

    # generate graph
    getTsne(filename, targetname, label)

if __name__ == "__main__":
    #getBayesianGaussian("./data/fakedata_latent.txt", "./process_images/kmeansOnfakeData_latent.png")
    _, k = kmeans("./data/mincell=3_mingene=200/latentSpace.txt",
                  "./process_images/mincell=3_mingene=200/tsne with kmeans_latent.png")
    getAccuracy("./data/pbmc_gene=200_cell=3/filtered_headed.tsv", k)
