import pandas as pd
import numpy as np

class data(object):

    def __init__(self, filename):
        self.df = pd.read_table(filename)

    # return a dictionary
    def readFile(self):
        dic = {}
        for column in self.geneList():
            dic[column] = self.df[column].tolist()
        print('dic')
        print(dic)
        return dic

    # return the list of Genes
    def geneList(self):
        result = list(self.df.columns.values)
        print('result[1::]')
        print(result[1::])
        return result[1::]

    # return the list of cell index
    def cellIndex(self):
        print('list(self.df[GENE].values)')
        print(list(self.df['GENE'].values))
        return list(self.df['GENE'].values)

    # return an numpy matrix of the values
    def getMatrix(self):
        dict=self.readFile()
        genes=self.geneList()
        result = np.zeros(shape=(len(genes), len(self.cellIndex())))
        for i in range(0, len(genes)):
            result[i] = dict[genes[i]]
        return np.transpose(result)

if __name__ == "__main__":
    data = data("./data/Airway.tsv").getMatrix()
    print(data)
    print(data.shape)
