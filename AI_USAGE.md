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
### Downloading the `.anno` file

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
### The real filename is different from what I gave you

Look at this part of the `wget` output, in the long redirect link:

```
filename*=UTF-8''v66.p1_1240K.aadr.PUB.anno
```

That's the file's actual name on Dataverse: **`v66.p1_1240K.aadr.PUB.anno`**. The name I gave you came from a secondary source (the ArcGIS visualizer page), not from Dataverse itself. Because `wget -O` saves under whatever name you tell it, the file got my name instead of the real one.

The **`p1`** matters. It most likely means "patch 1": a corrected re-release of v66 made after the original April release. Two things support that:

- **The file date.** `ls -lh` shows `Jun 8`. `wget` keeps the server's last-modified date, so the file was updated in June, about two months after v66.0 came out.
- **The line count.** You have 23,090 lines versus the reference's 23,250 rows. A patch release that corrected or removed some entries would explain that gap. The reference was a third-party example, not ground truth, so a small difference isn't alarming on its own.

For reproducibility and citation, you should record the version you actually have, which is v66.p1, not v66.0.

### Fixing it (one command at a time)

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

### You ran this outside your project environment

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

### What the columns tell us

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

### Step 2: Profile the numeric columns

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

### What to look for

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

### What the output shows

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

### Design decisions this suggests

These are worth writing into `docs/anno_notes.md` in your own words, since they'll shape the package code:

1. **Load the file with `na_values=[".."]`** in `pd.read_csv`. pandas then treats `".."` as missing from the start, and latitude and longitude load as real numbers instead of text.
2. **Don't assume dates are 0 or higher.** Negative BP values are valid.
3. **The date filter uses the mean date (column 10).** Column 11 holds each date's uncertainty, so a more precise "date range overlaps" filter is possible later. The simple version is the right place to start, as long as the documentation says which one it uses.
4. **The region filter should report what it drops.** If someone filters by a coordinate box, individuals without coordinates can't be included. Silently dropping 784 people is a transparency problem, so the tool should print something like "784 individuals have no coordinates and were excluded." The country column may still work for those individuals; we'll check it next.
5. **Coverage threshold is user-chosen,** with no hidden default.

### Two quick checks before moving on

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


### Profile the text columns

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

### Group ID (column 14)

- **3,897 distinct groups, no missing values.** That's far too many for anyone to scroll through, so a "list available values" helper matters even more here than for countries.
- **The labels follow a naming pattern**, roughly *place_period_culture*. For example, `Czechia_EBA_Unetice` is Czechia, Early Bronze Age, Unetice culture, and `Poland_IA` is Poland in the Iron Age. `Sweden_Viking` and `Belgium_HighMedieval` follow the same idea. The AADR paper cites a 2018 article by Eisenmann and colleagues about this naming system, which is worth reading before you rely on the abbreviations. I'm not certain what every short code means (for example, the `C` in `Spain_C`), so check the source rather than guessing.
- **`TSI`, `GWD`, and `CHS` are different.** These are 1000 Genomes Project codes for **present-day populations**: Tuscans in Italy, Gambians, and Southern Han Chinese. So present-day individuals clearly are in this file, with their own style of label.

**What this means for the filter:** exact matching works when a user knows the precise group name. But a researcher will often want *every* Iron Age group, or every group containing "Viking." That's a pattern search, which is a regular expression (Week 4 material, so another genuine course tie). The catch is that patterns can over-match: searching for `_C` would also catch any group with "_C" anywhere in its name. So pattern matching needs careful anchoring, and your tests should include a case that checks for over-matching.

This column also matters for later: Group ID is most likely the same population label used in the `.ind` file, which is how the filter results connect to `convertf`.

### Data type (column 21)

This is the messiest column so far, which makes it a good real-world example for your report:

- **Case inconsistency:** `1240k` appears 11,079 times and `1240K` 43 times. They're the same thing written two ways, the classic problem case-insensitive matching solves.
- **Multiple values in one cell:** entries like `1240k,Twist1.4M` and `1240k,Shotgun` combine data types with commas. A filter would have to split them apart first.
- **A note instead of a category:** "Shotgun pulled down only on 1240k autosomal targets - need to make a whole genome bam" (86 rows) is a processing note, not a data type.

Your problem statement doesn't promise a data-type filter, and I'd keep it that way. Coverage (column 26) already handles the "is there enough data?" question more directly. Record the messiness in your notes, and treat a data-type filter as out of scope, the same way you handled the JSON idea.

### The 0 BP question: stronger evidence, still not confirmed

Two findings now point the same way:

- **Almost all Shotgun.diploid rows are at 0 BP.** Of the 3,800 Shotgun.diploid rows in the whole file, 3,726 are dated at 0 BP.
- **Present-day population labels** like `TSI`, `GWD`, and `CHS` are among the most common groups.

That strongly suggests 0 BP means present-day. The one `1240k` row and the 240 plain `Shotgun` rows still need checking, though. So Column 12's Full Date text is the final check.

### Next: the Full Date check

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


## Entry 4
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Choosing test individuals so I could verify the tool against expected output especially with the tricky cases I discovered during profiling the `.anno` data. 
- **What I asked (verbatim):** Can you help me write a script to choose test individuals to verify against the tool's output that covers the tricky cases I found during the profiling: 1. present-day (0 BP), 2. reference genome (like `Chimp.REF`), 3. the one post-1950 individual (-4 BP), 4. someone with missing coordinates, 5. someone with low coverage, 6. someone from a place AADR lists separately (Canary Islands), 7. Someone whose group matches a pattern like "Viking, 8. a person with several rows. First check duplicates and publications to see how often one person appears in several rows before choosing test. Next, choose individuals. Finally, verify each one by hand with `grep` and record expected  values. 
- **Exact output (verbatim):**

### Step 3 has three parts

- **A.** Check duplicates and publications (finishing Step 2). You need to know how often one person appears in several rows before you can choose test individuals.
- **B.** Choose the individuals, using everything learned so far.
- **C.** Verify each one by hand with `grep`, and record the expected values.

### Part A: Duplicates and publications

Create a new file, `scripts/profile_ids.py`. It gets its own file because `profile_anno.py` is already long, and keeping each script focused on one question makes your exploration easier to follow later.

```python
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

# --- Duplicates: can one person have several rows? ---
genetic_id = anno.iloc[:, 0]
individual_id = anno.iloc[:, 2]
print("Rows:", len(anno))
print("Unique Genetic IDs:", genetic_id.nunique())
print("Unique Individual IDs:", individual_id.nunique())

rows_per_person = individual_id.value_counts()
print("\nNumber of people with 1, 2, 3... rows:")
print(rows_per_person.value_counts().sort_index())

example = rows_per_person.index[0]
print("\nThe person with the most rows:")
print(anno.loc[individual_id == example].iloc[:, [0, 2, 14, 21, 26]].to_string())

# --- Publications: what the citation export would draw on ---
first_pub = anno.iloc[:, 5]
pub = anno.iloc[:, 6]
doi = anno.iloc[:, 7]
print("\nMissing first publication:", first_pub.isna().sum())
print("Missing publication:", pub.isna().sum())
print("Missing DOI:", doi.isna().sum())
both_present = first_pub.notna() & pub.notna()
print("Rows where first publication differs:", ((first_pub != pub) & both_present).sum())
print("Unique publications:", pub.nunique())
```

### Line-by-line explanation

**Loading**
- **`na_values=[".."]`** is new. It's the first design decision from your notes, put into practice. pandas now treats `".."` as missing from the start, so `isna()` counts it automatically, without the separate `== ".."` check we used before.

**Duplicates**
- **`genetic_id` and `individual_id`** hold columns 0 and 2. Column 0 is the ID for one *dataset*, meaning one set of genotype data. Column 2 appears to be the ID for the *person*. If one person was sequenced more than once, for example with both capture and shotgun methods, they'd have one Individual ID but several Genetic IDs.
- **Comparing the unique counts** tells you whether that happens:
  - If unique Genetic IDs equals the number of rows, every row is a separate dataset.
  - If unique Individual IDs is *smaller* than the number of rows, some people appear more than once.
- **`rows_per_person.value_counts().sort_index()`** is a count of counts. The first `value_counts()` gives each person's number of rows. The second counts how many people have 1 row, how many have 2, and so on. `sort_index()` puts that list in order (1, 2, 3...).
- **`example`** is the person with the most rows, since `value_counts()` sorts from most to fewest. Printing their rows with the ID, group, data type, and SNP columns (0, 2, 14, 21, 26) shows what a multi-row person actually looks like. For example, do the rows differ only in data type and coverage?

**Publications**
- **The three `isna()` counts** show how complete each publication column is. Any gaps would affect the citation export.
- **`both_present`** handles a pandas quirk: a missing value is never considered equal to anything, not even another missing value. Without this check, every row with a missing publication would be counted as "different." `&` requires both columns to have a value before we compare them.
- **"Rows where first publication differs"** tells you whether the citation export needs both columns. If this is 0, one column is enough. If it's large, the export should probably list both papers for each individual.
- **`pub.nunique()`** counts how many distinct papers the data comes from. That tells you how long a citation list could get.

### Run it

```bash
python scripts/profile_ids.py
```

Paste the full output. From it, we'll decide how `aadrkit` should handle people with several rows and which publication columns the citation export needs. Then we'll move on to Part B, choosing your test individuals.
- **Verificaiton:** I typed out the script, analyzed the results myself after running it in the terminal, and then pasted back the output in Claude for a second verification. 
- **What I asked next (verbatim):** (pasted exact output of `profile_ids.py`) 
- **Exact output (verbatim):** 
The duplicates and publication checks were both worth doing. Each one changes the design.

### Duplicates: one person can have many rows

**Genetic ID is unique for every row** (23,089 IDs for 23,089 rows). That makes it the reliable key for identifying a specific dataset, and it's the ID `convertf` will use.

**Individual ID is not unique.** There are only 21,433 different people, so about 1,650 rows are repeat appearances. Most people (20,171) have one row, 936 have two, and one person, `YCH017`, has eleven.

`YCH017`'s rows show why. They're all the same individual from Late Classic Mexico, but they come from different datasets: `.AG` is 1240K capture and `.IM` is immune capture, plus several `_alt` and `_d` versions. I don't know exactly what `_alt` and `_d` mean, so that's another one to look up rather than guess. Their data quality varies hugely, from 7,796 SNPs up to 1,064,203 for `YCH017.AG`.

**Why this matters:** most analyses need each person counted once. If someone appears twice in a subset, population statistics treat them as two separate people. A kinship analysis would see two "individuals" with identical DNA, which looks like identical twins. So `aadrkit` needs a **deduplication option: keep one row per person, choosing the row with the most SNPs (column 26)**. `aadr-subset` describes doing something similar, so this is also a natural point to compare the two tools later.

Two decisions for you:

1. **Should deduplication be on by default?** I'd suggest yes. Counting a person twice is a silent error most users won't notice, while turning deduplication off is a deliberate choice a researcher can make. This differs from the coverage threshold, where there's no single right default. Here, one answer is usually correct.
2. **Filter first, then deduplicate.** Pick the best row among the rows that passed the user's filters. If you deduplicated first, you might keep a row that the filters then remove, and that person would disappear from the results entirely.

`YCH017` makes a perfect test individual: after deduplication, only `YCH017.AG` should remain.

### Publications: what the citation export can rely on

- **Every row has a publication label.** No missing values in columns 5 or 6.
- **647 rows have no DOI.** For those, the export can only give the label, and it should say so.
- **2,781 rows (about 12%) have a different "first publication."** So the export should list **both** columns, the paper that first reported the individual and the paper for this version of the data.
- **Some labels aren't published papers.** `Unpublished` and `FernandesMegalithic_Unpublished` are placeholders. Several others are preprints (`BioRxiv`, `ResSq`), which haven't completed peer review. The export should flag these rather than presenting them as ordinary citations.
- **The labels are inconsistent**, so they're names, not structured citations. The same journal appears as both `NatComm` and `NatCommun`, both `SciAdv` and `ScienceAdvances`, and `MolBiolEvol` and `MolBioEvol`. One label (`StolarekFiglerowiczGenomeBiol`) has no year. So the **DOI should be the main identifier** in the export, with the label as a fallback.
- **Many names contain non-English characters**: `Altınışık`, `Szécsényi-Nagy`, `Pääbo`, `Žegarac`. When `aadrkit` writes a citation file, it must use UTF-8 encoding explicitly. Otherwise, these names can be garbled on Windows, which uses a different default encoding. Since you work on Windows, you'd likely notice that bug.

### Part B: Find your test-individual candidates

Now we choose the 8–10 individuals. We already know several from earlier output:

| Situation | Genetic ID | Why it's useful |
|---|---|---|
| Reference genome | `Chimp.REF` | Must be excluded from present-day and ancient selections by default |
| Post-1950 date | `Khwit.SG` | The only negative date (−4 BP) |
| Present-day, unusual data type | `JHF05.AG` | Present-day, but captured with an "ancient" method |
| Person with many rows | `YCH017` | Deduplication must keep only `YCH017.AG` |

We still need candidates for: missing coordinates, very low coverage, the Canary Islands, a Viking group, a standard present-day individual, an "Unpublished" row, and a row with a missing DOI.

**Finding versus verifying:** using pandas to *find* candidates is fine. The independence rule applies to *verifying* their values, which you'll do in Part C with `grep`. Pandas helps you shop; `grep` checks the receipt.

Create `scripts/find_candidates.py`:

```python
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

cols = [0, 2, 10, 14, 16, 17, 26]
short = ["genetic_id", "individual_id", "date_bp", "group_id", "country", "lat", "snps_1240k"]
view = anno.iloc[:, cols].set_axis(short, axis=1)

def show(label, rows):
    print(f"\n=== {label} ===")
    print(rows.head(3).to_string())

show("Missing coordinates", view[view["lat"].isna()])
show("Lowest coverage", view.nsmallest(3, "snps_1240k"))
show("Canary Islands", view[view["country"] == "Canary Islands"])
show("Viking groups", view[view["group_id"].str.contains("Viking")])
show("Present-day Tuscans (TSI)", view[view["group_id"] == "TSI"])
show("Unpublished", view[anno.iloc[:, 6] == "Unpublished"])
show("Missing DOI", view[anno.iloc[:, 7].isna()])
```

### Explanation

**`view`** is a smaller version of the table with just seven columns, renamed to short names using `set_axis`, the same trick as before. From here on, you can write `view["country"]` instead of a column number or a very long name. This is very close to what the real package will do internally.

**`def show(label, rows):`** defines a **function**: a reusable block of code with a name.
- `label` and `rows` are its inputs.
- The two indented lines are what it does: print a heading, then print the first three matching rows.
- Without the function, you'd repeat those same two lines seven times. If you later wanted five rows instead of three, you'd change one line instead of seven. Functions are also exactly how `aadrkit` will be built: every filter will be a function like this.

**Each `show(...)` line** asks one question:
- **`view["lat"].isna()`** finds rows with no latitude. This works directly now because `na_values=[".."]` turned `".."` into a real missing value.
- **`view.nsmallest(3, "snps_1240k")`** returns the three rows with the fewest SNPs. This is how you find the 281-SNP individual.
- **`== "Canary Islands"`** and **`== "TSI"`** are exact matches.
- **`.str.contains("Viking")`** finds any group name *containing* "Viking" anywhere. This is the simple version of the pattern matching we discussed for the population filter.
- **The last two** use `anno.iloc[:, 6]` and `anno.iloc[:, 7]` (the publication and DOI columns). They aren't in `view`, but they're still in the same row order, so the matching works.

**`head(3)`** inside `show` limits each section to three rows, so you get a short list of candidates, not hundreds of rows.

Run it with `(aadr-project)` active:

```bash
python scripts/find_candidates.py
```

Paste the output. Then we'll pick one individual from each section and put together your final list of test individuals.
- **What I asked next (verbatim):** Pasted the output of `find_test_indiv.py`. "I want to use the following individuals "Chimp.REF" (ref genome), "Khwit.SG" (post-1950 date), "JHF05.AG" (present day individual with "ancient" data method), "NA20813.DG" (standard present-day individual), "YCH017.AG" (person with 11 rows), "I8508.AG" (missing coordinate but has a country Uzbekistan), "I13976.SG" (lowest coverage), "gun005.SG" (for the Canary Island that should not appear as Spain), "VK202.AG" (for both no DOI and the outlier test). I want to test finding these against pandas with regex using the grep function so they are verifiable to be accurate pulls."
- **Exact output (verbatim):**
Every section turned up a good candidate, and a couple of them revealed something new. First the new finding, then your final list, then Part C.

## A new finding: the `-o` suffix

Look at these group names:

- `Scotland_Viking-o` (VK201)
- `Altaian-o` (Altais1)
- `Russia_Karasuk-oAegean` (RISE492)

In AADR's naming, a `-o` suffix generally marks an **outlier**: an individual whose genetics don't match the rest of their labeled group. Confirm that in the AADR documentation or the naming-convention paper before relying on it. Sometimes extra text follows it, like `-oAegean`.

This matters a lot for the population filter:

- An **exact match** for `Scotland_Viking` returns VK202 but **not** VK201.
- A **"contains"** search for `Scotland_Viking` returns **both**.

Whether outliers belong in a researcher's analysis is their scientific decision, not the tool's. So `aadrkit` should make the behavior explicit and document it clearly. VK201 and VK202 together make an ideal pair of tests: they share a group name except for the suffix, so they show exactly how each matching mode behaves.

A smaller observation: the Tuscan present-day individuals all have latitude `40.00001`. That looks like an approximate location for the population, not an exact sampling site, so don't build tests that depend on precise coordinates for present-day individuals.

## Part B: Your test individuals

| # | Genetic ID | What it tests |
|---|---|---|
| 1 | `Chimp.REF` | Reference genome: excluded by default. Also "Unpublished," with no country or coordinates |
| 2 | `Khwit.SG` | The only post-1950 date (−4 BP, 1954 CE) |
| 3 | `JHF05.AG` | Present-day individual with an "ancient-style" data type (1240k) |
| 4 | `NA20813.DG` | Standard present-day individual (TSI, Italy) |
| 5 | `YCH017.AG` | Person with 11 rows: deduplication must keep this one |
| 6 | `I8508.AG` | Missing coordinates, but has a country (Uzbekistan) |
| 7 | `I13976.SG` | Lowest coverage in the file (281 SNPs) |
| 8 | `gun005.SG` | Canary Islands: must **not** appear when filtering for Spain |
| 9 | `VK202.AG` | `Scotland_Viking`; also has no DOI |
| 10 | `VK201.AG` | `Scotland_Viking-o`: the outlier test |

Ten individuals cover every edge case we found. Several cover two at once (VK202 is both a Viking and a missing-DOI case), which keeps the list short.

### Part C: Verify each one by hand

### Why use a different tool

So far, everything we know about these individuals came from pandas. If pandas had misread the file, for example by shifting a column, every check would agree with the same wrong answer. `grep` reads the raw text file directly, with no pandas involved. If the two tools agree, you can trust the values.

### Column numbers shift by one

pandas counts columns starting from **0**, but `cut` (the tool that picks out columns in the terminal) starts from **1**. So pandas column 0 is `cut` field 1, column 10 is field 11, and so on. Off-by-one mistakes like this are one of the most common bugs in data work, so it's worth seeing it once on purpose:

| Value | pandas column | `cut` field |
|---|---|---|
| Genetic ID | 0 | 1 |
| Individual ID | 2 | 3 |
| Date (BP) | 10 | 11 |
| Group ID | 14 | 15 |
| Country | 16 | 17 |
| Latitude | 17 | 18 |
| SNPs hit (1240k) | 26 | 27 |
| Publication | 6 | 7 |
| DOI | 7 | 8 |

### First individual: `Chimp.REF`

Run this from the repo root:

```bash
grep -P "^Chimp\.REF\t" data/raw/v66.p1_1240K.aadr.PUB.anno | cut -f1,3,11,15,17,18,27,7,8
```

Piece by piece:

- **`grep`** searches a file and prints every line that matches a pattern.
- **`-P`** tells grep to use the same regular-expression style as Python, so `\t` means a tab.
- **The pattern `"^Chimp\.REF\t"`** is built carefully, and it's a small example of the anchored matching we discussed:
  - **`^`** means "at the very start of the line." The Genetic ID is the first field, so this matches only rows whose ID *begins* this way.
  - **`\.`** matches a literal dot. In regular expressions, a plain `.` means "any character," so without the backslash the pattern could also match something like `ChimpXREF`.
  - **`\t`** at the end requires a tab right after the ID. Without it, searching for `VK20` would match both `VK201` and `VK202`. The tab guarantees you match the whole ID and nothing longer.
- **`|`** is a **pipe**. It sends grep's output straight into the next command instead of printing it.
- **`cut -f1,3,...`** keeps only the listed fields. Tabs separate the columns, which is `cut`'s default. Note that `cut` always prints fields in their original order, no matter what order you list them in.

Compare the output to the pandas results above. The ID, date, group, and coverage should match exactly.

### Second individual: `YCH017`, the multi-row person

Here you're checking a *count*, not a single row: does this person really have 11 rows, and is `YCH017.AG` the one with the most SNPs?

```bash
awk -F'\t' '$3 == "YCH017"' data/raw/v66.p1_1240K.aadr.PUB.anno | cut -f1,27
```

- **`awk`** is another text-processing tool. Unlike grep, it understands columns.
- **`-F'\t'`** tells awk the columns are separated by tabs.
- **`'$3 == "YCH017"'`** keeps lines where field 3 (Individual ID) is exactly `YCH017`. Because it's an exact comparison on one specific column, it can't accidentally match `YCH0170` or a group name that contains the same letters.
- **`cut -f1,27`** shows just the Genetic ID and SNP count.

You should see 11 lines, with `YCH017.AG` having the highest number (1,064,203).

To count the lines instead of reading them, add `| wc -l` to the end of the command. That pipes the output into the same line counter you used on the whole file earlier.

### The other eight

Use the `grep` command from `Chimp.REF` for each remaining individual, changing only the ID. Remember to put `\.` before each dot, and keep the `^` and `\t`:

- `Khwit\.SG`
- `JHF05\.AG`
- `NA20813\.DG`
- `I8508\.AG`
- `I13976\.SG`
- `gun005\.SG`
- `VK202\.AG`
- `VK201\.AG`

Paste all ten outputs, plus the `YCH017` result. Once we've confirmed they match the pandas values, we'll save them as your official expected-values file for the tests.
- **Verification:** I ran all the grep regex commands on the individuals that I had chosen per Claude's instructions, saved the outputs and made notes on them for my future script, and copied them into the Claude discussion. I also independently verified that the "-o" was indeed the updated version of the "_o" that stands for outliers via https://genarchivist.net/showthread.php?tid=2500 and the AADR paper (Mallick et al., 2024) itself. 
-**What I asked next (verbatim):** (pasted the output from the regex searches from my terminal) + "All 10 searches were successful, but now I am confused on how to handle the "-o" outlier. I looked up the documentation of the AADR outlier and this was what I found. "The group name may include a suffix that mark individuals such as potentially contaminated (“_contam”), or as a population genetic outlier (“_o”), or as having relatively little data (low coverage – “lc”)" from https://pure.mpg.de/rest/items/item_3570895_1/component/file_3570896/content as well as "Group ID naming convention changed entirely. v62 appended data type
  suffixes to group names (e.g. ACB.DG, Adygei.DG), v66 dropped them
  (just ACB, Adygei). Also various _o -> -o and other normalization
  changes, making direct group name comparison unreliable." from a forum on AADR v66 https://genarchivist.net/showthread.php?tid=2500. So it is confirmed they are outliers. How can the selection filter handle the outliers, possible contaminated sequences, and possible low coverage from the suffixes the paper listed? Also, would you be able to provide me a command to save all of these test subjects and their outputs to my repo?"
  - **Exact output (verbatim):**  
  All ten match the pandas output exactly, and your outlier research did more than confirm the guess.

### Verification: all ten match

| Genetic ID | Date | Group | Country | Lat | SNPs | Matches pandas? |
|---|---|---|---|---|---|---|
| `Chimp.REF` | 0 | Chimp | missing | missing | 1,102,442 | ✓ |
| `Khwit.SG` | −4 | Georgia_Tkhina_20thCentury | Georgia | missing | 1,113,084 | ✓ |
| `JHF05.AG` | 0 | Malaysia_Jehai | Malaysia | 4.5921 | 1,150,339 | ✓ |
| `NA20813.DG` | 0 | TSI | Italy | 40.00001 | 1,101,664 | ✓ |
| `YCH017` | — | — | — | — | 11 rows, `.AG` highest (1,064,203) | ✓ |
| `I8508.AG` | 6356 | Uzbekistan_N | Uzbekistan | missing | 16,278 | ✓ |
| `I13976.SG` | 18500 | Tanzania_LSA | Tanzania | −7.59 | 281 | ✓ |
| `gun005.SG` | 992 | Canary_Guanche | Canary Islands | 27.966667 | 379,128 | ✓ |
| `VK202.AG` | 1000 | Scotland_Viking | United Kingdom | 59.1341 | 810,231 | ✓ |
| `VK201.AG` | 1460 | Scotland_Viking-o | United Kingdom | 59.1341 | 666,641 | ✓ |

Two independent tools agree, so you can trust these values.

A few details to know:

- **`Malaysia4.5921` isn't a missing tab.** The terminal lines columns up at fixed tab positions, and a long value like "Malaysia" can run right into the next column visually. The tab is still there in the file. Similarly, `cu` / `t` splitting across lines is just your terminal wrapping a long command.
- **`Khwit.SG` also has missing coordinates.** That's new information, since our earlier pandas view of it didn't include latitude. It now covers two edge cases at once.
- **`gun005.SG` printed `Rodríguez` correctly**, which confirms the file's special characters read cleanly in your terminal.
- **VK201 and VK202 both have no DOI** for `AkbariReichNature2026`. My guess is the paper is recent enough that the DOI hadn't been added to the metadata yet, but that's only a guess. Either way, it's a realistic case for the citation export to handle.

### Your outlier research

This is a strong piece of verification, and it found something important: **the documentation and the data disagree.**

- **The paper** describes outlier suffixes written with an underscore (`_o`), plus `_contam` for possibly contaminated individuals and `lc` for low coverage.
- **The v66 data** writes it with a hyphen (`Scotland_Viking-o`, `Altaian-o`).
- **The forum post** explains why: v66 changed `_o` to `-o`, dropped data-type suffixes from group names, and normalized other naming. Group names can't be reliably compared across versions.

Notice how you established this. The forum is a community source, not peer-reviewed, so on its own it would be weak evidence. But its claim matches what you directly observed in the data, and the paper explains what the suffix *means*. Three sources agreeing is much stronger than any one alone. Describe that reasoning explicitly in your report's methods.

It also reinforces two earlier decisions:

- **Pinning v66.p1 was necessary.** A filter written against the paper's `_o` convention would silently miss every v66 outlier.
- **The suffix rules belong in one clearly documented place in the code**, tied to the pinned version, so a future AADR release with different conventions is easy to handle.

**A design decision this raises:** with `-o`, `_contam`, and `lc` all in play, the population filter could offer explicit options like "include outliers" or "include possibly contaminated individuals," rather than leaving it to whichever matching mode the user picks. Before deciding, it's worth counting how many groups actually use each suffix in v66, since the paper's conventions may not all have survived the renaming. That's a quick check for after this step.

### Save the ground truth file

Now we record these values as the expected answers your tests will check against. Since they come straight from `grep`, they stay independent of pandas.

**1. Create a `tests` folder:**

```bash
mkdir -p tests
```

`pytest` looks for tests in a folder named `tests` by convention, so the expected values will sit right next to the tests that use them.

**2. Write the header row:**

```bash
printf 'genetic_id\tindividual_id\tpublication\tdoi\tdate_bp\tgroup_id\tcountry\tlat\tsnps_1240k\n' > tests/ground_truth.tsv
```

- **`printf`** prints text exactly as written, with `\t` becoming a tab and `\n` a line break.
- **The header uses your short column names, in the order `cut` prints the fields** (1, 3, 7, 8, 11, 15, 17, 18, 27). As we noticed, `cut` always outputs fields in their original file order, so the header has to follow that order.
- **`>` works here** because the file doesn't exist yet, so `noclobber` doesn't block it.

**3. Add all ten individuals with one loop.** This is a single command, so paste it as one line:

```bash
for id in 'Chimp\.REF' 'Khwit\.SG' 'JHF05\.AG' 'NA20813\.DG' 'YCH017\.AG' 'I8508\.AG' 'I13976\.SG' 'gun005\.SG' 'VK202\.AG' 'VK201\.AG'; do grep -P "^${id}\t" data/raw/v66.p1_1240K.aadr.PUB.anno | cut -f1,3,7,8,11,15,17,18,27 >> tests/ground_truth.tsv; done
```

- **`for id in ...; do ...; done`** is a bash loop. It runs the same `grep | cut` command once for each ID in the list, setting `id` to each value in turn. It's the terminal version of the Python `for` loops you've been writing.
- **`${id}`** inserts the current ID into the pattern, so each pass searches `^Chimp\.REF\t`, then `^Khwit\.SG\t`, and so on.
- **The single quotes** around each ID keep the `\.` backslashes intact.
- **`>>`** appends each result to the end of the file instead of replacing it, and `noclobber` allows appending.
- **`YCH017.AG`** is the only `YCH017` row saved, because it's the row deduplication should keep. The fact that `YCH017` has 11 rows in total belongs in your notes.

**4. Check the result:**

```bash
cat tests/ground_truth.tsv
```

```bash
wc -l tests/ground_truth.tsv
```

You should see the header plus ten rows, so `wc -l` should report **11**. Missing values will still appear as `..`, which is correct: it's the raw truth from the file. The tests will treat `..` as missing, exactly the way the loader does.

A note on your redistribution promise: ten rows with nine fields each is a tiny test fixture, not a copy of the dataset. Your commitment not to redistribute AADR still holds. These values come from AADR v66.p1.

**5. Commit:**

```bash
git add tests/ground_truth.tsv AI_USAGE.md docs/anno_notes.md
```

```bash
git commit -m "Add hand-verified ground truth individuals for tests"
```

Paste the `cat` output so we can confirm the file looks right. Then we'll do the quick suffix count, and after that we'll move on.
- **What I asked next:** (pasted the cat result of `ground_truth.tsv` and the line count.) "All 11 lines (including header) had 9 fields so it populated correctly. Can you write me a script to count the different suffixes?"
- **Exact output (verbatim):** 
The file looks right: a header plus ten rows, and `wc -l` reports 11. The values for `YCH017.AG` also show up in full for the first time (1075 BP, `Mexico_LateClassic`, Mexico), which fills in its row.

Commit:

```bash
git add tests/ground_truth.tsv AI_USAGE.md docs/anno_notes.md
```

```bash
git commit -m "Add hand-verified ground truth individuals for tests"
```

### Quick check: which group-name suffixes actually exist in v66?

Your research found that the paper describes `_o`, `_contam`, and `lc`, while v66 uses `-o`. Before designing options around these suffixes, let's see which ones actually appear. Create `scripts/count_suffixes.py`:

```python
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
anno = pd.read_csv(ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno",
                   sep="\t", low_memory=False, na_values=[".."])

groups = pd.Series(anno.iloc[:, 14].unique())

for s in ["-o", "_o", "contam", "lc"]:
    hits = groups[groups.str.contains(s, regex=False)]
    print(f"\n=== '{s}': {len(hits)} groups ===")
    print(hits.head(10).to_string(index=False))
```

### Explanation

- **`anno.iloc[:, 14].unique()`** returns each group name once, all 3,897 of them. We're counting *groups*, not people, because suffixes are part of the group name.
- **`pd.Series(...)`** wraps the result back into a pandas Series. `.unique()` returns a plain array, which doesn't have pandas' text tools, and wrapping it gives us `.str.contains()` again.
- **`regex=False`** tells pandas to search for the text literally. Without it, pandas would treat the search text as a regular expression, where some characters have special meanings. Literal search keeps this check simple.
- **`len(hits)`** is how many groups contain that text, and **`head(10)`** shows up to ten examples.
- **`to_string(index=False)`** prints just the names, without row numbers.

### What to expect

This search is deliberately naive. It finds the text **anywhere** in a group name, not just as a suffix at the end. So read the examples, not just the counts:

- If **`lc`** shows names like `Chalcolithic` (the Copper Age, which contains "lc" in the middle), those aren't low-coverage markers. That's a false positive, and it shows exactly why the real filter needs precise rules instead of simple "contains" searches.
- If **`_o`** shows nothing or only unrelated matches, that supports the forum's point that v66 replaced `_o` with `-o`.
- **`-o`** should show the outlier groups we've already seen, like `Scotland_Viking-o`.

Run it:

```bash
python scripts/count_suffixes.py
```

Paste the output, and we'll work out exactly what the suffix rules should be. That's the last piece of the population-filter design.
- **Verification:** I manually inspected the results and logically thought about the output. I pasted the results into Claude mentioning why contamination was zero "Why would contam be zero? Could it be in a quality column? Also, it appears the "lc" picked up two names with lc but no lc suffixes. The final regex rule would include only outliers and the full base group?" for a final check and it responded with: 
- **Exact output (verbatim):**
This settles the suffix question cleanly. Only one suffix matters in v66, and the naive search turned up exactly the kind of false positive we expected.

### What each result means

**`-o`: 499 groups**, about 13% of all 3,897. That's a lot of outlier groups, so this definitely needs proper handling. The examples also show what comes *after* the `-o`:

- `England_BellBeaker-ohighEEF` and `England_BellBeaker-olowEEF`
- `Bulgaria_Samovodene_EarlyMedieval-oEastAsia`
- `England_EarlyMedieval_Saxon-o` (nothing after)

The text after `-o` describes **how** the individual differs from their group. EEF stands for Early European Farmer ancestry. So `-ohighEEF` means "an outlier with more farmer ancestry than the rest of the group," and `-oEastAsia` means "an outlier with East Asian-related ancestry." It's a useful detail for your report, because it shows these labels encode scientific findings, not just tags.

**`_o`: 0 groups.** This confirms the forum post: v66 replaced the underscore form with the hyphen. The paper's convention doesn't apply to this version.

**`contam`: 0 groups.** v66.p1 doesn't mark contamination in group names. Contamination appears to be tracked in the quality columns instead. Column 48's description talks about contamination estimates in detail, so the quality filter would cover it.

**`lc`: 2 groups, both false positives.**
- `Peru_Cullcunche_Tiwanaku` matches only because "Cul**lc**unche" contains those letters.
- `Ulchi` is a present-day population name.

Neither is a low-coverage marker. This is exactly the over-matching problem we predicted, and it's why the real filter needs a precise rule. Low coverage is already handled by the SNP-count column anyway.

### The suffix rule for `aadrkit`

Since `-o` is the only suffix that matters, the rule can be precise: **an outlier group is one whose name ends with `-o` followed by any text that doesn't contain an underscore.** As a regular expression:

```
-o[^_]*$
```

Piece by piece:

- **`-o`** matches the literal hyphen and "o".
- **`[^_]*`** means "any number of characters, as long as none is an underscore." The `^` inside square brackets means NOT. So it matches `highEEF`, `EastAsia`, or nothing at all, but it can't reach back into earlier parts of the name, which are separated by underscores.
- **`$`** means "at the very end of the name." Combined with the rest, this ensures `-o` is in the final section of the name, not somewhere in the middle.

The **base group** is then whatever comes before the `-o`. For example, `England_BellBeaker-ohighEEF` becomes `England_BellBeaker`. That gives the population filter a clean design:

- A user asks for `England_BellBeaker`.
- By default, the tool returns only that exact group, **excluding outliers**, and prints a message like "12 outlier individuals excluded; use `include_outliers` to keep them." It's the same transparency principle as the missing-coordinates message.
- With `include_outliers=True`, it also returns every group whose base name matches, such as `-ohighEEF` and `-olowEEF`.

Excluding by default makes sense here because it's also what exact matching naturally does, so the default isn't hiding anything. It just matches what the user typed. And outliers are included only when someone asks for them.

When you implement this, check the regular expression against this script's naive count. If both find 499 groups, the precise rule agrees with the simple search on this version. If they differ, look at the groups in the difference. Your test pair already covers it: VK201 (`Scotland_Viking-o`) must be recognized as an outlier, and VK202 (`Scotland_Viking`) must not.


```bash
git commit -m "Count group-name suffixes; define outlier rule for v66"
```

**That completes Steps 2 and 3.** You now know the metadata well enough to design every filter, and you have ten hand-verified individuals to test against.
