import pandas as pd
import numpy as np
import scanpy.api as sc
import math

class data(object):
    
    def __init__(self, filename):
        self.df = pd.read_table(filename)
        self.df.set_index("GENE", inplace=True)
        self.df = self.df.transpose()
        self.filename = filename

    # return a dictionary
    def readFile(self):
        dic = {}
        cells = self.cellIndex()
        for i in range(0, len(cells)):
            dic[cells[i]] = self.df.iloc[i].tolist()
        return dic
    
    # return the list of cells
    def cellIndex(self):
        result = list(self.df.index.values)
        return result
    
    # return the list of genes
    def geneList(self):
        return list(self.df.columns.values)
    
    # return an numpy matrix of the values
    def getMatrix(self):
        return self.df.values

    def saveTransposed(self, filename):
        self.df.to_csv(filename)

class scanpy(object):
    def __init__(self, filename, mingenes, mincells):
        self.adata = sc.read_csv(filename)

        # filter out insignificant cells
        sc.pp.filter_cells(self.adata, min_genes=mingenes)

        # filter out insignificant genes
        sc.pp.filter_genes(self.adata, min_cells=mincells)

        # log1p
        self.adata.X = np.log(self.adata.X + 1)

        # filter dispersion
        sc.pp.filter_genes_dispersion(self.adata, min_disp=0.5)

    def getScanpy(self, target):
        np.savetxt(target, self.adata.X, delimiter="\t")

    def getFilteredGeneList(self):
        return self.adata.var_names

    def getFilteredCellList(self):
        return self.adata.obs_names

def loadTSV(filename):
    return pd.read_table(filename).values

def loadCSV(filename):
    return pd.read_csv(filename).values

if __name__ == "__main__":
    data = data("./data/Gland.tsv")
    data.saveTransposed("./data/transposed_Gland.csv")
