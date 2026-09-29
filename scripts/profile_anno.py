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
# Findings 
# Date (10): int64 all usable, min = -4 (after 1950) - filter cannot assume dates are 0 or higher, max = 185k BP - huge span beyond 10k BP, median = 1,938 BP - 1/2 of indivs are younger than 2k years
# Lat/Long (17/18): both object bc of ".." ranges run from -55 (S tip of South America) to 75 (Arctic) well within -90 to 90, long stays within -180 to 180, both have 784 missing values - suggests same individuals lack both coords
# SNPs hit (26): int64 all usable, max = 1,150,639 - below 1.2 mil SNPs so plausible, min = 281 SNPs and median is 684,000 - coverage filter is useful so threshold is user's choice

lat_missing = anno.iloc[:, 17] == ".."
long_missing = anno.iloc[:, 18] == ".."
print("\nRows missing both lat and long:", (lat_missing & long_missing).sum()) #784
print("Dates below 0 BP:", (anno.iloc[:, 10] < 0).sum()) # 1 (-4)
print("Dates exactly 0 BP:", (anno.iloc[:, 10] == 0).sum()) # 3970 not confirmed if present or unknown

for i in [16, 14, 21, 47]: 
    col = anno.columns[i]
    print(f"\n=== Column {i}: {col[:60]} ===")
    print("unique values:", anno[col].nunique()) # Counts distinct values 
    print('".." entries:', (anno[col] == "..").sum())
    print("empty cells:", anno[col].isna().sum()) # Both two lines show missing values in ways AADR might record
    print(anno[col].value_counts().head(10)) # 10 most common values and how often each appears (quality categories)
print("\n=== All countries (column 16), sorted ===")
print(sorted(anno.iloc[:, 16].dropna().unique())) # Sorted country list to catch inconsistent spellings and namings 

print("\n=== Data type for rows at or below 0 BP ===")
print(anno.loc[anno.iloc[:, 10] <= 0, anno.columns[21]].value_counts())