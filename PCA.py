# import some necessary packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import operator
import plotly


# Try tSNE Plot
from sklearn.manifold import TSNE
# Try Agglomerative Clustering
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from mpl_toolkits.mplot3d import Axes3D

from sklearn.decomposition import IncrementalPCA



def PCA(data, component):
    X = data
    ipca = IncrementalPCA(n_components=component, batch_size=500)
    X_ipca = ipca.fit_transform(X)
    return X_ipca