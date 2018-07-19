import plot
import cluster
import numpy as np
import threading
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os
import time
from data_helper import scanpy, loadTSV

def createDir(target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

def saveTsne(filename, target_dir):
    createDir(target_dir)
    (x, y) = plot.getTsne(filename)
    l = len(x)
    with open(target_dir + "tsne.txt", "w+") as o:
        o.write(str(l) + "\n")
        for i in range(l):
            o.write(str(x[i]) + " " + str(y[i]) + "\n")

def saveKmeans(filename, target_dir, k):
    createDir(target_dir)
    _, k_mask = cluster.kmeans(filename, clusters=k)
    with open(target_dir + "color_mask_" + str(k) + ".txt", "w+") as o:
        for k_ in k_mask:
            o.write(str(k_) + "\n")

def saveGeneList(filename, target_dir):
    createDir(target_dir)
    sc = scanpy(filename, mingenes=200, mincells=3)
    with open(target_dir + "genelist.txt", "w+") as out:
        for gene in sc.getFilteredGeneList():
            out.write(gene + "\n")

def saveGeneTable(filename, target_dir, k):
    createDir(target_dir)
    _, k_mask = cluster.kmeans(filename, clusters=k)
    data = loadTSV(filename)
    indexes = []
    for _ in range(k):
        indexes.append([])
    for index in range(len(k_mask)):
        indexes[k_mask[index]].append(index)
    result = np.zeros(shape=(k, len(data[0])))
    for _ in range(k):
        result[_] = np.mean(data[indexes[_]], axis=0)
    np.savetxt(target_dir + "geneTable_" + str(k) + ".txt", result.transpose(), delimiter="\t")

def savePCA(file, target_dir):
    createDir(target_dir)
    data = loadTSV(file)
    pca = PCA(n_components=10).fit_transform(data)
    print(type(pca))
    np.savetxt(target_dir + "pca.txt", pca, delimiter="\t")

def savePipeline(filtered_filename_after_reduction, filtered_filename, unfiltered_filename, target_dir):
    createDir(target_dir)
    threads = []
    start = time.time()
    # save kmeans color mask
    for k in range(1, 9):
        thread = threading.Thread(target=saveKmeans, args=(filtered_filename_after_reduction, target_dir, k))
        thread.start()
        threads.append(thread)
        print("thread {} started".format(len(threads)))
    # generate gene list
    thread = threading.Thread(target=saveGeneList, args=(unfiltered_filename, target_dir))
    threads.append(thread)
    thread.start()
    print("thread {} started".format(len(threads)))
    for k in range(1, 9):
        thread = threading.Thread(target=saveGeneTable, args=(filtered_filename, target_dir, k))
        thread.start()
        threads.append(thread)
        print("thread {} started".format(len(threads)))
    thread = threading.Thread(target=saveTsne, args=(filtered_filename_after_reduction, target_dir))
    thread.start()
    threads.append(thread)
    print("thread {} started".format(len(threads)))
    for th in threads:
        th.join()
    end = time.time()
    print("It takes {} minutes to finish the pipeline".format((end - start) / 60))



if __name__ == "__main__":
    print(os.getcwd())
    savePCA("./Website/data/Airway/filtered.txt", "./Website/data/Airway/pca/")
    savePipeline("./Website/data/Airway/pca/pca.txt", "./Website/data/Airway/filtered.txt",
                 "./data/Airway.tsv", "./Website/data/Airway/pca/")
    #data = loadTSV("./Website/data/Airway/filtered.txt")
    #print(data.shape)
    #print(np.all(np.isfinite(np.log1p(data))))
