import os
import gzip
import tempfile
import numpy as np
from Bio.PDB import MMCIFParser

DATA_DIR = "../data"
OUTPUT_DIR = "../outputs/contact_maps"
DIST_THRESHOLD = 8.0

parser = MMCIFParser(QUIET=True)

def extract_ca_coords(file_path):
    with gzip.open(file_path, "rb") as gz, tempfile.NamedTemporaryFile(delete=False, suffix=".cif") as tmp:
        tmp.write(gz.read())
        tmp_path = tmp.name

    structure = parser.get_structure("protein", tmp_path)
    coords = []

    for model in structure:
        for chain in model:
            for residue in chain:
                if "CA" in residue:
                    coords.append(residue["CA"].get_coord())

    os.remove(tmp_path)
    return np.array(coords)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".cif.gz")]

    for file in files:
        coords = extract_ca_coords(os.path.join(DATA_DIR, file))
        np.save(os.path.join(OUTPUT_DIR, file.replace(".cif.gz", ".npy")), coords)

if __name__ == "__main__":
    main()
