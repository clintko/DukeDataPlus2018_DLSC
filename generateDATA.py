import plot
import cluster
import numpy as np
import threading
import time
from data_helper import scanpy, loadTSV

def saveTsne(filename, target_dir):
    (x, y) = plot.getTsne(filename)
    l = len(x)
    with open(target_dir + "tsne.txt", "w+") as o:
        o.write(str(l) + "\n")
        for i in range(l):
            o.write(str(x[i]) + " " + str(y[i]) + "\n")

def saveKmeans(filename, target_dir, k):
    _, k_mask = cluster.kmeans(filename, clusters=k)
    with open(target_dir + "color_mask_" + str(k) + ".txt", "w+") as o:
        for k_ in k_mask:
            o.write(str(k_) + "\n")

def saveGeneList(filename, target_dir):
    sc = scanpy(filename, mingenes=200, mincells=3)
    with open(target_dir + "genelist.txt", "w+") as out:
        for gene in sc.getFilteredGeneList():
            out.write(gene + "\n")

def saveGeneTable(filename, target_dir, k):
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

if __name__ == "__main__":
    threads = []
    start = time.time()
    saveGeneTable("./data/mincell=3_mingene=200/filtered.txt", "./Website/data/PBMC/", 1)
    for k in range(1,9):
        t = threading.Thread(target=saveGeneTable, args=("./data/mincell=3_mingene=200/filtered.txt",
                                                         "./Website/data/PBMC/", k))
        t.start()
        print("start")
        threads.append(t)
    for thread in threads:
        thread.join()
        print("finish")
    end = time.time()
    print("it takes {} minutes to run".format((end - start)/60))
