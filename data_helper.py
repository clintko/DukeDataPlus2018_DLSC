import pandas as pd
import numpy as np

class data(object):

    def __init__(self, filename):
        self.df = pd.read_table(filename)

    # return a dictionary
    def readFile(self):
        dic = {}
<<<<<<< HEAD
        for column in self.geneList():
            dic[column] = self.df[column].tolist()
        print('dic')
        print(dic)
=======
        genes=self.geneList()
        for i in range(0,len(genes)):
            dic[genes[i]] = self.df.iloc[i].tolist()[1::]
>>>>>>> d2334e3f424ba67cf9c460abaf82565fcfb7e50b
        return dic

    # return the list of cells
    def cellIndex(self):
        result = list(self.df.columns.values)
        print('result[1::]')
        print(result[1::])
        return result[1::]

<<<<<<< HEAD
    # return the list of cell index
    def cellIndex(self):
        print('list(self.df[GENE].values)')
        print(list(self.df['GENE'].values))
=======
    # return the list of genes
    def geneList(self):
>>>>>>> d2334e3f424ba67cf9c460abaf82565fcfb7e50b
        return list(self.df['GENE'].values)

    # return an numpy matrix of the values
    def getMatrix(self):
        dict=self.readFile()
        genes=self.geneList()
        result = np.zeros(shape=(len(genes), len(self.cellIndex())))
        for i in range(0, len(genes)):
            result[i] = dict[genes[i]]
        return result.transpose()

if __name__ == "__main__":
    data = data("./data/Airway.tsv")
    print(data.df.shape)
    print(len(data.geneList()))
    print(data.geneList())
    print(data.cellIndex())
    print(data.getMatrix().shape)