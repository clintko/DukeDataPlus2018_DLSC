import plot
import cluster
import numpy as np

def saveTsne(filename):
    (x, y) = plot.getTsne(filename)
    l = len(x)
    with open("./Website/data/tsne.txt", "w+") as o:
        o.write(str(l) + "\n")
        for i in range(l):
            o.write(str(x[i]) + " " + str(y[i]) + "\n")

def saveKmeans(filename, k):
    pass

if __name__ == "__main__":
    saveTsne("./data/mincell=3_mingene=200/filtered.txt")
