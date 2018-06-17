import pandas as pd
import numpy as np
import scanpy.api as sc

class data(object):
    
    def __init__(self, filename):
        self.df = pd.read_table(filename)
        self.df.set_index("GENE", inplace=True)
        self.df = self.df.transpose()

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

    def saveTransposed(self):
        self.df.to_csv("./data/transposed_Airway.csv")

    def getScanpy(self, mingenes, mincells):
        adata = sc.read_csv("./data/transposed_Airway.csv")

        # filter out insignificant cells
        sc.pp.filter_cells(adata, min_genes=mingenes)

        # filter out insignificant genes
        sc.pp.filter_genes(adata, min_cells=mincells)

        # save to file
        np.savetxt("./data/filtered_Airway.txt", adata.X, delimiter="\t")

def loadTSV(filename):
    return pd.read_table(filename).values

if __name__ == "__main__":
    data = data("./data/Airway.tsv")
    #data.saveTransposed()
#    print(data.df.iloc[:, 0])
    print(data.getMatrix() == data.matrix())