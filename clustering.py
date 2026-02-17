import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def main():
    embeddings = np.load("../outputs/embeddings/protein_embeddings.npy")

    kmeans = KMeans(n_clusters=4, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    df = pd.DataFrame({
        "protein_id": range(len(labels)),
        "cluster": labels
    })

    df.to_csv("../outputs/clusters/cluster_labels.csv", index=False)
    print("Clustering completed.")

if __name__ == "__main__":
    main()
