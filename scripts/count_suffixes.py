from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

groups = pd.Series(anno.iloc[:,14].unique()) # Returns each group name once (3879) because suffixes are part of group name, not people
# pd.Series wraps the result back into pandas Series
# .unique() returns plain array which doesn't have pandas text tools 
# regex=False tells pandas to search for the literal text, without it pandas would treat the search text as a regex
for s in ["-o", "_o", "contam", "lc"]:
    hits = groups[groups.str.contains(s, regex=False)]
    print(f"\n=== '{s}': {len(hits)} groups ===") # How many groups contain that text
    print(hits.head(10).to_string(index=False)) # Names without row numbers