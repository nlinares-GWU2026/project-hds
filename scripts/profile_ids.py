from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."]) # Design decision from previous data
# exploration that pandas treats ".." as missing from the start so isna() counts it automatically

# --- Duplicates: Several rows per one individual? ---
genetic_id = anno.iloc[:, 0] # Column 0 is the ID for one dataset (one set of genotype data)
individual_id = anno.iloc[:, 2] # Column 2 appears to be ID for the person, if one person was sequenced more than once, 
#like with capture and shotgun methods the would have ONE individual ID but SEVERAL Genetic
# If unique Genetic IDs equals the number of rows, every row is a separate dataset
print("Rows:", len(anno))
print("Unique Genetic IDs:", genetic_id.nunique())
print("Unique Individual IDs:", individual_id.nunique())

rows_per_person = individual_id.value_counts() # a count of counts. First value_counts() gives each person's number of rows. The second 
# counts how many people have 1 row, how many have 2, etc 
print("\nNumber of people with 1,2,3... rows")
print(rows_per_person.value_counts().sort_index()) # puts list above in order

example = rows_per_person.index[0] # Person with the most rows since value_coutns() sorts from most to fewest.
print("\nThe person with the most rows:")
print(anno.loc[individual_id == example].iloc[:, [0, 2, 14, 21, 26]].to_string()) 
# Printing their rows with the ID, group, data type, and SNP columns (0,2,14,21,26) shows whawt a multi=row person actually looks like

# Publications: what the citation export would draw on
# Three .isna() counts show how complete each publication column is - any gaps would affect the citation export
first_pub = anno.iloc[:, 5]
pub = anno.iloc[:, 6]
doi = anno.iloc[:, 7]
print("\n Misisng first publication:", first_pub.isna().sum())
print("Missing publication:", pub.isna().sum())
print("Misisng DOI:", doi.isna().sum())
both_present = first_pub.notna() & pub.notna() # handles a pandas quirk: a missing value is never considered equal to anything, without this check
# every row with a missing publication would be counted as "different". 
print("Rows where first publication differs:", ((first_pub != pub) & both_present).sum()) # Tells you whether the citation export needs both columns, if 0 one column is enough, if it is large, export should list both papers for individual
print("Unique publications:", pub.nunique())