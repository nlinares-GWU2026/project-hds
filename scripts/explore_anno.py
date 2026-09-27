import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT
    / "data"
    / "raw"
    / "v66.p1_1240K.aadr.PUB.anno"
)

# Read the CSV using the constructed path
anno = pd.read_csv(DATA_FILE, sep="\t", low_memory=False)

# sep="t/" tells pandas columns separated by tabs, not commas. 
# low_memory=False makes pandas read the whole file before deciding each column's data type. Without, inconsistent guessing about datatypes can happen.

print(anno.shape) # 23089, 49 for rows, columns (instead of 23090 - 1 for header)

# List every column with its position number
for i, col in enumerate(anno.columns): print(i,col)