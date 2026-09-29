# AI USAGE LOG 
### Claude had access to my current proposal, project requirements, and project rubric before answering. 
- **Tool:**
- **What I was doing:**
- **What I asked (verbatim):**
- **Exact output (verbatim):**
- **Verificaiton:**
## Entry 1
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Downloading the `.anno` file from AADR
- **What I asked (verbatim):** "How do I download the `.anno` file correctly from Harvard Dataverse via terminal?"
- **Exact output (verbatim):**
## Downloading the `.anno` file

**Which file:** Use the 1240K version. The AADR's own visualizer project took its metadata from the file v66.1240K.aadr.PUB.anno. The 1240K panel is the one the AADR uses to represent the world's published ancient human DNA data at more than a million SNPs at which almost all ancient individuals have been assayed. That makes it the natural default for a tool focused on ancient samples. The HO (Human Origins) version has more modern populations but fewer SNPs.

**1. Open the Dataverse page** at https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/FFIDCW and check that the version shown is 66.0.

**2. Find `v66.1240K.aadr.PUB.anno`** in the file list and click it to open its own page. Dataverse usually lists an MD5 checksum there. Copy it, because you'll use it in step 5.

**3. Download it.** The preferred way is to copy the file's download link and run this in WSL, from your repo folder, with `aadr-project` active:

```bash
wget -O data/raw/v66.1240K.aadr.PUB.anno "PASTE-LINK-HERE"
```

Downloading from the terminal means this exact command can later go into a download script, so your data acquisition is reproducible too. If Dataverse asks you to accept terms first, or if `wget` saves a small web page instead of the data, download it in your browser and move it:

```bash
mv /mnt/c/Users/nelin/Downloads/v66.1240K.aadr.PUB.anno data/raw/
```

If Dataverse offers a choice of formats, pick the original file format.

**4. Check that you got the real file.** First, the file size:

```bash
ls -lh data/raw/
```

Count the tab-separated columns in the header row:

```bash
head -n 1 data/raw/v66.1240K.aadr.PUB.anno | awk -F'\t' '{print NF}'
```

Count the lines:

```bash
wc -l data/raw/v66.1240K.aadr.PUB.anno
```

As a reference point, `aadr-resolve` reported loading v66.0_1240K_public.anno: 23,250 rows × 49 cols. Your numbers should be close to that; `wc -l` also counts the header line. If you see only a few lines or one column, you downloaded a web page instead of the data.

**5. Record checksums.** Compare this to the MD5 from the Dataverse page. If they match, the download is complete and uncorrupted:

```bash
md5sum data/raw/v66.1240K.aadr.PUB.anno
```

Then save a SHA-256 checksum to a file you'll commit:

```bash
sha256sum data/raw/v66.1240K.aadr.PUB.anno > docs/data_checksums.txt
```

Later, anyone can run `sha256sum -c docs/data_checksums.txt` to confirm they have the identical file. Using `>` works here because the checksum file doesn't exist yet. If you ever re-run this command, `noclobber` will refuse to overwrite the file, which protects your record.

**6. Commit the checksum file.** The data itself stays ignored:

```bash
git add docs/data_checksums.txt
```

```bash
git commit -m "Record checksum for AADR v66.0 1240K anno file"
```
## The real filename is different from what I gave you

Look at this part of the `wget` output, in the long redirect link:

```
filename*=UTF-8''v66.p1_1240K.aadr.PUB.anno
```

That's the file's actual name on Dataverse: **`v66.p1_1240K.aadr.PUB.anno`**. The name I gave you came from a secondary source (the ArcGIS visualizer page), not from Dataverse itself. Because `wget -O` saves under whatever name you tell it, the file got my name instead of the real one.

The **`p1`** matters. It most likely means "patch 1": a corrected re-release of v66 made after the original April release. Two things support that:

- **The file date.** `ls -lh` shows `Jun 8`. `wget` keeps the server's last-modified date, so the file was updated in June, about two months after v66.0 came out.
- **The line count.** You have 23,090 lines versus the reference's 23,250 rows. A patch release that corrected or removed some entries would explain that gap. The reference was a third-party example, not ground truth, so a small difference isn't alarming on its own.

For reproducibility and citation, you should record the version you actually have, which is v66.p1, not v66.0.

## Fixing it (one command at a time)

**1. Rename the file to its original name:**

```bash
mv data/raw/v66.1240K.aadr.PUB.anno data/raw/v66.p1_1240K.aadr.PUB.anno
```

**2. Regenerate the checksum file,** since it currently records the old name:

```bash
sha256sum data/raw/v66.p1_1240K.aadr.PUB.anno >| docs/data_checksums.txt
```

This uses `>|` instead of `>`. Your shell has `noclobber` on, so a plain `>` would refuse to overwrite the existing checksum file. `>|` means "yes, I really mean to overwrite this one."

**3. Test the checksum file,** exactly as someone reproducing your work would:

```bash
sha256sum -c docs/data_checksums.txt
```

You should see the filename followed by `OK`.

**4. Commit and push.** You haven't pushed the earlier commit yet, so both go up together:

```bash
git add docs/data_checksums.txt
```

```bash
git commit -m "Use original Dataverse filename (v66.p1) for anno file"
```

```bash
git push
```
- **Verification:** I completed all steps and the file downloaded accurately. MD5 checksum: a2db1ac16f0f3558ed66fb251e1d5c7d. Link to paste "https://dataverse.harvard.edu/api/access/datafile/13994515".

## Entry 2
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Exploring the `.anno` file.
- **What I asked (verbatim):** "Using pandas, can you help me explore this `.anno` file to understand the data better?"
- **Exact output (verbatim):**
The key result is good: **(23089, 49)** matches the line count exactly, so pandas is reading every row correctly, with no quoting or line-break problems hiding in the file.

There's one important issue in how you ran it, though.

## You ran this outside your project environment

Look at the first line of your output:

```
C:/Users/nelin/AppData/Local/Programs/Python/Python314/python.exe
```

That's the **Windows** Python installation, not the `aadr-project` conda environment in WSL. It probably happened through VS Code's "Run Python File" button, which uses whichever Python interpreter VS Code has selected, usually the Windows one.

This matters for two reasons:

- **Reproducibility.** Your `environment.yml` pins pandas 2.3.3, but this run used whatever pandas version happens to be installed in Windows Python. Someone following your README would get the pinned version, so your results and theirs could quietly differ.
- **`convertf` only exists in WSL.** Once the package starts calling `convertf`, running from Windows Python will simply fail. It's better to build the habit of running everything in WSL now.

There's also a smaller issue: the script is in `src/`, which is where the `aadrkit` package will live. Exploration scripts aren't part of the package, so they belong in their own folder. Keep the script and commit it, though. It's a useful record of how you explored the data.

### The fix (one command at a time, in a WSL terminal)

**1. Go to your repo.** WSL sees your Windows drive under `/mnt/c`, and the quotes handle the spaces in your folder names:

```bash
cd "/mnt/c/Users/nelin/Desktop/GWU Information/GWU Fall 2026/Applied_Computing/project-hds"
```

**2. Create a `scripts` folder and move the script into it:**

```bash
mkdir -p scripts
```

```bash
mv src/explore_anno.py scripts/
```

**3. Check the file path inside the script.** It should be `"data/raw/v66.p1_1240K.aadr.PUB.anno"`, a path relative to the repo root. If it's `../data/...` or a full `C:/...` path, change it. A `C:/` path won't exist on anyone else's computer, and you'll always run scripts from the repo root.

**4. Run it in the project environment:**

```bash
conda activate aadr-project
```

```bash
python scripts/explore_anno.py
```

You should get the same `(23089, 49)` and column list, this time produced by the pinned environment.

If you like working in VS Code: running `code .` from your WSL terminal opens the folder in WSL mode, where you can select `aadr-project` as the interpreter so the Run button uses the right environment.

## What the columns tell us

Here's how the 49 columns map onto the filters promised in your problem statement (region, time period, lineage, coverage):

| Filter | Column(s) | Notes |
|---|---|---|
| ID for `convertf` | 0 Genetic ID | Should match the IDs in the `.ind` file, which is how the filter results connect to the genotype extraction |
| Region | 16 Political Entity, 15 Locality, 17–18 Latitude/Longitude | Country for simple filtering; coordinates allow a bounding-box filter |
| Time period | 10 Date mean in BP | "BP" means years before 1950 CE, so 5000 BP is about 3050 BCE |
| Population | 14 Group ID | Likely the same labels as the `.ind` file's population column |
| Lineage | 35 Y haplogroup (ISOGG), 38 mtDNA haplogroup | Covers "lineage" from your problem statement |
| Coverage | 26 SNPs hit on 1240k snpset | Use 26, not 25, 27, 28, or 29. Those count SNPs on other panels, and your file is the 1240K panel |
| Quality | 47 ASSESSMENT | A possible "passing samples only" filter |

A few details in the column names will matter once you write code:

- **Column 33 ends in `.1`.** The file has two columns with exactly the same name, so pandas renamed the second one to keep them distinct. If code looks up that column by name, it has to use the `.1` version.
- **Column 25 has a trailing space** at the end of its name. Code that types the name without the space won't find the column. Details like these are why `aadrkit` should store its own short names mapped to the exact real names, tied to the pinned v66.p1 version.
- **Missing values are written as `".."`.** Column 24's description mentions this directly. pandas won't treat `".."` as missing automatically, so numeric columns like dates or SNP counts may load as text. That's exactly what Step 2 will check.
- **One person can have several rows.** Column 0's description explains the suffixes: `.AG`, `.DG`, `.SG`, and others mark different data types for the same individual. A filter could return the same person twice, so you'll need to decide how to handle duplicates.

One idea to think about, not decide now: columns 5–7 hold each individual's publication and DOI. `aadrkit` could export a list of the original papers to cite for whatever subset you extract. That turns the citation obligation in your README into something the tool actually helps with.
- **Verificaiton:** I developed the script Claude wrote and added its suggestion about exporting publications of subsetted individuals to the project proposal. 

## Entry 3
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** After exploring the data, I noticed there were missing values reported as "..". I wanted to know whether the columns contain concrete/clear numbers. 
- **What I asked (verbatim):** "Can you help me develop a script that will profile my columns/data?
- **Exact output (verbatim):**
Nice work keeping the repo updated as you go. Those small, steady commits are exactly what the code rubric looks for.

## Step 2: Profile the numeric columns

Before you can filter by date or coverage, you need to know whether those columns actually contain clean numbers. Last time we saw that AADR writes missing values as `".."`. If a column holds even one `".."`, pandas stores the whole column as text, and a filter like "date greater than 5000" either errors out or silently gives wrong results.

We'll check the four numeric columns your filters depend on: date (10), latitude (17), longitude (18), and 1240K SNPs hit (26). The text columns (country, group, publications, assessment) come next, as a separate step.

Create a new file, `scripts/profile_anno.py`. The first lines can match how your `explore_anno.py` already builds the path:

```python
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False)

# Numeric columns: date (10), latitude (17), longitude (18), 1240K SNPs hit (26)
for i in [10, 17, 18, 26]:
    col = anno.columns[i]
    nums = pd.to_numeric(anno[col], errors="coerce")
    print(f"\n=== Column {i}: {col[:60]} ===")
    print("pandas dtype:", anno[col].dtype)
    print("values that aren't numbers:", nums.isna().sum())
    print(anno.loc[nums.isna(), col].value_counts(dropna=False).head(10))
    print(nums.describe())
```

Here's what each part does:

- **`anno.columns[i]`** looks up a column by its position number, so you don't have to type the long names.
- **`pd.to_numeric(..., errors="coerce")`** tries to turn every value into a number. Anything that can't be converted, like `".."`, becomes `NaN` (pandas' marker for "missing"). Counting the `NaN`s tells you how many entries aren't usable numbers.
- **`value_counts(...)`** shows *what* those unusable entries actually look like, and how often each appears. `dropna=False` includes cells that were completely empty in the file.
- **`describe()`** summarizes the values that did convert: count, mean, minimum, maximum, and quartiles. This is your plausibility check.
- **`col[:60]`** prints only the first 60 characters of each column name, so the output stays readable.

Run it in your WSL terminal from the repo root, with `aadr-project` active:

```bash
python scripts/profile_anno.py
```

## What to look for

- **pandas dtype:** `float64` or `int64` means the column is already clean numbers. `object` means pandas treated it as text because something non-numeric is in it.
- **Values that aren't numbers:** how many, and what they are, whether `".."`, empty cells, or something unexpected.
- **Minimum and maximum:**
  - **Latitude** must fall between −90 and 90, and **longitude** between −180 and 180. Anything outside those ranges is a data-entry error.
  - **Date** should be 0 or higher. Present-day individuals likely sit at or near 0 BP, and the oldest samples should be in the tens of thousands of years.
  - **SNPs hit** can't exceed the number of SNPs on the 1240K panel, which is a bit over 1.2 million.

Paste me the output, and we'll decide together how `aadrkit` should handle whatever problems turn up. Then commit the script so your exploration stays on record:

```bash
git add scripts/profile_anno.py
```

```bash
git commit -m "Add column profiling for anno file"
```
This is a really informative result. Two of your four columns are perfectly clean, and the other two have one specific, fixable problem. Here's what each one tells us.

## What the output shows

**Date (column 10): clean, with one surprise.**
- `int64` with zero non-numbers means every row has a usable date.
- The **minimum is −4**, not 0. Since BP counts backward from 1950, a negative value means *after* 1950: −4 BP is 1954 CE, most likely a recently sampled present-day individual. So the filter can't assume dates are always 0 or higher.
- The **maximum is 185,000 BP**, which is far older than any modern human sample. The dataset includes some very old, likely archaic individuals, so a user asking for "everything older than 10,000 BP" gets a very wide time span.
- The **median is 1,938 BP**, so half of all individuals are younger than about 2,000 years.

**Latitude and longitude (columns 17 and 18): one known problem.**
- Both are `object` (text) because of **784 `".."` entries**, which is AADR's missing-value marker, exactly as we expected.
- The ranges that did convert are all valid: latitude runs from −55 (roughly the southern tip of South America) to 75 (the Arctic), well within −90 to 90. Longitude stays within −180 to 180.
- Both columns have exactly 784 missing values, which suggests the same individuals lack both coordinates. That still needs confirming (below).

**SNPs hit (column 26): clean.**
- `int64`, no missing values.
- The maximum, 1,150,639, is below the panel's roughly 1.2 million SNPs, so it passes the plausibility check.
- The **minimum is 281 SNPs**, which is extremely low. The middle value is about 684,000. Individuals with very little data are real and present in the file, which is exactly why a coverage filter is useful. The threshold should be the user's choice, not hard-coded, since different analyses need different amounts of data.

## Design decisions this suggests

These are worth writing into `docs/anno_notes.md` in your own words, since they'll shape the package code:

1. **Load the file with `na_values=[".."]`** in `pd.read_csv`. pandas then treats `".."` as missing from the start, and latitude and longitude load as real numbers instead of text.
2. **Don't assume dates are 0 or higher.** Negative BP values are valid.
3. **The date filter uses the mean date (column 10).** Column 11 holds each date's uncertainty, so a more precise "date range overlaps" filter is possible later. The simple version is the right place to start, as long as the documentation says which one it uses.
4. **The region filter should report what it drops.** If someone filters by a coordinate box, individuals without coordinates can't be included. Silently dropping 784 people is a transparency problem, so the tool should print something like "784 individuals have no coordinates and were excluded." The country column may still work for those individuals; we'll check it next.
5. **Coverage threshold is user-chosen,** with no hidden default.

## Two quick checks before moving on

Add these lines to the bottom of `profile_anno.py`:

```python
lat_missing = anno.iloc[:, 17] == ".."
lon_missing = anno.iloc[:, 18] == ".."
print("\nRows missing both lat and lon:", (lat_missing & lon_missing).sum())
print("Dates below 0 BP:", (anno.iloc[:, 10] < 0).sum())
print("Dates exactly 0 BP:", (anno.iloc[:, 10] == 0).sum())
```

- **The first check** confirms whether the 784 missing latitudes and 784 missing longitudes are the same rows. `&` means "both conditions true in the same row."
- **The date checks** show how many individuals are post-1950 or dated exactly at 0. That tells us whether date alone can separate ancient from present-day individuals, which would make an "ancient only" filter straightforward.

Run it again:

```bash
python scripts/profile_anno.py
```

Paste me just those three new lines of output, then commit the updated script. After that, we'll profile the text columns: country, group ID, the publication columns, and the quality assessment.

All three numbers are useful, and one of them raises a question worth checking.

**784 rows missing both coordinates.** The missing latitudes and longitudes are the same 784 individuals, so it's one group of people without a location, not two overlapping problems. A coordinate-based region filter will exclude exactly those 784, and the tool can report that number cleanly.

**1 date below 0 BP.** That's the single −4 BP individual. It's a real edge case, but only one row, and it doesn't break anything as long as the filter doesn't reject negative dates.

**3,970 dates exactly at 0 BP.** This is the interesting one. The AADR includes present-day individuals for comparison, and a date of 0 most likely marks them. If so, "ancient only" could simply mean "date above 0," which would be a very natural filter to offer. But we haven't confirmed that 0 always means "present-day." It's possible some ancient individuals with unknown dates were also entered as 0. That's worth checking before building a filter on the assumption.


## Profile the text columns

This step looks at four text columns and also answers the 0 BP question:

- **16 Political Entity** (country), for the region filter
- **14 Group ID** (population label), for the population filter
- **21 Data type**, which should help identify present-day individuals
- **47 ASSESSMENT** (quality), for a possible quality filter

Add this to the bottom of `profile_anno.py`:

```python
for i in [16, 14, 21, 47]:
    col = anno.columns[i]
    print(f"\n=== Column {i}: {col[:60]} ===")
    print("unique values:", anno[col].nunique())
    print('".." entries:', (anno[col] == "..").sum())
    print("empty cells:", anno[col].isna().sum())
    print(anno[col].value_counts().head(10))

print("\n=== All countries (column 16), sorted ===")
print(sorted(anno.iloc[:, 16].dropna().unique()))

print("\n=== Data type for rows at or below 0 BP ===")
print(anno.loc[anno.iloc[:, 10] <= 0, anno.columns[21]].value_counts())
```

Here's what each piece tells you:

- **`nunique()`** counts distinct values. For example, how many different countries or population groups are in the data.
- **The `".."` and empty-cell counts** show missing values in both of the ways AADR might record them. For text columns, pandas reads a truly blank cell as missing but reads `".."` as ordinary text, so we count them separately.
- **`value_counts().head(10)`** shows the ten most common values and how often each appears. For ASSESSMENT, this reveals the quality categories you'd let users filter on.
- **The sorted country list** is there to catch inconsistent spellings. If the same country appears as both "USA" and "United States," or with different capitalization, a user filtering for one would silently miss the other. Sorting puts near-duplicates next to each other, so they're easy to spot.
- **The last block** shows the data types of all the individuals at or below 0 BP. If they're overwhelmingly one present-day data type, that supports "date above 0 = ancient." If a meaningful number are ancient-looking data types, then 0 is also being used for unknown dates, and the filter needs a different approach.

Run it:

```bash
python scripts/profile_anno.py
```

The output will be long, mostly because of the country list. Paste it all in, and we'll go through it together.

- **What I asked next (verbatim):** (pasted the output of the script)
- **Exact output (verbatim):** 

- **Country:** only 10 missing, with AADR's labels matched exactly and a "list available values" helper for users.
- **Assessment:** nine categories with inconsistent capitalization, and the `PROVISIONAL_`/`MERGE_` prefixes need a source before you design around them.

The new information is in columns 14 and 21.

## Group ID (column 14)

- **3,897 distinct groups, no missing values.** That's far too many for anyone to scroll through, so a "list available values" helper matters even more here than for countries.
- **The labels follow a naming pattern**, roughly *place_period_culture*. For example, `Czechia_EBA_Unetice` is Czechia, Early Bronze Age, Unetice culture, and `Poland_IA` is Poland in the Iron Age. `Sweden_Viking` and `Belgium_HighMedieval` follow the same idea. The AADR paper cites a 2018 article by Eisenmann and colleagues about this naming system, which is worth reading before you rely on the abbreviations. I'm not certain what every short code means (for example, the `C` in `Spain_C`), so check the source rather than guessing.
- **`TSI`, `GWD`, and `CHS` are different.** These are 1000 Genomes Project codes for **present-day populations**: Tuscans in Italy, Gambians, and Southern Han Chinese. So present-day individuals clearly are in this file, with their own style of label.

**What this means for the filter:** exact matching works when a user knows the precise group name. But a researcher will often want *every* Iron Age group, or every group containing "Viking." That's a pattern search, which is a regular expression (Week 4 material, so another genuine course tie). The catch is that patterns can over-match: searching for `_C` would also catch any group with "_C" anywhere in its name. So pattern matching needs careful anchoring, and your tests should include a case that checks for over-matching.

This column also matters for later: Group ID is most likely the same population label used in the `.ind` file, which is how the filter results connect to `convertf`.

## Data type (column 21)

This is the messiest column so far, which makes it a good real-world example for your report:

- **Case inconsistency:** `1240k` appears 11,079 times and `1240K` 43 times. They're the same thing written two ways, the classic problem case-insensitive matching solves.
- **Multiple values in one cell:** entries like `1240k,Twist1.4M` and `1240k,Shotgun` combine data types with commas. A filter would have to split them apart first.
- **A note instead of a category:** "Shotgun pulled down only on 1240k autosomal targets - need to make a whole genome bam" (86 rows) is a processing note, not a data type.

Your problem statement doesn't promise a data-type filter, and I'd keep it that way. Coverage (column 26) already handles the "is there enough data?" question more directly. Record the messiness in your notes, and treat a data-type filter as out of scope, the same way you handled the JSON idea.

## The 0 BP question: stronger evidence, still not confirmed

Two findings now point the same way:

- **Almost all Shotgun.diploid rows are at 0 BP.** Of the 3,800 Shotgun.diploid rows in the whole file, 3,726 are dated at 0 BP.
- **Present-day population labels** like `TSI`, `GWD`, and `CHS` are among the most common groups.

That strongly suggests 0 BP means present-day. The one `1240k` row and the 240 plain `Shotgun` rows still need checking, though. So Column 12's Full Date text is the final check.

## Next: the Full Date check

Add this to the bottom of `profile_anno.py`:

```python
cols = [0, 10, 12, 14, 21]
short = ["genetic_id", "date_bp", "full_date", "group_id", "data_type"]
at_or_below_zero = anno.iloc[:, 10] <= 0

print("\n=== Full Date text for rows at or below 0 BP ===")
print(anno.loc[at_or_below_zero, anno.columns[12]].value_counts().head(10))

unusual = at_or_below_zero & ~anno.iloc[:, 21].isin(["Shotgun.diploid", "Shotgun"])
unusual = unusual | (anno.iloc[:, 10] < 0)
print("\n=== Unusual rows at or below 0 BP ===")
print(anno.loc[unusual].iloc[:, cols].set_axis(short, axis=1).to_string())
```

Here's what each part does:

- **The first block** lists the most common Full Date descriptions among the 0 BP rows. If they almost all say something like "present," that's strong evidence that 0 BP means present-day.
- **`~`** means NOT and **`isin([...])`** checks whether a value is in a list. So the `unusual` line picks rows that are at or below 0 BP and are **not** one of the two shotgun types.
- **`|`** means OR, so the next line also adds the −4 row.
- **`set_axis(short, axis=1)`** renames the columns for display only. It's a small preview of the short-name mapping `aadrkit` will need.
- **`to_string()`** prints every row instead of abbreviating the middle. There should only be about six rows here.

Keep all of these lines unindented, since none of them are inside a loop.

Run it and paste just the two new sections. Your prompt also shows `main ✗`, which means you have uncommitted changes, so commit the updated script once it runs correctly.
- **Verificaiton:** I developed the script, ran it, and visually inspected the results and interpreted them on my own, and added to my notes with the findings before continuing. 