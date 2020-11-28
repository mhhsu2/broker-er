import os 
from k_means_constrained import KMeansConstrained
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import constant 

df = pd.read_csv(os.path.join(constant.DATA_DIR, "cluster_analysis.csv"))
X = df.drop(columns=["Ticker"]).values
scaler = StandardScaler()
X = scaler.fit_transform(X)

clf = KMeansConstrained(n_clusters=50, size_min=5, size_max=10)
labels = clf.fit_predict(X)

result = {"ticker": df["Ticker"], 
          "clusterId": labels,
         }
cluster_df = pd.DataFrame(result)
cluster_df.to_csv(os.path.join(constant.DATA_DIR, "cluster_result.csv"), index=False)
import pdb; pdb.set_trace()
