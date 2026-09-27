from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno", sep="\t", low_memory=False)

# Numeric columns: date (10), latitude (17), longitude (18), 1240K SNPs hit (26)
for i in [10, 17, 18, 26]:
    col = anno.columns[i] # Looks up a column by its position number to avoid typing names 
    nums = pd.to_numeric(anno[col], errors="coerce") # Tries to turn every value into a number. Anything that can't be converted -> "NaN". Counting shows the amount of unusable numbers.
    print(f"\n=== Column {i}: {col[:60]} ===") # Printing only the first 60 chars of each column so output stays readable
    print("pandas dtype:", anno[col].dtype)
    print("values that are not numbers:", nums.isna().sum())
    print(anno.loc[nums.isna(), col].value_counts(dropna=False).head(10)) # Shows what those unusable entries look like and how often each appears (including totally empty cells)
    print(nums.describe()) # Summarizes the values that did convert successfully: count, mean, min, max, quartiles