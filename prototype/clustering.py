import numpy as np
from sklearn.cluster import KMeans
from db import Database



def clustering():

	db = Database()

	tickers, data_vecs = db.clustering_data()

	kmeans = KMeans(n_clusters =10, random_state = 0).fit(data_vecs)
	clusterIds = kmeans.labels_







	print(clusterIds)
	print(tickers)
	print(data_vecs)




if __name__ == "__main__":
	clustering()
