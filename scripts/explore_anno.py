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
# How the columns map to filteres 
# Filter: ID for covertf | Columns: 0 Genetic Identity | Should match the IDs in the `.ind` file, which is how the filter results connect to geno extraction
# Filter: Region | Columns : 16 Political Entity, 15 Locality, 17 -18 Latitude/Longitutde | Country for simple filtering, coordinates allow for bound-box filter
# Filter: Time Period | Columns: 10 Date mean in BP | "BP" means years before 1950 CE, so 5000 BP is about 3050 BCE
# Filter: Population | Columns: 14 Group ID | Likely same labels as .ind file's population column
# Filter: Lineage | Columns: 35 Y haplogroup (ISOGG), 38 mtDNA haplogroup 
# Filter:  Coverage | Columns: 26 SNPs hit on 1240K snpset | Use 26, not 25 or 27-29 because those count SNPs on other panels, and this project uses 1240K panel
# Filter: Quality | Columns: 47 ASSESSMENT