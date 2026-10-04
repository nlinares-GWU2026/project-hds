from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

cols = [0, 2, 10, 14, 16, 17, 26]
short = ["genetic_id", "individual_id", "date_bp", "group_id", "country", "lat", "snps_1240k"]
view = anno.iloc[:, cols].set_axis(short, axis=1) # smaller version of table with just 7 columns renamed to short names 

def show(label, rows):
    print(f"\n=== {label} ===")
    print(rows.head(3).to_string())

show("Missing coordinates", view[view["lat"].isna()]) # with no latitude
show("Lowest coverage", view.nsmallest(3, "snps_1240k")) # low coverage
show("Canary Islands", view[view["country"] == "Canary Islands"]) 
show("Viking groups", view[view["group_id"].str.contains("Viking")]) # any group name containing "Viking" which is the simple version of the pattern matching 
show("Present-day Tuscans (TSI)", view[view["group_id"] == "TSI"])
show("Unpublished", view[anno.iloc[:, 6] == "Unpublished"])
show("Missing DOI", view[anno.iloc[:, 7].isna()])