import pandas as pd

def main():
    df = pd.read_csv("../outputs/clusters/cluster_labels.csv")
    print("Cluster distribution:")
    print(df["cluster"].value_counts())

if __name__ == "__main__":
    main()
