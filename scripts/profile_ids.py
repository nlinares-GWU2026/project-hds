from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

# --- Duplicates: Several rows? ---
genetic_id = anno.iloc[:, 0]
individual_id = anno.iloc[:, 2]
print("Rows:", len(anno))
print("Unique Genetic IDs:", genetic_id.nunique())
print("Unique Individual IDs:", individual_id.nunique())