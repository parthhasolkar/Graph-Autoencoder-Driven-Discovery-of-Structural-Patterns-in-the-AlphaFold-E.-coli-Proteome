import numpy as np
import os
from scipy.spatial.distance import cdist

INPUT_DIR = "../outputs/contact_maps"
GRAPH_DIR = "../outputs/embeddings"
DIST_THRESHOLD = 8.0

def build_contact_map(coords):
    distances = cdist(coords, coords)
    return (distances <= DIST_THRESHOLD).astype(int)

def main():
    os.makedirs(GRAPH_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".npy")]

    for file in files:
        coords = np.load(os.path.join(INPUT_DIR, file))
        contact_map = build_contact_map(coords)
        np.save(os.path.join(GRAPH_DIR, file), contact_map)

if __name__ == "__main__":
    main()
