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

# Check geographic coverage by ID-ing rows where both Lat and Long contain missing placeholder strings, returning the total count of samples missing spatial coordinates
# Evaluate date distributions in Date (column 10) by identifying samples with dates recorded below 0 BP (modern benchmarks after 1950) and exactly 0 BP (present day)
lat_missing = anno.iloc[:, 17] == ".."
long_missing = anno.iloc[:, 18] == ".."
print("\nRows missing both lat and long:", (lat_missing & long_missing).sum()) #784
print("Dates below 0 BP:", (anno.iloc[:, 10] < 0).sum()) # 1 (-4)
print("Dates exactly 0 BP:", (anno.iloc[:, 10] == 0).sum()) # 3970 not confirmed if present or unknown

# Loops through 4 specific metadata column indices (Country - 16, Political Entity - 14, Assessment/Quality - 21, Coverage/Pub Status - 47)
# Prints: column index and truncated header name, number of distinct values, frequency of custom AADR missing markers "..", 10 most common categories and their sample counts
for i in [16, 14, 21, 47]: 
    col = anno.columns[i]
    print(f"\n=== Column {i}: {col[:60]} ===")
    print("unique values:", anno[col].nunique()) # Counts distinct values 
    print('".." entries:', (anno[col] == "..").sum())
    print("empty cells:", anno[col].isna().sum()) # Both two lines show missing values in ways AADR might record
    print(anno[col].value_counts().head(10)) # 10 most common values and how often each appears (quality categories)
# Drops missing entries, extracts all unique country names from column 16, sorts alphabetically
# To audit data cleanliness by catching typos, naming variants, or inconsistent formatting across samples
print("\n=== All countries (column 16), sorted ===")
print(sorted(anno.iloc[:, 16].dropna().unique())) # Sorted country list to catch inconsistent spellings and namings 

# Filters the dataset to rows where the sample date is <= 0 BP (column 10)
# Cross tabulates those specific samples against their quality/assess. categories in column 21 to determine whether 0 BP entries correspond to present-day ref individuals, control samples, or uncalibrated entries
print("\n=== Data type for rows at or below 0 BP ===")
print(anno.loc[anno.iloc[:, 10] <= 0, anno.columns[21]].value_counts())
#  Column 21 data type contains mixed casing, mulitple values combined with commas, and free-text notes. Leave a data-type filter out of scope of my tool
# Almost all Shotgun.diplod samples (3726 out of 3800) are dated at 0 BP, and common present-day population codes (TSI, GWD, and CHS) appear frequently. 
# Strongly indicates that 0 BP represents present day samples. Column 12 (full_date) will serve as the final sanity check.

# Full Date Check: Displays 10 most frequent text descriptions for 0 BP rows in Column 12 to verify if it explicity says "present"
cols = [0,10,12,14,21]
short = ["genetic_id", "date_bp", "full_date", "group_id", "data_type"]
at_or_below_zero = anno.iloc[:, 10] <= 0
print("\n=== Full Date text for rows at or below 0 BP ===")
print(anno.loc[at_or_below_zero, anno.columns[12]].value_counts().head(10))

# Uses boolean logic (~ for NOT, | for OR) to find and display the few rows that are <= 0 BP but are not standard shotgun types, plus the -4
unusual = at_or_below_zero & ~anno.iloc[:, 21].isin(["Shotgun.diploid", "Shotgun"])
unusual = unusual | (anno.iloc[:, 10] < 0)
print("\n=== Unusual rows at or below 0 BP ===")
print(anno.loc[unusual].iloc[:, cols].set_axis(short, axis=1).to_string()) # Renames columns for display - preview of short-name mappring for aadrkit