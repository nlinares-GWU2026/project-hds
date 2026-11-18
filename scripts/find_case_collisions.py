from pathlib import Path
from aadrkit import load_anno

ROOT = Path(__file__).resolve().parent.parent
anno = load_anno(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno")

labels = anno["group_id"].dropna(). drop_duplicates()
collide = labels[labels.str.casefold().duplicated(keep=False)]
print("Labels that differ only by capitalization:", collide.tolist())

rows = anno[anno["group_id"].isin(collide)]
print(rows[["genetic_id", "group_id", "country", "date_bp", "publication"]].to_string())