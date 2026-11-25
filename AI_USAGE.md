# AI USAGE LOG 
### Claude had access to my current proposal, project requirements, project rubric, my initial sources, accessions, data, project idea, project guidelines, and goals in initial  chat.
before answering. 
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

### A new finding: the `-o` suffix

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

### Part B: Your test individuals

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

## Entry 5
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Running a test on `convertf` 9.0.0 with a few test individuals to see if it reads the TGENO file correctly.
- **What I asked (verbatim):** "Can you write a parameter file for the `.ind` file that tests `convertf` on a present day Tuscan with about 1 million SNPs, a Viking with about 800,000 SNPs, and the lowest coverage individual in the file? The file will go in data/`test_convertf`. 
- **Exact output(verbatim):**
### Make the modified `.ind`

This creates a copy of the `.ind` where everyone except our three individuals is labeled `Ignore`:

```bash
awk '{ if ($1=="NA20813.DG" || $1=="VK202.AG" || $1=="I13976.SG") print $1, $2, $3; else print $1, $2, "Ignore" }' data/raw/v66.p1_1240K.aadr.patch.PUB.ind > data/test_convertf/test.ind
```

- **`if (...)`** checks whether column 1 is one of our three IDs.
- **If yes,** `print $1, $2, $3` writes the line unchanged: ID, sex, real population.
- **If no,** `print $1, $2, "Ignore"` writes the same ID and sex, but replaces the population with `Ignore`.
- **The commas** in `print` put a single space between columns. The leading padding disappears, which is fine: `convertf` only needs whitespace between columns.
- **`>`** saves the result as a new file. If you ever rerun this, use `>|` instead, since `noclobber` will refuse to overwrite the existing file.

**Why relabel instead of deleting lines?** The `.geno` file stores genotypes in the same order as the `.ind` lines. Line 1 of the `.ind` is the first person in the `.geno`, line 2 the second, and so on. If you deleted lines, every person after the gap would be matched to the wrong genotypes, with no error message. Relabeling keeps every line in place, so the order stays intact.

Check the result two ways:

```bash
grep -v "Ignore" data/test_convertf/test.ind
```

**`grep -v`** prints lines that *don't* match, so this should show exactly our three individuals.

```bash
wc -l data/test_convertf/test.ind
```

This must still say **23,089**. If it's any lower, a line was lost and the order is broken.

### Write the parameter file

Create `scripts/convertf_test.par` in VS Code. It belongs in `scripts/` and gets committed: it's a record of exactly how you ran the test, and it contains settings, not data.

```
genotypename:    data/raw/v66.p1_1240K.aadr.patch.PUB.geno
snpname:         data/raw/v66.p1_1240K.aadr.patch.PUB.snp
indivname:       data/test_convertf/test.ind
outputformat:    EIGENSTRAT
genotypeoutname: data/test_convertf/test_out.geno
snpoutname:      data/test_convertf/test_out.snp
indivoutname:    data/test_convertf/test_out.ind
hashcheck:       NO
```

Two details:

- **The output names end in `_out`.** If `indivoutname` were the same file as `indivname`, `convertf` would overwrite its own input while reading it. Ending each name with `.geno`, `.snp`, or `.ind` also means your `.gitignore` patterns cover them.
- **The paths are relative to the repo root**, so always run `convertf` from `project-hds`, not from inside `scripts/` or `tests/`.

### Run it and time it

From the repo root, with `(aadr-project)` showing:

```bash
time convertf -p scripts/convertf_test.par 2>&1 | tee data/test_convertf/convertf.log
```

- **`time`** measures how long the command takes. This is the speed test for whether keeping the data on `/mnt/c` is fast enough.
- **`2>&1`** sends error messages to the same place as regular output, so nothing gets lost.
- **`| tee data/test_convertf/convertf.log`** shows the output on screen *and* saves a copy to a log file. If something goes wrong, you'll have the full message to look at.

**What to expect:**

- **If TGENO isn't supported,** `convertf` should fail almost immediately with an error about the genotype file or its format.
- **If it works,** it will run for a while, since it has to read through the 6.7 GB file, then print a summary including how many individuals and SNPs it wrote out. We want to see **3 individuals**.

Paste the output, especially the last 20 or so lines and the `real` time that `time` prints at the end. That tells us whether it works as planned.
- **Verification:** I ran all commands, created the parameter file, and inspected the result. The TGENO file worked correctly in `real    1m18.590s`. Interpreting the results, I sae that the `records read: 3` (my 3 individuals), `before compress: ... 23089` (correct, the total number of individuals), `after compress: ... 3`, `numsnps output: 1233013` (kept all SNPs). I then inspected the `test_out.ind` file to confirm which individuals appeared "VK202.AG M Scotland_Viking, NA20813.DG F TSI, I13976.SG F Tanzania_LSA" (correct) and the `test_out.geno` file for 3 digits per line and 1,233,013 SNPs per person. Additionally I checked each person's genotype against the `.anno` file (). The numbers for 0's 1's and 2's (remembering that pseudohaploid means 0 1's for ancient individuals) matched up to the expected counts of 281, 810,231, and 1,101,664.

## Entry 6
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Creating the project package for `aadrkit`
- **What I asked (verbatim):** Can you help me creat an `__init__.py` file and a `pyproject.toml` file for `aadirkit`? And test it correctly?"
- **Exact output (verbatim):**

### Install pytest and pin its version

`pytest` is the testing tool. Install it into your environment:

```bash
mamba install -n aadr-project -c conda-forge pytest
```

Then see which version you got:

```bash
conda list pytest
```

Add it to `environment.yml` with that exact version, the same way you pinned EIGENSOFT, for example `- pytest=X.Y.Z`. "Install it, then pin what you actually got" means you never guess a version number, and your environment file always describes something you've tested.

### Create the package folder and its first file

```bash
mkdir -p src/aadrkit
```

Create `src/aadrkit/__init__.py` with:

```python
"""aadrkit: filter and export subsets of the Allen Ancient DNA Resource (AADR)."""

__version__ = "0.1.0"
```

- **`__init__.py`** is what tells Python "this folder is a package." Anything in it runs when someone writes `import aadrkit`.
- **The text in triple quotes** is a docstring, the package's built-in description. The documentation rubric looks for these.
- **`__version__`** gives the package a version number you can check from Python.

### Create `pyproject.toml` in the repo root

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "aadrkit"
version = "0.1.0"
description = "Filter and export subsets of the Allen Ancient DNA Resource (AADR)"
requires-python = ">=3.11"
dependencies = ["pandas"]

[tool.setuptools.packages.find]
where = ["src"]
```

- **`[build-system]`** tells pip which tool builds the package. Setuptools is the long-standing standard.
- **`[project]`** is the package's basic information. `dependencies` lists what it needs to run, so installing `aadrkit` would pull in pandas too.
- **The pandas dependency is deliberately unpinned here.** `pyproject.toml` describes what the package *needs*; `environment.yml` pins the exact versions *you tested with*. Keeping the two roles separate is standard practice.
- **`[tool.setuptools.packages.find]`** with `where = ["src"]` tells setuptools to look for packages inside `src/`.

### Install the package in editable mode

From the repo root, with `(aadr-project)` active:

```bash
pip install -e .
```

- **`.`** means "the package described in this folder," which setuptools finds through `pyproject.toml`.
- **`-e`** means **editable**. Instead of copying your code somewhere else, pip links to your `src/aadrkit` folder. When you edit the code, the change takes effect immediately, with no need to reinstall. That's what you want while developing.

Then add this to `environment.yml`, so anyone who builds the environment also gets the package installed:

```yaml
  - pip
  - pip:
      - -e .
```

These lines go at the end of the `dependencies` list, at the same indentation as the other entries. YAML is strict about indentation, like Python.

### 6e. Check that it imports

```bash
python -c "import aadrkit; print(aadrkit.__version__, aadrkit.__file__)"
```

**`python -c`** runs a single line of Python without creating a file. You should see `0.1.0` followed by a path ending in `src/aadrkit/__init__.py`. That path confirms Python is using your editable install.

### 6f. Write and run the first test

Create `tests/test_import.py`:

```python
import aadrkit


def test_package_imports():
    """The package installs and exposes a version number."""
    assert aadrkit.__version__ == "0.1.0"
```

- **pytest finds tests automatically** in files named `test_*.py` and in functions whose names start with `test_`.
- **`assert`** means "this must be true." If it isn't, the test fails and pytest shows you exactly what didn't match.

Run it from the repo root:

```bash
pytest
```

You should see `1 passed`. It's a deliberately trivial test. Its only job is to prove that the installing, importing, and testing pieces all connect, before any real code depends on them.

### 6g. Commit

```bash
git add pyproject.toml src/aadrkit/__init__.py tests/test_import.py environment.yml
```

```bash
git commit -m "Create aadrkit package skeleton with editable install and first test"
```

Paste the output. Your first real function can be: loading the `.anno` file with all the decisions from your notes built in, tested against your ground-truth individuals. 
- **Verificaiton:** I created a package for `aadrkit` with its own `src/` folder, `__init__.py`, a `pyproject.toml` in the repo root, installed it with `pip install -e .`, added the "pip, -pip: -e ." dependency to the `environment.yml` file, checked the import of `aadrkit` by running `python -c "import aadrkit; print(aadrkit.__version__, aadrkit.__file__)"`, installed `pytest`, and tested the `aadrkit` package set up by running `test_import.py`. All were successful. (Job of the test is to see if the installing, importing, and testing pieces connect).

## Entry 7: 
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Creating a loader script for the annotation file. 
- **What I asked (verbatim):** The first step of the `aadrkit` needs to be able to load the `.anno` file correctly. It needs to 1. Treat ".." as missing and only ".." and empty cells. 2. Give important columns short names. 3. Find those columns reliably despite long names. 4. Fail loudly if anything looks wrong rather than quietly loading the wrong column. 
For it to find each column: use a short pattern matching the start of the name because it is readable, tolerant of small changes, and can be checked for exactly one match. It will be matched against the beginning of the column name. Each patterns must match exactly one column. Error raised if matches one or more than one.
What to count as missing is ".." and blanks: pandas by default treats a whole list of strings as missing: "NA, N/A, null, None, etc." A real value could happen to be one of those and pandas would erase it silently.
I also need this implemented into the package to test it. 
- **Exact output (verbatim):**
- **A (now):** write the loader and tests that check its overall structure.
- **B (next):** test the loader's values against your hand-verified `ground_truth.tsv`.

### What the loader needs to do

Your notes become its requirements:

1. **Treat `".."` as missing**, and *only* `".."` and empty cells.
2. **Give the important columns short names**, like `date_bp` instead of a 150-character header.
3. **Find those columns reliably**, despite long names, a trailing space in one, a duplicate name, and two columns that both start with "ASSESSMENT."
4. **Fail loudly if anything looks wrong**, rather than quietly loading the wrong column.

### Decision 1: How to find each column

We'll use a **regular expression** for each column, matched against the beginning of the column name. The key safety rule is that **each pattern must match exactly one column**. If it matches none, or more than one, the loader raises an error and tells you which pattern failed. That turns the "silently reads the wrong column" problem into a clear error message.

That rule matters because of what you found. `ASSESSMENT` and `ASSESSMENT WARNINGS` both start with the same word, so the pattern for column 47 is `ASSESSMENT$`. The `$` means "end of name," which excludes the warnings column.

### Decision 2: Only `".."` and blanks count as missing

By default, pandas treats a whole list of strings as missing: `"NA"`, `"N/A"`, `"null"`, `"None"`, and more. In a dataset full of codes and names, a real value could happen to be one of those, and pandas would silently erase it. So the loader switches the defaults off (`keep_default_na=False`) and lists only AADR's own marker and empty cells.

### Write the loader

Create `src/aadrkit/anno.py`:

```python
"""Load the AADR annotation (.anno) file into a tidy pandas DataFrame.

Column patterns were written for AADR release v66.p1 (1240K panel).
"""
import re
from pathlib import Path

import pandas as pd

# Short name -> regular expression matching the start of the real column name.
# Each pattern must match exactly one column, or load_anno() raises an error.
COLUMN_PATTERNS = {
    "genetic_id": r"Genetic ID",
    "individual_id": r"Individual ID$",
    "first_publication": r"First publication",
    "publication": r"Publication abbreviation$",
    "doi": r"doi for publication",
    "date_bp": r"Date mean in BP",
    "full_date": r"Full Date",
    "group_id": r"Group ID$",
    "country": r"Political Entity$",
    "lat": r"Latitude$",
    "lon": r"Longitude$",
    "data_type": r"Data type$",
    "snps_1240k": r"SNPs hit on autosomal targets .*on 1240k snpset",
    "y_haplogroup": r"Y haplogroup\s+in ISOGG",
    "mt_haplogroup": r"mtDNA haplogroup",
    "assessment": r"ASSESSMENT$",
}

# AADR writes missing values as ".."; empty cells are also missing.
MISSING_VALUES = ["..", ""]


def find_columns(names):
    """Map each short name to exactly one real column name.

    Raises ValueError if any pattern matches zero or several columns.
    """
    found = {}
    for short, pattern in COLUMN_PATTERNS.items():
        matches = [name for name in names if re.match(pattern, name.strip())]
        if len(matches) != 1:
            raise ValueError(
                f"Expected 1 column matching {pattern!r} for '{short}', "
                f"found {len(matches)}: {matches}"
            )
        found[short] = matches[0]
    return found


def load_anno(path):
    """Read an AADR .anno file and return the key columns under short names.

    AADR's missing-value marker ".." and empty cells become NaN. pandas'
    other default missing-value strings (such as "NA") are deliberately
    not applied, so real values are never mistaken for missing ones.
    """
    raw = pd.read_csv(
        Path(path), sep="\t", encoding="utf-8", low_memory=False,
        keep_default_na=False, na_values=MISSING_VALUES,
    )
    columns = find_columns(raw.columns)
    anno = raw[list(columns.values())].copy()
    anno.columns = list(columns.keys())
    return anno
```

### How it works

**`COLUMN_PATTERNS`** is a dictionary: each short name points to its pattern. Putting the patterns in one place, at the top of the file, means that when a future AADR version renames a column, there's exactly one place to update. The docstring at the top states which version these patterns were written for.

**A few patterns handle specific problems you found:**
- **`r"..."`** is a "raw string": backslashes are passed to the regular expression untouched instead of being interpreted by Python first. It's the standard way to write regex in Python.
- **`Individual ID$`**, **`Group ID$`**, and the others ending in `$` must match the whole name.
- **`Y haplogroup\s+in ISOGG`**: the real column name has *two* spaces between "haplogroup" and "in." `\s+` means "one or more spaces," so the pattern doesn't depend on counting spaces exactly.
- **`SNPs hit on autosomal targets .*on 1240k snpset`**: `.*` means "any characters," so this reliably picks the 1240k version out of the five similar SNP-count columns.
- **`name.strip()`** removes the trailing space from column 25's name before matching, so it can't cause problems.

**`find_columns(names)`** checks every pattern against every column name:
- **`re.match(pattern, ...)`** only matches at the *start* of the name. That's why `Genetic ID` doesn't match column 1, "Persistent Genetic ID."
- **The list in square brackets** collects every column that matches. This is a list comprehension, a compact way to build a list with a loop.
- **`if len(matches) != 1: raise ValueError(...)`** is the safety rule. `raise` stops the program with an error, and the message names the pattern and lists what it found, so you know exactly what to fix.
- **`{pattern!r}`** inside the f-string prints the pattern with its quotes, which makes the error message clearer.

**`load_anno(path)`** is the function users will call:
- **`pd.read_csv(...)`** has the same settings you used in the scripts, plus `encoding="utf-8"` (for names like `Rodríguez`) and the two missing-value settings above.
- **`raw[list(columns.values())]`** keeps only the 16 matched columns. `.copy()` makes it an independent table, rather than a view that still points back into `raw`.
- **`anno.columns = list(columns.keys())`** swaps the long names for the short ones.

### Make `load_anno` available from the package

Update `src/aadrkit/__init__.py`:

```python
"""aadrkit: filter and export subsets of the Allen Ancient DNA Resource (AADR)."""

from aadrkit.anno import load_anno

__version__ = "0.1.0"
```

With that import, users can write `aadrkit.load_anno(...)` instead of having to know the function lives in the `anno` module. The module organization becomes an internal detail.

### Write the tests

Create `tests/test_anno.py`:

```python
from pathlib import Path

import pandas as pd
import pytest

from aadrkit.anno import COLUMN_PATTERNS, find_columns, load_anno

ROOT = Path(__file__).resolve().parent.parent
ANNO_PATH = ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno"


@pytest.fixture(scope="module")
def anno():
    """Load the real .anno file once for all tests in this file."""
    if not ANNO_PATH.exists():
        pytest.skip("AADR .anno file not found; see README 'Data' section")
    return load_anno(ANNO_PATH)


# --- Tests that need no data ---

def test_find_columns_rejects_two_matches():
    with pytest.raises(ValueError):
        find_columns(["Genetic ID (copy 1)", "Genetic ID (copy 2)"])


def test_find_columns_rejects_missing_column():
    with pytest.raises(ValueError):
        find_columns(["Something unrelated"])


# --- Tests on the real file ---

def test_shape(anno):
    assert anno.shape == (23089, len(COLUMN_PATTERNS))


def test_short_column_names(anno):
    assert list(anno.columns) == list(COLUMN_PATTERNS)


def test_genetic_id_is_unique(anno):
    assert anno["genetic_id"].is_unique


def test_missing_marker_becomes_nan(anno):
    assert pd.api.types.is_float_dtype(anno["lat"])
    assert anno["lat"].isna().sum() == 784
```

### How the tests work

**`@pytest.fixture`** marks `anno()` as a **fixture**: shared setup that tests can request. Any test with `anno` as an input automatically receives the loaded table.
- **`scope="module"`** means the file is loaded once and reused by every test in this file, instead of being reloaded for each test.
- **`pytest.skip(...)`**: if someone runs the tests without having downloaded the data, these tests are marked "skipped" with a message pointing to the README, instead of failing with a confusing "file not found" error. Your ground truth file is in the repo, but the AADR data isn't, so this keeps the test suite honest about what it can check.

**The first two tests need no data.** They feed `find_columns` made-up column names and check that it refuses them:
- **`with pytest.raises(ValueError):`** means "the code inside must raise a `ValueError`; if it doesn't, the test fails." Testing that bad input is *rejected* is just as important as testing that good input works. These two tests prove the safety rule actually works.

**The other four test the real file against numbers you measured:**
- **`test_shape`:** 23,089 rows and 16 columns.
- **`test_short_column_names`:** the columns come out in the right order with the right names.
- **`test_genetic_id_is_unique`:** confirms Genetic ID is a unique key, which the whole tool depends on.
- **`test_missing_marker_becomes_nan`:** latitude is now a real number column, not text, and exactly 784 values are missing. This proves `".."` handling works.

### Run the tests

From the repo root, with `(aadr-project)` active:

```bash
pytest -v
```

**`-v`** means "verbose": pytest lists every test by name with PASSED or FAILED, instead of just printing dots. You should see **7 passed**: the import test from Step 6, the two `find_columns` tests, and the four tests on the real file.

If anything fails, paste the full output. pytest's failure messages show exactly what was expected and what it got, and if a column pattern fails, the error message will name the pattern.

### Commit

```bash
git add src/aadrkit/anno.py src/aadrkit/__init__.py tests/test_anno.py
```

```bash
git commit -m "Add load_anno with pattern-based column matching and tests"
```

Paste the `pytest -v` output. Then in 7b, we'll test the loader's values against your ten hand-verified individuals, plus the "0 BP means present-day" assumption test from your notes.
- **Verificaiton:** I typed up the script and ran `pytest -v` but ran into an error (pasted below). I attempted to inspect the error myself but I did not understand what went wrong. I suspected it was something in the `anno.py` file but was not sure. 
- **What I asked next (verbatim):** "What does this error mean? Is it in the `anno.py file`?"
- **Exact output (verbatim):**
### How to read the failure

Look at what pytest printed for `anno` in each failed test:

```
[23089 rows x 1 columns]
```

The loader returned all 23,089 rows but only **one** column, `genetic_id`. All three failures follow from that:

- **`test_shape`** expected 16 columns and got 1.
- **`test_short_column_names`** found `genetic_id` and then nothing else.
- **`test_missing_marker_becomes_nan`** crashed because there's no `lat` column.

When several tests fail at once, look for the **one** thing they all have in common. Here, the problem isn't in the tests; it's in what `load_anno` gave them.

### The likely cause: `return found` is indented too far

`genetic_id` is the **first** entry in `COLUMN_PATTERNS`. Getting only the first one means the loop in `find_columns` stopped after its first pass. The usual reason is that `return found` ended up *inside* the loop:

```python
    for short, pattern in COLUMN_PATTERNS.items():
        matches = [...]
        if len(matches) != 1:
            raise ValueError(...)
        found[short] = matches[0]
        return found          # ← inside the loop: returns after the first column
```

`return` ends the function immediately. Inside the loop, it runs at the end of the very first pass, with just one column found. It's the same kind of silent bug as the indentation issue in `profile_anno.py`: perfectly valid Python, wrong behavior.

**The fix:** move `return found` four spaces left, so it lines up with `for` and runs only once the loop has finished:

```python
    for short, pattern in COLUMN_PATTERNS.items():
        matches = [name for name in names if re.match(pattern, name.strip())]
        if len(matches) != 1:
            raise ValueError(
                f"Expected 1 column matching {pattern!r} for '{short}', "
                f"found {len(matches)}: {matches}"
            )
        found[short] = matches[0]
    return found
```

If your `return found` is already at that level, paste your `find_columns` function and we'll find what else is cutting the loop short.

### Why the other tests passed anyway

Notice that `test_find_columns_rejects_two_matches` and `test_find_columns_rejects_missing_column` **passed** despite the bug. Both feed in fake names that fail on the *first* pattern, so the error is raised before the loop ever gets to the early `return`. They tested the safety rule correctly, but they never tested that the function keeps going through all 16 patterns.

That's a gap worth closing with a test that needs no data, so it would catch this even on a computer without AADR downloaded. Add this to `tests/test_anno.py`, under the other two "no data" tests:

```python
def test_find_columns_finds_every_pattern():
    """Every pattern is matched, not just the first one."""
    names = [
        "Genetic ID (suffixes...)", "Individual ID", "First publication: ...",
        "Publication abbreviation", "doi for publication ...", "Date mean in BP ...",
        "Full Date ...", "Group ID", "Political Entity", "Latitude", "Longitude",
        "Data type",
        "SNPs hit on autosomal targets (Computed using easystats on 1240k snpset)",
        "Y haplogroup  in ISOGG notation ...", "mtDNA haplogroup ...", "ASSESSMENT",
    ]
    assert len(find_columns(names)) == len(COLUMN_PATTERNS)
```

- **The `names` list** is a set of made-up column names, each shaped like the real one, including the double space in the Y haplogroup name.
- **The `assert`** checks that `find_columns` returns one entry for every pattern.

**Test it on purpose:** run `pytest -v` *before* fixing the indentation. This new test should fail too. Then fix the indentation and run it again. Seeing a test fail on the bug and pass on the fix is how you know the test actually checks what you think it does. A test that has never failed might not be testing anything.

### After the fix

```bash
pytest -v
```

You should now see **8 passed**: the 7 from before plus the new one.

The run took about 18 seconds, almost all of it loading the 13 MB file across `/mnt/c`. Because the fixture uses `scope="module"`, that load happens once, not once per test.

Then commit:

```bash
git add src/aadrkit/anno.py tests/test_anno.py
```

```bash
git commit -m "Fix early return in find_columns; test that every pattern is matched"
```

Paste the new `pytest -v` summary, and then we'll do comparing the loader against your ground-truth individuals.
- **Verification:** As Claude suggested, there was indeed that exact return indentation error in my `anno.py`. First I added that block that checks that every pattern is matched rather than just the first one and tested it - the test failed again. Then I fixed the indentation in the `anno.py` file and ran the test again - it failed. So I inspected it myself and found that there was a typo inside of my `COLUMN_PATTERNS`. `"publication": r"Publication abbreviations$"` was supposed to be `"publication": r"Publication abbreviation$"` - there was an additional "s" at the end of abbreviation that created an ERROR message. After I fixed this, the test ran and passed successfully. 

## Entry 8:
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Testing the loader against the ground individuals. 
- **What I asked (verbatim):** Can you create a script that tests the ground truth individuals? Do I need a second script? Or would I be able to move the `anno` fixture so it works in a seperate test? I would also like to test a failure case. 
- **Exact output (verbatim):**
### What this step proves

In the first part, the tests checked the loader's **structure**: the right number of columns, the right names, latitude as numbers. But a loader could pass all of those and still read the **wrong** column. For example, the SNP-count pattern could accidentally match the Human Origins SNP column instead of the 1240k one. The shape would be perfect and every value would be wrong.

The ground truth comparison closes that gap. Your ten individuals' values came from `grep` reading the raw file, completely independent of the loader. If the loader returns exactly those values, it's reading the right columns, handling missing values correctly, and keeping special characters intact.

Your ten individuals were chosen so that each loader decision gets checked at least once:

| Loader decision | Checked by |
|---|---|
| Picks the 1240k SNP column out of five similar ones | Every row's `snps_1240k` |
| `".."` becomes missing | `lat` for I8508, Khwit, and Chimp; `doi` for VK202, VK201, and Chimp |
| Negative dates kept as-is | Khwit (−4) |
| Special characters survive (UTF-8) | gun005's publication, `Rodríguez-Varela...` |
| Outlier suffix kept in the group name | VK201, `Scotland_Viking-o` |
| Approximate present-day coordinates | NA20813 (40.00001) |

We'll also add the **data assumption tests** from your notes: 0 BP means "present," and exactly four rows are reference genomes. Those test the *data*, not the code, and I'll explain the difference below.

### Share fixtures with `conftest.py`

Right now, the `anno` fixture lives inside `test_anno.py`. Your new tests will go in a second file that also needs it, and the filter tests later will too. Copying the fixture into every file would mean several copies to keep in sync.

pytest has a built-in answer: a file named **`conftest.py`** in the `tests/` folder. Any fixture defined there is automatically available to every test file, with no import needed.

Create `tests/conftest.py`:

```python
"""Shared pytest fixtures for the aadrkit test suite."""
from pathlib import Path

import pandas as pd
import pytest

from aadrkit.anno import load_anno

ROOT = Path(__file__).resolve().parent.parent
ANNO_PATH = ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno"
GROUND_TRUTH_PATH = ROOT / "tests" / "ground_truth.tsv"


@pytest.fixture(scope="session")
def anno():
    """The real AADR v66.p1 .anno file, loaded once for the whole test run."""
    if not ANNO_PATH.exists():
        pytest.skip("AADR .anno file not found; see README 'Data' section")
    return load_anno(ANNO_PATH)


@pytest.fixture(scope="session")
def ground_truth():
    """Ten individuals whose values were verified by hand with grep."""
    return pd.read_csv(
        GROUND_TRUTH_PATH, sep="\t", encoding="utf-8",
        keep_default_na=False, na_values=[".."],
    )
```

- **`scope="session"`** instead of `"module"`: the file is now loaded **once for the entire test run**, shared across all test files. With the 18-second load you saw, that keeps the test run from getting slower as you add files.
- **The `ground_truth` fixture reads your file with the same missing-value rules as the loader** (only `".."` counts as missing). That's deliberate: the comparison should test whether the loader reads the right *values*, not whether two different missing-value settings happen to agree.
- **The ground truth fixture has no skip.** `ground_truth.tsv` is committed to the repo, so it's always present.

### Update `test_anno.py`

Since the fixture now lives in `conftest.py`, remove these from the top of `test_anno.py`:

- the `from pathlib import Path` line
- the `ROOT = ...` and `ANNO_PATH = ...` lines
- the whole `@pytest.fixture` block and its `anno()` function

Keep `import pandas as pd`, `import pytest`, and the `from aadrkit.anno import ...` line. Every test using `anno` will still work, because pytest finds the fixture in `conftest.py` automatically.

Then add this test at the bottom:

```python
def test_matches_hand_verified_individuals(anno, ground_truth):
    """Loader values match the ten individuals verified by hand with grep."""
    ids = ground_truth["genetic_id"].tolist()
    columns = [c for c in ground_truth.columns if c != "genetic_id"]
    actual = anno.set_index("genetic_id").loc[ids, columns].reset_index()
    pd.testing.assert_frame_equal(actual, ground_truth, check_dtype=False)
```

### How the comparison works

- **The test asks for both fixtures** by listing them as inputs: `(anno, ground_truth)`.
- **`ids`** is the list of your ten Genetic IDs, in the order they appear in `ground_truth.tsv`.
- **`columns`** is every ground-truth column except `genetic_id`: individual ID, publication, DOI, date, group, country, latitude, and SNPs. The list comprehension simply skips `genetic_id`.
- **Building `actual`**, in three steps:
  1. `set_index("genetic_id")` makes Genetic ID the row label, so you can look up rows by ID instead of by position. This is "always match by ID, never by row order" in action.
  2. `.loc[ids, columns]` picks out exactly your ten individuals, in your file's order, and exactly the columns being compared.
  3. `.reset_index()` turns `genetic_id` back into an ordinary first column, so `actual` has the same shape as `ground_truth`.
- **`pd.testing.assert_frame_equal(actual, ground_truth, ...)`** is pandas' built-in tool for comparing two tables. If anything differs, it says exactly which column and row, and shows both values. Two details:
  - **It treats missing values as equal to each other.** A plain `==` comparison wouldn't, as you saw with the publication columns in `profile_ids.py`.
  - **`check_dtype=False`** ignores differences in *storage* type (for example, a number stored as a whole number in one table and a decimal in the other), while still requiring the actual values to match.

### Test the data assumptions

Create `tests/test_data_assumptions.py`:

```python
"""Facts about AADR v66.p1 that aadrkit's design relies on.

These test the data, not the code. If they fail after switching to a
different AADR release, revisit the design decisions in docs/anno_notes.md.
"""


def test_zero_bp_means_present_day(anno):
    """Every individual dated 0 BP is labeled 'present'."""
    at_zero = anno[anno["date_bp"] == 0]
    assert len(at_zero) == 3970
    assert (at_zero["full_date"] == "present").all()


def test_reference_genomes(anno):
    """Exactly four rows are reference genomes, not individuals."""
    refs = anno[anno["genetic_id"].str.endswith(".REF")]
    assert sorted(refs["genetic_id"]) == [
        "Ancestor.REF", "Chimp.REF", "Gorilla.REF", "Href.REF",
    ]
    assert (refs["data_type"] == "Reference Genome").all()
```

### Why these are different from the other tests

Your other tests check that **your code** works correctly. These check that **the data** still behaves the way your design assumes:

- The present-day filter will rely on "0 BP means present-day."
- The default exclusion of reference genomes will rely on them ending in `.REF`.

If someone later points `aadrkit` at a newer AADR release where, say, unknown dates are also stored as 0, the code would run without errors and quietly give wrong answers. These tests turn that hidden risk into a visible failure, and the docstring at the top of the file tells whoever sees it what to do next.

Two pandas pieces are new:

- **`.all()`** is true only if every value in the column is true. So `(at_zero["full_date"] == "present").all()` means "every 0 BP row says present." The parentheses matter: the comparison runs first, then `.all()` checks the results.
- **`.str.endswith(".REF")`** checks the end of each ID. The dot is just a dot here, because `endswith` matches text literally rather than using regular expressions.

### Run the tests

```bash
pytest -v
```

You should see **11 passed**: the 8 from before, the ground truth test, and the two data-assumption tests. The tests now come from three files, and the `.anno` file is still loaded only once.

### Prove the ground truth test can fail

Same idea as with the indentation bug: a test that has never failed might not be testing anything. Break the loader on purpose, in exactly the way this test exists to catch.

**1.** In `src/aadrkit/anno.py`, change the SNP pattern to pick the wrong column, the Human Origins count instead of 1240k:

```python
    "snps_1240k": r"SNPs hit on autosomal targets .*on HO snpset",
```

**2.** Run only the ground truth test. `-k` selects tests whose names contain the given text:

```bash
pytest -v -k hand_verified
```

It should **fail**, and `assert_frame_equal` should report that the `snps_1240k` column differs, showing your verified values next to the wrong ones. Notice that `test_shape` would still pass with this bug, since the column count hasn't changed. That's exactly the gap this test fills.

**3.** Change the pattern back to `on 1240k snpset`. Then confirm the file is back to exactly what you committed:

```bash
git diff src/aadrkit/anno.py
```

**No output means no changes**, so the pattern is restored exactly. Then run the full suite again and confirm 11 passed.

Intentionally breaking code to check that tests catch it is a small version of a technique called **mutation testing**. Describing it in your report's oversight section shows the tests were themselves tested.

### Commit

```bash
git add tests/conftest.py tests/test_anno.py tests/test_data_assumptions.py
```

```bash
git commit -m "Test loader against hand-verified individuals and data assumptions"
```

Paste the `pytest -v` output from step 4 and the failure message from step 5. After that, Step 8 is the first filter functions: date range and present-day exclusion.
- **Verificaiton:** I ran the `pytest -v` and all 11 tests passed. I also edited the `anno.py` script to pick the wrong column by changing the SNP pattern. I then ran only the ground truth test against that and it failed successfully with an assertion failure and it reported that the `snp_1240k` column differed. The `test_shape` also passed because the column count did not change. 

## Entry 9:
- **Tool:** Cladue (Opus 5.5)
- **What I was doing:** Creating the first filter functions.
- **What I asked (verbatim):** "I need you to help me write a script that takes the table from `load_anno` and returns a new table containing only the rows that pass. Each filter will be a small function. Let's start with three filters: 1) a filter for date range that keeps individuals dated between two values, 2) a filter that excludes present day individuals, and 3) a filter that removes reference genomes. Important to note as a decision is that present day means exactly `date_bp == 0` so someone like Khwit is kept. I would like to then do a toy tests to test these beginning filters. Build a table that tests each edge case(present  day, post 1950, sits exactly on a boundary years, missing date, and ref genome).
- **Exact output (verbatim):**
Excellent. You've now seen the ground truth test fail on a real bug and pass on the fix, so you know it actually guards the loader.

### The first filter functions

### How the filters will be designed

This design has three advantages:

- **They combine freely.** A full query becomes a chain: filter by date, then remove present-day individuals, then filter by country. Each step's output feeds the next.
- **Each is easy to test on its own.** One function, one job, a few clear tests.
- **They don't change the original table.** Each filter returns a new one, so you can't accidentally lose data partway through a chain.

Decisions like "exclude reference genomes by default" and printed messages like "784 individuals excluded" will live one level up, in a single top-level function we'll build after the individual filters work. Keeping the filters simple now makes that easier later.

This step builds three filters:

1. **`filter_date_range`**: keep individuals dated between two values.
2. **`exclude_present_day`**: remove present-day individuals.
3. **`exclude_reference_genomes`**: remove the four `.REF` rows.

### One design decision: what counts as "present-day"?

Present-day means exactly `date_bp == 0`, so Khwit is **kept**. Khwit has a real historical date, sampled from a 20th-century burial, and AADR itself distinguishes it ("1954 CE") from "present." A user who wants only older individuals can combine this with a date range, such as `min_bp=100`. The docstring will state this explicitly, and Khwit becomes the test for it.

If you'd rather treat everything at or below 0 BP as present-day, that's a reasonable choice too. Just change `!= 0` to `> 0` in the code below and flip the Khwit test. Whatever you choose, the documentation and tests should say so.

### Write the filters

Create `src/aadrkit/filters.py`:

```python
"""Filter functions for AADR annotation tables returned by load_anno().

Each function takes a DataFrame and returns a new, filtered DataFrame,
so filters can be combined in any order.
"""
import pandas as pd


def filter_date_range(anno, min_bp=None, max_bp=None):
    """Keep individuals whose mean date (years BP) is within [min_bp, max_bp].

    BP means "before present", where present = 1950 CE, so larger numbers
    are older. Both bounds are inclusive, and either can be None for no
    limit. Individuals with a missing date are excluded whenever a bound
    is given.
    """
    if min_bp is not None and max_bp is not None and min_bp > max_bp:
        raise ValueError(f"min_bp ({min_bp}) is greater than max_bp ({max_bp})")
    keep = pd.Series(True, index=anno.index)
    if min_bp is not None:
        keep &= anno["date_bp"] >= min_bp
    if max_bp is not None:
        keep &= anno["date_bp"] <= max_bp
    return anno[keep]


def exclude_present_day(anno):
    """Remove present-day individuals (date_bp == 0, labeled "present" in AADR).

    Individuals dated after 1950 CE (negative BP, such as 1954 CE) are kept,
    because they have a real historical date rather than "present".
    """
    return anno[anno["date_bp"] != 0]


def exclude_reference_genomes(anno):
    """Remove reference genomes (Genetic IDs ending in ".REF"), which are not individuals."""
    return anno[~anno["genetic_id"].str.endswith(".REF")]
```

### How each filter works

**`filter_date_range`**

- **`min_bp=None, max_bp=None`** are **default values**. If a caller leaves one out, it's `None`, meaning "no limit on that side." So `filter_date_range(anno, min_bp=5000)` means "5,000 years or older," with no upper limit.
- **Why name them `min_bp` and `max_bp`?** Because BP counts backward, "start" and "end" would be confusing: is the start the older date or the younger one? `min_bp=3000, max_bp=5000` reads unambiguously as "between 3,000 and 5,000 years before present."
- **The `raise ValueError`** catches a reversed range like `min_bp=5000, max_bp=3000`. Without it, the filter would quietly return zero rows, and the user might think there simply aren't any individuals in that range. An error message makes the mistake obvious.
- **`keep = pd.Series(True, index=anno.index)`** starts with a column of `True`, one per row, meaning "keep everything so far." `index=anno.index` lines its rows up exactly with `anno`'s rows.
- **`keep &= ...`** is short for `keep = keep & ...`. It narrows the selection: a row stays `True` only if it was already `True` **and** passes the new condition. Each bound that's given narrows it further.
- **Missing dates:** comparing a missing value with anything gives `False`, so rows with no date are dropped whenever a bound is set. The docstring says so. v66.p1 happens to have no missing dates, but the function shouldn't depend on that.
- **`>=` and `<=`** make both bounds **inclusive**: VK202, dated exactly 1000 BP, is kept by `min_bp=1000`.

**`exclude_present_day`**

- **`anno["date_bp"] != 0`** keeps every row whose date isn't exactly 0. Khwit's −4 passes.
- **A missing date is also kept,** because "unknown" isn't the same as "present." It doesn't happen in v66.p1, but now the behavior is defined.

**`exclude_reference_genomes`**

- **`~`** means NOT, as before. So this keeps rows whose ID does **not** end in `.REF`.
- The references are also dated 0 BP, so `exclude_present_day` happens to remove them too. They're still separate functions, because a researcher might want present-day individuals **without** the chimpanzee and gorilla references.

### Write the tests

Create `tests/test_filters.py`. This file uses **two kinds of tests**, and that's worth understanding:

- **Toy-table tests** use a tiny table you build in code, where every edge case is deliberately included and you can see the right answer at a glance. They run instantly and need no AADR data.
- **Real-data tests** check the same filters on the real file, using your hand-verified individuals.

```python
import pandas as pd
import pytest

from aadrkit.filters import (
    exclude_present_day,
    exclude_reference_genomes,
    filter_date_range,
)


@pytest.fixture
def toy():
    """A tiny hand-made table covering the edge cases."""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "Ref.REF"],
        "date_bp": [0, -4, 1000, 1500, float("nan"), 0],
    })


# --- Toy-table tests ---

def test_date_range_bounds_are_inclusive(toy):
    result = filter_date_range(toy, min_bp=1000, max_bp=1500)
    assert list(result["genetic_id"]) == ["C", "D"]


def test_date_range_one_sided(toy):
    assert list(filter_date_range(toy, min_bp=1000)["genetic_id"]) == ["C", "D"]
    assert list(filter_date_range(toy, max_bp=0)["genetic_id"]) == ["A", "B", "Ref.REF"]


def test_date_range_without_bounds_keeps_everything(toy):
    assert len(filter_date_range(toy)) == len(toy)


def test_date_range_rejects_reversed_bounds(toy):
    with pytest.raises(ValueError):
        filter_date_range(toy, min_bp=5000, max_bp=3000)


def test_exclude_present_day_keeps_post_1950_and_missing(toy):
    assert list(exclude_present_day(toy)["genetic_id"]) == ["B", "C", "D", "E"]


def test_exclude_reference_genomes(toy):
    assert list(exclude_reference_genomes(toy)["genetic_id"]) == ["A", "B", "C", "D", "E"]


# --- Real-data tests, using hand-verified individuals ---

def test_date_range_on_real_data(anno):
    ids = set(filter_date_range(anno, min_bp=1000, max_bp=1500)["genetic_id"])
    assert {"VK202.AG", "VK201.AG", "YCH017.AG"} <= ids            # 1000, 1460, 1075 BP
    assert not {"gun005.SG", "I8508.AG", "NA20813.DG"} & ids        # 992, 6356, 0 BP


def test_exclude_present_day_on_real_data(anno):
    result = exclude_present_day(anno)
    ids = set(result["genetic_id"])
    assert len(result) == 23089 - 3970
    assert "Khwit.SG" in ids                                         # -4 BP (1954 CE) is kept
    assert not {"NA20813.DG", "JHF05.AG", "Chimp.REF"} & ids
```

### How the tests work

**The `toy` fixture** builds a six-row table where each row is an edge case:

| Row | `date_bp` | Why it's there |
|---|---|---|
| A | 0 | Present-day |
| B | −4 | Post-1950, like Khwit |
| C | 1000 | Sits exactly on a boundary |
| D | 1500 | Sits exactly on the other boundary |
| E | missing | Missing date |
| Ref.REF | 0 | Reference genome |

This fixture has no `scope`, so it's rebuilt fresh for every test. Building a six-row table takes no time, and a fresh copy means no test can affect another.

**What each toy test checks:**
- **Inclusive bounds:** C (1000) and D (1500) sit exactly on the edges and must both be kept.
- **One-sided ranges:** with only `max_bp=0`, the result is A, B, and Ref.REF. B (−4) is included because −4 is below 0. E is excluded because its date is missing.
- **No bounds:** nothing is removed, not even E.
- **Reversed bounds:** must raise an error rather than quietly return nothing.
- **Present-day:** B (post-1950) and E (missing date) are kept; A and Ref.REF (both 0) are removed.
- **Reference genomes:** only Ref.REF is removed.

**The real-data tests use Python set operations**, which keep membership checks short and readable:
- **`set(...)`** turns the list of IDs into a set, which is good for "is this in there?" questions.
- **`{...} <= ids`** means "every ID on the left is in `ids`," a subset check. VK202 (exactly 1000), VK201 (1460), and YCH017 (1075) must all be inside the range.
- **`not {...} & ids`**: `&` gives the IDs in **both** sets. `not` requires that overlap to be empty, so none of gun005 (992, just outside), I8508 (6356), or NA20813 (0) can appear.
- **`23089 - 3970`** is written as a subtraction on purpose: it shows the reasoning (all rows minus the present-day count from Phase 2) rather than an unexplained number.

### Run the tests

```bash
pytest -v
```

You should see **19 passed**: the previous 11, plus 6 toy tests and 2 real-data tests.

### An outside check on the result

`exclude_present_day` leaves 23,089 − 3,970 = **19,119** rows. That number is familiar: the AADR visualizer page we found when looking up the v66 files reported that v66.0 contains **19,119 sequences representing 17,634 ancient individuals** (https://experience.arcgis.com/experience/244dbd2b96604e178d8a313743b86be5/page/Information). Your filter's row count matches a number published by an independent source.

Check the second number too: how many **distinct people** remain after removing present-day individuals?

```bash
python -c "from aadrkit import load_anno; from aadrkit.filters import exclude_present_day; a = exclude_present_day(load_anno('data/raw/v66.p1_1240K.aadr.PUB.anno')); print(len(a), a['individual_id'].nunique())"
```

- **`len(a)`** is the number of rows, which should be 19,119.
- **`a['individual_id'].nunique()`** is the number of distinct people.

If the second number is **17,634**, your present-day filter agrees with AADR's own published counts on both measures. That's a strong outside confirmation for your report. The page describes v66.0 while your file is v66.p1, so a small difference would be possible from the patch. Since the row count already matches exactly, though, I'd expect this to match as well. If it doesn't, we'll look at what differs.

### Commit

```bash
git add src/aadrkit/filters.py tests/test_filters.py
```

```bash
git commit -m "Add date range, present-day, and reference genome filters with tests"
```

Paste the `pytest -v` summary and the two numbers.
- **Verificaiton:** I typed up the script and logically walked through it. I ran pytest and all 19 tests (including the others I built previously) passed successfully. I also ran the command to see how many distinct people reamined after removing present day individuals and the numbers 19,119 and 17,630 returned showing that my present day filter agrees with AADR's own published counts on both measures (rows and number of distinct people). *See notes for probable merged v66.p1 and resulting 4 individuals less*.

## Entry 10: 
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Writing region (country and coordinates) filters.
- **What I asked (verbatim):** "I need you to help me write script that does the following:" (pasted from `anno_notes.md`): Region filters: Adds two ways to select individuals by place, plus a helper for discovering valid labels: 1) `filter_country`: keep individuals from one or more countries, 2) `filter_bounding_box`: keep individuals whose coordinateds fall inside a rectangle on the map, 3) `list_values`: show every label in a column (such as all 145 countries), so user can see the exact spellings before filtering. Design decisions: match AADR's labels exactly and provide `list_values` so users can see them, case insensitive matching, bounding-box filter excludes individuals who have no coordinates but the country filter still finds them, the bounding box must handle regions that cross the 180 degree longitude line because some data comes from the Pacific (longitude runs -180 to 180 and those two values are the same on a globe, so a box covering Tonga (~ -175) and Vanuatu (~ 167) has to "wrap around" that line. if `min_long` is larger than `max_long`, the box crosses the 180 degree line). 
- Will raise warnings (like if a valid country is chosen to filter but is not in the subset) and errors (like mispelling a country).
- Each filter will remain simple and just return rows. Reporting what was dropped will happen in top-level function that runs the whole query, where it can count before and after every filter in one place."
- **Exact output (verbatim):**
This step adds two ways to select individuals by place, plus a helper for discovering valid labels:

1. **`filter_country`**: keep individuals from one or more countries.
2. **`filter_bounding_box`**: keep individuals whose coordinates fall inside a rectangle on the map.
3. **`list_values`**: show every label in a column (such as all 145 countries), so users can see the exact spellings before filtering.

Both filters use:

| Finding | Design decision |
|---|---|
| AADR lists some territories separately ("Canary Islands" isn't "Spain") | Match AADR's labels exactly, and provide `list_values` so users can see them |
| Capitalization shouldn't matter to a user | Case-insensitive matching |
| 784 individuals have no coordinates, but most of those do have a country | Bounding-box filter excludes them; country filter still finds them |
| Some data comes from the Pacific (Tonga, Vanuatu) | The bounding box must handle regions that cross the 180° longitude line |

### Two new ideas in this step

**Warnings vs. errors.** If a user asks for a country that isn't in the table, there are two possible reasons:

- **A typo**, like "Spian." That's a mistake.
- **A valid country that just isn't in this subset**, for example if they already filtered to 3000–5000 BP and no one from Greenland falls in that range. That's not a mistake at all.

An error would be wrong in the second case. So the filter issues a **warning** instead: a message that appears on screen but doesn't stop the program. A useful rule: **raise an error when something is definitely wrong; warn when it might be.**

**Crossing the 180° line.** Longitude runs from −180 to 180, and those two values are the same line on a globe, running through the Pacific. A box covering Tonga (about −175) and Vanuatu (about 167) has to "wrap around" that line. The convention is: if `min_lon` is *larger* than `max_lon`, the box crosses the 180° line. So `min_lon=160, max_lon=-170` means "from 160° east, across the line, to 170° west." Latitude never wraps, so a reversed latitude range is an error.

**One thing deliberately left out:** the message "784 individuals have no coordinates and were excluded." Each filter stays simple and just returns rows. Reporting what was dropped will happen in the top-level function that runs the whole query, where it can count before and after every filter in one place. I've added it to the plan so it isn't forgotten.

### Add `list_values` to `anno.py`

Add this to the bottom of `src/aadrkit/anno.py`:

```python
def list_values(anno, column):
    """Return each distinct value in a column with its row count, most common first.

    Missing values are not listed. Useful for finding the exact labels to
    pass to a filter, e.g. list_values(anno, "country").
    """
    return anno[column].value_counts()
```

It's the same `value_counts()` you used before, now packaged as part of the tool with a docstring explaining when to use it.

Update `src/aadrkit/__init__.py` so users can reach it directly:

```python
from aadrkit.anno import list_values, load_anno
```

### Add the region filters to `filters.py`

Add `import warnings` near the top of `src/aadrkit/filters.py`, next to `import pandas as pd`. Then add these two functions at the bottom:

```python
def filter_country(anno, countries):
    """Keep individuals whose country (AADR "Political Entity") is in `countries`.

    `countries` can be one name or a list of names. Matching ignores
    capitalization but is otherwise exact: AADR records some territories
    separately (for example, "Canary Islands" is not part of "Spain").
    Use list_values(anno, "country") to see the available labels.
    Rows with a missing country are never kept.
    """
    if isinstance(countries, str):
        countries = [countries]
    wanted = {c.strip().casefold() for c in countries}
    present = anno["country"].str.casefold()
    for name in sorted(wanted - set(present.dropna())):
        warnings.warn(
            f"No rows with country {name!r}; check spelling with "
            f"list_values(anno, 'country')",
            UserWarning,
            stacklevel=2,
        )
    return anno[present.isin(wanted)]


def filter_bounding_box(anno, min_lat=None, max_lat=None, min_lon=None, max_lon=None):
    """Keep individuals whose coordinates fall inside a latitude/longitude box.

    Bounds are inclusive, and any bound can be None for no limit. If
    min_lon is greater than max_lon, the box crosses the 180-degree line
    (e.g. min_lon=160, max_lon=-170 covers the central Pacific).
    Individuals with missing coordinates are excluded whenever a bound is given.
    """
    for name, value, limit in [("min_lat", min_lat, 90), ("max_lat", max_lat, 90),
                               ("min_lon", min_lon, 180), ("max_lon", max_lon, 180)]:
        if value is not None and not -limit <= value <= limit:
            raise ValueError(f"{name} must be between {-limit} and {limit}, got {value}")
    if min_lat is not None and max_lat is not None and min_lat > max_lat:
        raise ValueError(f"min_lat ({min_lat}) is greater than max_lat ({max_lat})")

    keep = pd.Series(True, index=anno.index)
    if min_lat is not None:
        keep &= anno["lat"] >= min_lat
    if max_lat is not None:
        keep &= anno["lat"] <= max_lat
    if min_lon is not None and max_lon is not None and min_lon > max_lon:
        keep &= (anno["lon"] >= min_lon) | (anno["lon"] <= max_lon)
    else:
        if min_lon is not None:
            keep &= anno["lon"] >= min_lon
        if max_lon is not None:
            keep &= anno["lon"] <= max_lon
    return anno[keep]
```

### How `filter_country` works

- **`isinstance(countries, str)`** checks whether the user passed a single name like `"Spain"` instead of a list. If so, it's wrapped in a list. Without this, Python would treat the string as a sequence of letters, and the filter would search for countries named "S", "p", "a", "i", "n." It's a classic Python bug, and this line prevents it.
- **`{c.strip().casefold() for c in countries}`** is a **set comprehension**, like the list comprehensions you've used but with curly braces, producing a set. For each name, `.strip()` removes accidental spaces at either end, and `.casefold()` converts it to lowercase. `casefold` is a slightly stronger version of `lower` that also handles letters from other languages correctly.
- **`present`** is the country column converted to lowercase, so both sides of the comparison use the same capitalization. Missing countries stay missing.
- **`wanted - set(present.dropna())`** is set subtraction: requested names that don't appear in the table at all. For each one, `warnings.warn(...)` issues a warning that points the user to `list_values`.
  - **`UserWarning`** is the standard category for warnings meant for the person using the code.
  - **`stacklevel=2`** makes the warning point at the user's own line that *called* `filter_country`, rather than at a line inside `aadrkit`. That's the line they actually need to look at.
- **`present.isin(wanted)`** is true for rows whose country is in the requested set. Missing countries are never in the set, so those rows are never kept.

### How `filter_bounding_box` works

- **The validation loop** checks each given bound against its legal range: ±90 for latitude, ±180 for longitude. Writing the four checks as one loop over a small list avoids four nearly identical `if` statements. `not -limit <= value <= limit` reads as "the value is not between −limit and +limit."
- **Reversed latitude** is an error, since latitude can't wrap around.
- **The `keep` pattern** is the same one as `filter_date_range`: start with all `True` and narrow with `&=`.
- **The longitude part has two branches:**
  - **If `min_lon > max_lon`**, the box crosses the 180° line, so a row is kept if it's on **either** side: east of `min_lon` **or** west of `max_lon`. `|` means OR.
  - **Otherwise**, it's an ordinary range, handled just like latitude.
- **Missing coordinates** fail every comparison, so those rows are dropped whenever any bound is given, as the docstring says.

### Write the tests

Add these to `tests/test_filters.py`. First, extend the import at the top:

```python
import pytest
import pandas as pd

from aadrkit.anno import list_values
from aadrkit.filters import (
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
    filter_date_range,
)
```

Then add a second toy fixture and the new tests at the bottom:

```python
@pytest.fixture
def places():
    """A tiny hand-made table covering the region edge cases."""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "F", "G"],
        "country": ["Spain", "Canary Islands", "United Kingdom", "Tonga",
                    "Vanuatu", float("nan"), "Uzbekistan"],
        "lat": [40.0, 28.0, 59.1, -21.2, -15.4, float("nan"), float("nan")],
        "lon": [-3.0, -15.5, -3.0, -175.2, 167.0, float("nan"), float("nan")],
    })


# --- Region: toy-table tests ---

def test_country_ignores_capitalization_and_territories(places):
    assert list(filter_country(places, "spain")["genetic_id"]) == ["A"]


def test_country_accepts_a_list(places):
    result = filter_country(places, ["Spain", "United Kingdom"])
    assert list(result["genetic_id"]) == ["A", "C"]


def test_country_finds_individuals_without_coordinates(places):
    assert list(filter_country(places, "Uzbekistan")["genetic_id"]) == ["G"]


def test_country_warns_about_unknown_names(places):
    with pytest.warns(UserWarning, match="spian"):
        result = filter_country(places, "Spian")
    assert result.empty


def test_bounding_box_basic(places):
    result = filter_bounding_box(places, min_lat=35, max_lat=60, min_lon=-10, max_lon=0)
    assert list(result["genetic_id"]) == ["A", "C"]


def test_bounding_box_crosses_180_degrees(places):
    result = filter_bounding_box(places, min_lon=160, max_lon=-170)
    assert list(result["genetic_id"]) == ["D", "E"]


def test_bounding_box_rejects_invalid_bounds(places):
    with pytest.raises(ValueError):
        filter_bounding_box(places, min_lat=-100)
    with pytest.raises(ValueError):
        filter_bounding_box(places, min_lat=60, max_lat=35)


# --- Region: real-data tests ---

def test_country_on_real_data(anno):
    spain = filter_country(anno, "Spain")
    assert len(spain) == list_values(anno, "country")["Spain"] == 802
    assert "gun005.SG" not in set(spain["genetic_id"])               # Canary Islands
    assert "gun005.SG" in set(filter_country(anno, "canary islands")["genetic_id"])


def test_whole_world_box_excludes_missing_coordinates(anno):
    world = filter_bounding_box(anno, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180)
    assert len(world) == 23089 - 784
    assert not {"I8508.AG", "Khwit.SG", "Chimp.REF"} & set(world["genetic_id"])
```

### What the tests check

**The `places` fixture** includes every region edge case:
- **A and B:** Spain versus the Canary Islands.
- **C:** a second country, for testing lists.
- **D and E:** Tonga and Vanuatu, on opposite sides of the 180° line.
- **F:** missing everything.
- **G:** a country but no coordinates, like I8508.

**The toy tests:**
- **Capitalization and territories:** lowercase `"spain"` finds A but not B.
- **Lists:** two countries in one call.
- **No coordinates:** G is found by country even though it has no coordinates. This is the "country filter as a fallback" behavior from your notes.
- **`pytest.warns(UserWarning, match="spian")`** works like `pytest.raises`, but for warnings. `match` also checks that the warning message contains the misspelled name, so the user would know exactly which name was wrong. `result.empty` is true when the table has no rows.
- **Ordinary box:** A (Spain) and C (UK) are inside; B (Canary Islands, at −15.5° longitude) is just outside the west edge.
- **Crossing 180°:** D (−175.2) and E (167.0) are both found, even though they're numerically far apart.
- **Invalid bounds:** an impossible latitude and a reversed latitude range both raise errors.

**The real-data tests:**
- **Spain:** **802** is the count you saw in the previous top-ten list. The chained comparison `a == b == 802` checks that the filter, `list_values`, and your earlier profiling all agree. Then it checks that gun005 isn't in Spain but *is* found under "canary islands," written in lowercase on purpose.
- **Whole-world box:** a box covering the entire planet should return every individual *with* coordinates, which is exactly **23,089 − 784**. Your three test individuals without coordinates must be absent.

### Run and commit

```bash
pytest -v
```

You should see **28 passed**: the previous 19, plus 7 toy tests and 2 real-data tests.

```bash
git add src/aadrkit/anno.py src/aadrkit/__init__.py src/aadrkit/filters.py tests/test_filters.py
```

```bash
git commit -m "Add country and bounding-box filters, list_values helper, and tests"
```

Paste the `pytest -v` summary.
- **Verificaiton:** I typed up the script and logically walked through it. I ran pytest and all 28 tests (including the others I built previously) passed successfully. 

## Entry 11: 
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Creating a script for population filters.
- **What I asked (verbatim):** "Can you help me in the same way as before to create scripts and test for population filters? Follow these ideas: Population filters: Will probably be used the most since AADR's Group IDs encode place, period, and culture all at once. Design Decisions: Exact matching by default plus browsing because 3,897 groups with exact names are hard to guess, an optional regex mode because researchers might want "every Iron Age group" or "every Viking group", matching on the base group name (suffix removed) with excluding outliers unless true because 499 groups end in an outlier suffix, and one explicity option that works the same way in both matching modes because outlier inclusion is the researchers decision.*Match on the base name, decide outliers seperate*. On a different final step, the outliers are removed unless the user asks for the. 
- **Exact output (verbatim):**
### The population filter

| Finding | Design decision |
|---|---|
| 3,897 groups, with exact names hard to guess | Exact matching by default, plus `list_values(anno, "group_id")` to browse |
| Researchers often want "every Iron Age group" or "every Viking group" | An optional **regular-expression** mode (Week 4 material) |
| 499 groups end in an outlier suffix: `-o`, `-ohighEEF`, `-oEastAsia` | Match on the **base group name** (suffix removed); exclude outliers unless `include_outliers=True` |
| Outlier inclusion is the researcher's scientific decision | One explicit option that works the same way in both matching modes |

### The key idea: match on the base name, decide outliers separately

Every Group ID is split into two pieces of information:

- **The base group:** `England_BellBeaker-ohighEEF` becomes `England_BellBeaker`.
- **Whether it's an outlier:** yes, because it has the `-o...` suffix.

Matching happens **only on the base group**. Then, as a separate final step, outliers are removed unless the user asked for them. That gives one simple rule for users: *"name the population you want; decide separately whether to include its outliers."* It works the same whether they typed an exact name or a pattern.

Without this split, the two modes would treat outliers inconsistently. A pattern like `Viking` would silently include `Scotland_Viking-o`, while the exact name `Scotland_Viking` would silently exclude it.

### Add the population filter to `filters.py`

Add this to the bottom of `src/aadrkit/filters.py`:

```python
# Outlier groups end in "-o", optionally followed by a description with no
# underscore, e.g. "Scotland_Viking-o" or "England_BellBeaker-ohighEEF".
OUTLIER_SUFFIX = r"-o[^_]*$"


def is_outlier(group_ids):
    """True for each Group ID marked as a population-genetic outlier ("-o" suffix)."""
    return group_ids.str.contains(OUTLIER_SUFFIX, regex=True, na=False)


def base_group(group_ids):
    """Remove any outlier suffix: "England_BellBeaker-ohighEEF" -> "England_BellBeaker"."""
    return group_ids.str.replace(OUTLIER_SUFFIX, "", regex=True)


def filter_group(anno, groups, include_outliers=False, regex=False):
    """Keep individuals whose population label (AADR "Group ID") matches `groups`.

    Matching uses the base group name, with any outlier suffix ("-o",
    "-ohighEEF", ...) removed, and ignores capitalization. Outliers are
    excluded unless include_outliers=True.

    regex=False: `groups` are exact base names, e.g. "Scotland_Viking".
    regex=True: `groups` are regular-expression patterns searched within
    the base name, e.g. "_IA$" (ends with "_IA") or "Viking" (contains "Viking").
    `groups` can be one name/pattern or a list.
    """
    if isinstance(groups, str):
        groups = [groups]
    base = base_group(anno["group_id"]).str.casefold()

    if regex:
        keep = pd.Series(False, index=anno.index)
        for pattern in groups:
            hits = base.str.contains(pattern, case=False, regex=True, na=False)
            if not hits.any():
                warnings.warn(f"Pattern {pattern!r} matched no groups", UserWarning, stacklevel=2)
            keep |= hits
    else:
        wanted = {g.strip().casefold() for g in groups}
        for name in sorted(wanted - set(base.dropna())):
            warnings.warn(
                f"No group {name!r}. Give the name without any outlier suffix "
                f"(use include_outliers=True for outliers), and check spelling "
                f"with list_values(anno, 'group_id')",
                UserWarning,
                stacklevel=2,
            )
        keep = base.isin(wanted)

    if not include_outliers:
        keep &= ~is_outlier(anno["group_id"])
    return anno[keep]
```

### How it works

**`OUTLIER_SUFFIX`** stored once at the top so every function uses the same definition:
- **`-o`** is the literal suffix marker.
- **`[^_]*`** allows any following characters except an underscore (`highEEF`, `EastAsia`, or nothing at all).
- **`$`** anchors it at the end of the name.

The comment above it shows real examples, so a future reader doesn't have to decode the regular expression to know what it's for.

**`is_outlier`** returns True/False for each Group ID:
- **`.str.contains(..., regex=True)`** checks whether the pattern appears.
- **`na=False`** says "treat a missing Group ID as *not* an outlier," rather than producing a missing value that would break the True/False logic later.

**`base_group`** uses **`.str.replace(OUTLIER_SUFFIX, "", regex=True)`** to replace the suffix with nothing, removing it. Names without a suffix are unchanged.

**`filter_group`**, step by step:
- **The single-name handling** (`isinstance` check) is the same as in `filter_country`.
- **`base`** holds every row's base group in lowercase. Both modes compare against this.
- **Regular-expression mode:**
  - It starts with `keep` as all **`False`** (nothing selected), because each pattern *adds* matches. That's the opposite of the date and region filters, which start with everything and narrow it down.
  - For each pattern, **`base.str.contains(pattern, case=False, ...)`** finds the base names containing it.
  - If a pattern matches nothing, a warning is issued, for the same reason as with countries: it may be a typo, or this subset may just not contain that group.
  - **`keep |= hits`** is short for `keep = keep | hits`: a row is selected if it was already selected **or** matches this pattern. So a list of patterns works as "any of these."
- **Exact mode** is the same logic as `filter_country`. The warning also reminds users to give the name *without* a suffix, since typing `Scotland_Viking-o` would otherwise find nothing with no explanation.
- **The final outlier step** removes every outlier unless `include_outliers=True`. It runs after either mode, so the behavior is identical in both.

### Write the tests

Update the import in `tests/test_filters.py` to include the new functions:

```python
from aadrkit.filters import (
    base_group,
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
    filter_date_range,
    filter_group,
    is_outlier,
)
```

Then add a third toy fixture and these tests at the bottom:

```python
@pytest.fixture
def pops():
    """A tiny hand-made table covering the population edge cases."""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "F", "G"],
        "group_id": ["Scotland_Viking", "Scotland_Viking-o", "Sweden_Viking",
                     "Poland_IA", "England_BellBeaker-ohighEEF",
                     "England_BellBeaker", "Russia_Karasuk-oAegean"],
    })


# --- Population: toy-table tests ---

def test_base_group_strips_outlier_suffix(pops):
    assert list(base_group(pops["group_id"])) == [
        "Scotland_Viking", "Scotland_Viking", "Sweden_Viking", "Poland_IA",
        "England_BellBeaker", "England_BellBeaker", "Russia_Karasuk",
    ]


def test_is_outlier(pops):
    assert list(is_outlier(pops["group_id"])) == [False, True, False, False, True, False, True]


def test_group_exact_excludes_outliers_by_default(pops):
    assert list(filter_group(pops, "Scotland_Viking")["genetic_id"]) == ["A"]


def test_group_exact_can_include_outliers(pops):
    result = filter_group(pops, "Scotland_Viking", include_outliers=True)
    assert list(result["genetic_id"]) == ["A", "B"]


def test_group_exact_ignores_capitalization(pops):
    assert list(filter_group(pops, "scotland_VIKING")["genetic_id"]) == ["A"]


def test_group_exact_does_not_match_partial_names(pops):
    with pytest.warns(UserWarning, match="viking"):
        result = filter_group(pops, "Viking")
    assert result.empty


def test_group_regex_contains(pops):
    assert list(filter_group(pops, "Viking", regex=True)["genetic_id"]) == ["A", "C"]
    result = filter_group(pops, "Viking", regex=True, include_outliers=True)
    assert list(result["genetic_id"]) == ["A", "B", "C"]


def test_group_regex_anchored_end(pops):
    assert list(filter_group(pops, "_IA$", regex=True)["genetic_id"]) == ["D"]


def test_group_regex_keeps_outlier_descriptions_with_their_group(pops):
    result = filter_group(pops, "BellBeaker", regex=True, include_outliers=True)
    assert list(result["genetic_id"]) == ["E", "F"]


def test_group_regex_warns_when_nothing_matches(pops):
    with pytest.warns(UserWarning, match="Neanderthal"):
        result = filter_group(pops, "Neanderthal", regex=True)
    assert result.empty


# --- Population: real-data test ---

def test_group_on_real_data(anno):
    default = set(filter_group(anno, "Scotland_Viking")["genetic_id"])
    with_outliers = set(filter_group(anno, "Scotland_Viking", include_outliers=True)["genetic_id"])
    assert "VK202.AG" in default and "VK201.AG" not in default
    assert {"VK202.AG", "VK201.AG"} <= with_outliers
```

### What the tests check

**The `pops` fixture** covers each kind of group name:

| Row | Group ID | Why it's there |
|---|---|---|
| A | `Scotland_Viking` | Plain group |
| B | `Scotland_Viking-o` | Same group, bare outlier suffix (like VK201) |
| C | `Sweden_Viking` | A different Viking group, for pattern matching |
| D | `Poland_IA` | Tests anchoring with `$` |
| E | `England_BellBeaker-ohighEEF` | Outlier with a description after the suffix |
| F | `England_BellBeaker` | E's base group |
| G | `Russia_Karasuk-oAegean` | Another described outlier, like RISE492 |

**What each test confirms:**
- **`base_group` and `is_outlier`** are checked row by row, including the described suffixes (`-ohighEEF`, `-oAegean`).
- **Exact mode excludes outliers by default** (only A), and **includes them on request** (A and B).
- **Capitalization doesn't matter** (`scotland_VIKING` works).
- **Exact mode never does partial matching:** `"Viking"` alone matches no group exactly, so the result is empty and a warning names what failed. This keeps exact mode trustworthy: it never quietly matches more than the user typed.
- **Regex "contains":** `Viking` finds both Scottish and Swedish Vikings, and adds the outlier only when asked.
- **Regex anchoring:** `_IA$` finds only names *ending* in `_IA`. This is the anchoring idea from before, now part of the tool.
- **Described outliers belong to their base group:** `BellBeaker` with outliers included returns both E and F.
- **A pattern that matches nothing** produces a warning.

**The real-data test** is your VK201/VK202 pair, chosen earlier specifically for this filter: VK202 is in the default result, and VK201 appears only with `include_outliers=True`.

### Add two data assumption tests

The filter relies on two facts about v66.p1 that are worth guarding. Add these to `tests/test_data_assumptions.py`, with `import pandas as pd` and `from aadrkit.filters import is_outlier` at the top:

```python
def test_outlier_rule_matches_simple_search(anno):
    """The precise "-o" rule finds the same 499 groups as a plain text search."""
    groups = pd.Series(anno["group_id"].unique())
    precise = is_outlier(groups).sum()
    simple = groups.str.contains("-o", regex=False).sum()
    assert precise == simple == 499


def test_group_ids_are_distinct_ignoring_capitalization(anno):
    """Case-insensitive matching never merges two different groups."""
    groups = anno["group_id"].dropna().unique()
    assert len({g.casefold() for g in groups}) == len(groups)
```

**The first test**: the precise regular expression and the naive "contains `-o`" search must agree, at 499 groups. If a future AADR release had a group with `-o` somewhere other than the end, the counts would differ, and this test would flag it before it caused a wrong result.

**The second test** protects the decision to ignore capitalization. If two genuinely different groups were spelled the same except for capitals, lowercasing everything would merge them into one. This test counts the groups before and after lowercasing; equal counts mean no two groups collide.

### Run and commit

```bash
pytest -v
```

You should see **41 passed**: the previous 28, plus 10 toy tests, 1 real-data test, and 2 data assumption tests.

```bash
git add src/aadrkit/filters.py tests/test_filters.py tests/test_data_assumptions.py
```

```bash
git commit -m "Add population filter with exact/regex matching and outlier handling"
```

Paste the `pytest -v` summary.
- **What I asked next (verbatim):** I ran into the same error repeatedly after manually checking my code but deduced that there was probably a mismatch in the Group IDs when converting them to lowercase. I pasted the error and asked Claude to help me write code to find the error and determine if it is duplicate populations or different:
```bash
________________________________________ test_group_ids_are_distinct_ignoring_capitalization ________________________________________

anno =          genetic_id individual_id                 first_publication  ...       y_haplogroup mt_haplogroup        asses...95             AkbariReichNature2026  ...          I2a1b1a2b           NaN  PROVISIONAL_PASS

[23089 rows x 16 columns]

    def test_group_ids_are_distinct_ignoring_capitalization(anno):
        """Case-insensitive matching never merges two different groups."""
        groups = anno["group_id"].dropna().unique()
>       assert len({g.casefold() for g in groups}) == len(groups)
E       AssertionError: assert 3896 == 3897
E        +  where 3896 = len({'abkhasian', 'acb', 'acb-1', 'acb-2', 'acb-3', 'adygei', ...})
E        +  and   3897 = len(array(['Luxembourg_Loschbour_Mesolithic',\n       'Greece_EpanoKoufonisi_EBA_Cycladic', 'Greece_ElatiLogkassite_MBA',\n       ..., 'China_Penghu_Suogang_LN', 'Afghanistan_DarraiKurCave_MBA',\n       'Romania_Brailita_Mesolithic'], shape=(3897,), dtype=object))

tests/test_data_assumptions.py:33: AssertionError
====================================================== short test summary info ======================================================
FAILED tests/test_data_assumptions.py::test_group_ids_are_distinct_ignoring_capitalization - AssertionError: assert 3896 == 3897
=================================================== 1 failed, 39 passed in 41.02s ===================================================
02:53:00 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→
```
- **Exact output (verbatim):**
Both mysteries are solved, and the first turned out to be a nice finding.

### The collision is a typo in AADR, and it doesn't affect your filter

The two labels are:

- `Hungary_EarlyAvar-oLowEastAsia` (52 individuals)
- `Hungary_EarlyAvar-olowEastAsia` (1 individual, `A1824.AG`)

Everything about the rows says they're the **same group, written inconsistently**:

- **Same country** (Hungary) and **same time period** (around 1,300 BP).
- **Same paper:** `A1824.AG` comes from `Gnecchi-RusconeKrauseCell2022`, and so does `A1817.AG` right above it, which uses the capital-L spelling.
- **Same meaning:** both are outliers from the Early Avar group, with lower East Asian–related ancestry than is typical for that group. The capitalization of "low" is the only difference.

So this is a small inconsistency in AADR's labels, not two genuinely different populations.

**It also turns out not to matter for your filter at all.** The difference sits entirely *inside the outlier suffix*, and `filter_group` matches on the **base** group name, with the suffix removed. Both labels become `Hungary_EarlyAvar`, and both are outliers. So with or without `include_outliers`, a user gets identical results either way.

That means your code is right. But the test was checking a slightly broader assumption than the code actually relies on. The filter only cares whether **base names** collide, not whether full labels do.

### Fixing the test

Replace `test_group_ids_are_distinct_ignoring_capitalization` in `tests/test_data_assumptions.py` with these two tests, and add `base_group` to the import from `aadrkit.filters` at the top:

```python
def test_known_capitalization_differences_in_group_ids(anno):
    """v66.p1 has exactly one pair of Group IDs differing only by capitalization.

    Both are outliers of Hungary_EarlyAvar from the same study; the outlier
    description is written "Low" in one and "low" in the other.
    """
    labels = anno["group_id"].dropna().drop_duplicates()
    collide = sorted(labels[labels.str.casefold().duplicated(keep=False)])
    assert collide == ["Hungary_EarlyAvar-oLowEastAsia", "Hungary_EarlyAvar-olowEastAsia"]


def test_base_groups_are_distinct_ignoring_capitalization(anno):
    """Case-insensitive matching never merges two different base groups.

    filter_group matches on base names (outlier suffix removed), so this is
    the assumption that matters for filtering.
    """
    bases = base_group(anno["group_id"].dropna()).unique()
    assert len({b.casefold() for b in bases}) == len(bases)
```

### Why two tests instead of one

**The first test records exactly what you found.** It doesn't just say "collisions are fine now." It names the **one** known pair. If a future AADR release added a *new* collision, the list wouldn't match, and the test would fail again and make you look. Writing down the specific exception keeps the alarm working for everything else. That's very different from deleting the test or loosening it until it passes.

- **`sorted(...)`** puts the two labels in a fixed order so the comparison is reliable. Capital letters sort before lowercase ones, which is why `-oLow...` comes first.

**The second test checks the assumption the code actually depends on:** after stripping outlier suffixes, no two base names differ only by capitalization. It's the same counting trick as before, applied to `base_group(...)` instead of the raw labels.

I expect this second test to pass, but run it rather than assume. If it fails, there's a case collision among the base names themselves, which would matter, and we'd look at it the same way.

### The missing test

Comparing the collected list, the one that's absent is:

**`test_group_regex_keeps_outlier_descriptions_with_their_group`**, the Bell Beaker test. It probably just didn't get copied in. Add it to `tests/test_filters.py` with the other population tests:

```python
def test_group_regex_keeps_outlier_descriptions_with_their_group(pops):
    result = filter_group(pops, "BellBeaker", regex=True, include_outliers=True)
    assert list(result["genetic_id"]) == ["E", "F"]
```

It's worth having: it's the only toy test where an outlier has a **description** after `-o` (`-ohighEEF`) and still has to be recognized as belonging to its base group. That's exactly the situation in the Avar labels you just found.

A useful habit from this: when you add tests, run `pytest --collect-only -q` and check that the count went up by as much as you expected. A test that was never collected can't fail, so nothing else would have told you it was missing.

### Run and commit

```bash
pytest -v
```

You should now see **42 passed**: the 40 collected before, plus the missing Bell Beaker test, plus the second new data assumption test (the first one replaced the failing test).

```bash
git add src/aadrkit/filters.py tests/test_filters.py tests/test_data_assumptions.py scripts/find_case_collisions.py
```

```bash
git commit -m "Add population filter; document case-only Group ID difference in v66.p1"
```

Paste the `pytest -v` summary. 
- **Verificaiton:** I inspected the error myself, wrote the fix, reran the code, and made notes of the change. The code subsequently passed after the fixes.

## Entry 12: 
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Creating deduplication and coverage filters.        
- **What I asked (verbatim):** Can you write me code chunks that will achieve the following criteria for coverage and deduplication filtering: 
Coverage and deduplication filter: The coverage filter keeps individuals with at least a given number of SNPs covered but the threshold has no default value. The min number depends on the analysis. Python will refuse to run until a number is given. The deduplication filter keeps one row per person, choosing which has the most SNPs. From previously, 23,089 rows belong to 21,433 people. Follow these rules: 1. pick the row with the most SNPs, 2. Break ties consistently if rows have exactly the same SNP count, the function must pick the same one every time (RULE = ALPHABETICAL), 3. Do not merge rows with a missing individual ID because there is no way to know whether they are the same person if two rows both lack an ID. Deduplication happens after filtering so best row is chosen among rows that passed. Deduplication rules: one person, two datasets (keep higher SNPs), one person one row (keep), tie (Keep alphabetical first), and no individual id (keep both). 
- **Exact output (verbatim):**
### Coverage filter and deduplication

### The coverage filter

**`filter_min_snps`** keeps individuals with at least a given number of SNPs covered (column 26, `snps_1240k`).

There's one important design decision: **the threshold has no default value**. The right minimum depends entirely on the analysis. Some methods work with 20,000 SNPs, others need hundreds of thousands. If the function quietly assumed a number, users might not realize data was being dropped. Leaving the threshold without a default means Python itself refuses to run the function until a number is given.

### Deduplication

**`deduplicate_individuals`** keeps one row per person, choosing the row with the most SNPs. 23,089 rows belong to 21,433 people, and `YCH017` alone has 11 rows. It needs three rules:

1. **Pick the row with the most SNPs.** That's the most informative dataset for that person, and it's how `YCH017.AG` should win.
2. **Break ties consistently.** If two rows have exactly the same SNP count, the function must pick the same one every time, or rerunning the same query could produce different files, which would break reproducibility. The rule: the alphabetically first Genetic ID wins.
3. **Never merge rows with a missing Individual ID.** If two rows both lack an ID, there's no way to know whether they're the same person, so both are kept. v66.p1 has no missing IDs, but the function shouldn't silently merge strangers if a future version does.

**When to deduplicate:** you decided **filter first, then deduplicate**, so the best row is chosen among rows that passed the user's filters. For the coverage filter specifically, the order happens not to matter: keeping each person's best row and then applying a threshold gives the same result as applying the threshold first. But it does matter for other filters. For example, if one person's rows had different data types, deduplicating first could keep a row that a later filter removes, losing that person entirely. The top-level function can enforce the correct order, so users don't have to remember it.

### Add both functions to `filters.py`

Add these to the bottom of `src/aadrkit/filters.py`:

```python
def filter_min_snps(anno, min_snps):
    """Keep individuals with at least `min_snps` SNPs covered on the 1240K panel.

    There is deliberately no default: the right threshold depends on the
    analysis, so the user must choose it. The bound is inclusive.
    Individuals with a missing SNP count are excluded.
    """
    if min_snps < 0:
        raise ValueError(f"min_snps must be 0 or greater, got {min_snps}")
    return anno[anno["snps_1240k"] >= min_snps]


def deduplicate_individuals(anno):
    """Keep one row per person (individual_id): the row with the most 1240K SNPs.

    Ties are broken by Genetic ID in alphabetical order, so the result is
    always the same. Rows with a missing individual_id are all kept, since
    there is no way to tell whether they are the same person. Apply this
    after the other filters, so the best row is chosen among the rows that
    passed them. Rows are returned in their original order.
    """
    has_id = anno["individual_id"].notna()
    ranked = anno[has_id].sort_values(
        ["individual_id", "snps_1240k", "genetic_id"],
        ascending=[True, False, True],
    )
    best = ranked.drop_duplicates("individual_id", keep="first")
    return pd.concat([best, anno[~has_id]]).sort_index()
```

### How `filter_min_snps` works

- **`def filter_min_snps(anno, min_snps):`** has no `=` after `min_snps`, so it's **required**. Calling `filter_min_snps(anno)` without a number raises an error immediately.
- **A negative minimum** can't mean anything sensible, so it raises a `ValueError` instead of quietly returning everyone.
- **`>=`** makes the threshold inclusive, the same convention as the date filter.

### How `deduplicate_individuals` works

It works by **sorting so the winning row for each person comes first**, then keeping only the first row per person:

- **`has_id`** marks rows that have an Individual ID. Only those take part in deduplication.
- **`sort_values([...], ascending=[True, False, True])`** sorts by three columns, in priority order:
  1. **`individual_id`**, ascending: groups each person's rows together.
  2. **`snps_1240k`**, **descending** (`False`): within each person, the most SNPs first.
  3. **`genetic_id`**, ascending: if two rows tie on SNPs, the alphabetically first ID comes first.
- **`drop_duplicates("individual_id", keep="first")`** keeps the first row for each person, which thanks to the sort is their best row.
- **`pd.concat([best, anno[~has_id]])`** stacks the deduplicated rows and the rows without an ID back into one table.
- **`.sort_index()`** puts the rows back in their original file order. Each row has kept its original row label (its "index") through all of these steps, so sorting by that label restores the order from the file. A stable, predictable order also makes the output reproducible.

### Write the tests

Add `deduplicate_individuals` and `filter_min_snps` to the import list at the top of `tests/test_filters.py`, keeping it alphabetical:

```python
from aadrkit.filters import (
    base_group,
    deduplicate_individuals,
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
    filter_date_range,
    filter_group,
    filter_min_snps,
    is_outlier,
)
```

Then add a fourth toy fixture and these tests at the bottom:

```python
@pytest.fixture
def reps():
    """Repeated individuals, a tie, and rows without an Individual ID."""
    return pd.DataFrame({
        "genetic_id": ["P1.AG", "P1.SG", "P2.AG", "P3.AG", "P3.TW", "X.AG", "Y.AG"],
        "individual_id": ["P1", "P1", "P2", "P3", "P3", float("nan"), float("nan")],
        "snps_1240k": [500, 900, 300, 700, 700, 100, 200],
    })


# --- Coverage and deduplication: toy-table tests ---

def test_min_snps_is_inclusive(reps):
    assert list(filter_min_snps(reps, 700)["genetic_id"]) == ["P1.SG", "P3.AG", "P3.TW"]


def test_min_snps_rejects_negative(reps):
    with pytest.raises(ValueError):
        filter_min_snps(reps, -1)


def test_dedupe_keeps_highest_coverage_row(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert "P1.SG" in ids and "P1.AG" not in ids


def test_dedupe_breaks_ties_by_genetic_id(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert "P3.AG" in ids and "P3.TW" not in ids


def test_dedupe_keeps_rows_without_individual_id(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert {"X.AG", "Y.AG"} <= ids


def test_dedupe_preserves_original_order(reps):
    assert list(deduplicate_individuals(reps)["genetic_id"]) == [
        "P1.SG", "P2.AG", "P3.AG", "X.AG", "Y.AG",
    ]


# --- Coverage and deduplication: real-data tests ---

def test_min_snps_on_real_data(anno):
    assert "I13976.SG" in set(filter_min_snps(anno, 281)["genetic_id"])       # exactly 281
    assert "I13976.SG" not in set(filter_min_snps(anno, 282)["genetic_id"])


def test_dedupe_on_real_data(anno):
    result = deduplicate_individuals(anno)
    assert len(result) == 21433
    ych = result[result["individual_id"] == "YCH017"]
    assert list(ych["genetic_id"]) == ["YCH017.AG"]
```

### What the tests check

**The `reps` fixture** covers each deduplication rule:

| Rows | Situation | Expected |
|---|---|---|
| P1.AG (500), P1.SG (900) | One person, two datasets | Keep **P1.SG** (more SNPs) |
| P2.AG (300) | One person, one row | Keep it |
| P3.AG (700), P3.TW (700) | A tie | Keep **P3.AG** (alphabetically first) |
| X.AG, Y.AG | No Individual ID | Keep **both** |

**The toy tests:**
- **Inclusive threshold:** at exactly 700, both tied P3 rows pass, as does P1.SG (900).
- **Negative threshold:** rejected.
- **The three deduplication rules,** each with its own test, so a failure tells you exactly which rule broke.
- **Original order:** the full expected list, which also confirms nothing extra was kept or lost.

**The real-data tests use numbers you already verified independently:**
- **I13976.SG has exactly 281 SNPs**, the lowest in the file, confirmed by hand with `grep`. A threshold of 281 keeps it and 282 drops it. That tests the inclusive boundary on a real record.
- **21,433** is the number of distinct people you counted in Phase 2 with `profile_ids.py`. Deduplicating the whole file must produce exactly one row per person.
- **YCH017:** of its 11 rows, only `YCH017.AG` (1,064,203 SNPs, also hand-verified) may remain. That's exactly what you chose it for in Phase 2.

### Check, run, and commit

First, confirm the new tests were collected. That's your new habit:

```bash
pytest --collect-only -q | tail -n 3
```

- **`| tail -n 3`** shows only the last three lines of the output, where pytest prints the total count.
- You should see **50 tests collected**: the previous 42, plus 6 toy tests and 2 real-data tests.

Then run them:

```bash
pytest -v
```

```bash
git add src/aadrkit/filters.py tests/test_filters.py
```

```bash
git commit -m "Add coverage filter and deduplication with tests"
```

Paste the `pytest -v` summary when it's done.
- **Verificaiton:** I wrote the code, manually thought about the process and workthrough, ran the tests, verified all had passed.

## Entry 13:
- **Tool:** Cladue (Opus 5.5)
- **What I was doing:** Creating and testing a top level function.
- **What I asked (verbatim):** ""Choosing" function: I want to add in a top level function now that calls each filter in the correct order every time (for consistency) that is: min bp, max bp, groups, min snps. Create a new script that runs the selection in order from the filter script functions that we have created and turns it into a report that is then turned into a dataframe at the end. Have it trim the dataset as each step progresses. If a certain filter is left blank, have it be skipped. Remove outliers explicitly and make sure deduplication is last. Then, can you create a script that test to make sure that the function connects/integrates the filtering tests correctly. Check the defaults (no options at all), that every person is unique and appears once, and that the ref genomes are gone. Enable that only the requested steps are run, make sure that the filters are in the correct order if run manually vs running through the choosing function, identify the correct amount of missing coordinates (784), handles the outliers correctly, and handles misspells. Add any design tweaks or additions you deem necessary for this to work smoothly."
- **Exact output (verbatim):**
Fifty passing tests means every filter is checked against both edge cases and your hand-verified individuals. Now we connect them.

### The top-level `select()` function

Right now, a user would have to call each filter themselves, in the right order, and remember the defaults. **`select()`** does all of that in one call:

```python
selected, report = aadrkit.select(anno, min_bp=1000, max_bp=1500,
                                  groups="Scotland_Viking", min_snps=100000)
```

It does three things the individual filters don't:

1. **Runs the filters in a fixed order.** Deduplication always comes last, as you decided, so each person's best row is chosen from the rows that passed every other filter.
2. **Applies the defaults** from your design: reference genomes are excluded, outliers are excluded from population matches, and each person appears once. Each default can be switched off explicitly.
3. **Reports what each step removed.** This is where the transparency promise is kept, including "784 had no coordinates."

### Why a fixed order matters even though most filters don't care

Apart from deduplication, the filters give the **same final rows in any order**: keeping "Iron Age" then "Poland" gives the same people as "Poland" then "Iron Age." But the **report** would differ, because each step's "removed" count depends on what came before it. A fixed order means the same query always produces the same result **and** the same report, which is what reproducibility requires.

### Two new Python ideas

- **Keyword-only arguments.** A `*` in the function definition means every argument after it **must be named**. So `select(anno, 3000, 5000)` is rejected, and you must write `select(anno, min_bp=3000, max_bp=5000)`. With this many numeric options, positional numbers would be an easy way to swap a date for a latitude without noticing. A misspelled name like `min_snp=` also raises an error instead of being silently ignored.
- **Returning two things.** `select` returns a **tuple**, two values bundled together: the selected rows and the report table. You unpack them with `selected, report = select(...)`. The report is a normal DataFrame, so later it can be saved alongside the output files as a record of how each subset was made.

### Write `query.py`

Create `src/aadrkit/query.py`. It's named `query.py` rather than `select.py` because Python's standard library already has a module called `select`, and avoiding the name prevents confusion.

```python
"""Run a full AADR selection: filters in a fixed order, sensible defaults, and a report."""
import pandas as pd

from aadrkit.filters import (
    deduplicate_individuals,
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
    filter_date_range,
    filter_group,
    filter_min_snps,
    is_outlier,
)

REPORT_COLUMNS = ["step", "rows_before", "rows_after", "removed", "note"]


def _record(report, step, before, after, note=""):
    """Add one row to the selection report."""
    report.append({
        "step": step,
        "rows_before": len(before),
        "rows_after": len(after),
        "removed": len(before) - len(after),
        "note": note,
    })


def select(anno, *, min_bp=None, max_bp=None, exclude_present=False,
           countries=None, min_lat=None, max_lat=None, min_lon=None, max_lon=None,
           groups=None, group_regex=False, include_outliers=False,
           min_snps=None, include_references=False, deduplicate=True,
           verbose=True):
    """Select individuals from a load_anno() table.

    Steps run in a fixed order, so the same arguments always give the same
    result and the same report:
      1. reference genomes removed (unless include_references=True)
      2. present-day individuals removed (if exclude_present=True)
      3. date range        (min_bp, max_bp)
      4. country           (countries)
      5. coordinates       (min_lat, max_lat, min_lon, max_lon)
      6. population        (groups, group_regex, include_outliers)
      7. coverage          (min_snps)
      8. one row per person (unless deduplicate=False); always last

    Steps whose arguments are not given are skipped. Outliers only matter
    in the population step, where they are excluded unless
    include_outliers=True. All arguments after `anno` must be named.

    Returns (selected, report): the selected rows, and a table of how many
    rows each step removed. The report is also printed if verbose=True.
    """
    report = []
    current = anno

    if not include_references:
        before, current = current, exclude_reference_genomes(current)
        _record(report, "exclude reference genomes", before, current)

    if exclude_present:
        before, current = current, exclude_present_day(current)
        _record(report, "exclude present-day", before, current)

    if min_bp is not None or max_bp is not None:
        before, current = current, filter_date_range(current, min_bp, max_bp)
        _record(report, f"date range (min_bp={min_bp}, max_bp={max_bp})", before, current)

    if countries is not None:
        before, current = current, filter_country(current, countries)
        _record(report, f"country {countries}", before, current)

    bounds = dict(min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
    if any(value is not None for value in bounds.values()):
        no_coords = int((current["lat"].isna() | current["lon"].isna()).sum())
        before, current = current, filter_bounding_box(current, **bounds)
        _record(report, "coordinates", before, current, f"{no_coords} had no coordinates")

    if groups is not None:
        before = current
        matched = filter_group(current, groups, include_outliers=True, regex=group_regex)
        outliers = is_outlier(matched["group_id"])
        if include_outliers:
            current, note = matched, "outliers included"
        else:
            current, note = matched[~outliers], f"{int(outliers.sum())} outliers excluded"
        _record(report, f"group {groups}", before, current, note)

    if min_snps is not None:
        before, current = current, filter_min_snps(current, min_snps)
        _record(report, f"at least {min_snps} SNPs", before, current)

    if deduplicate:
        before, current = current, deduplicate_individuals(current)
        _record(report, "one row per person", before, current)

    report = pd.DataFrame(report, columns=REPORT_COLUMNS)
    if verbose:
        print(report.to_string(index=False))
        print(f"Selected {len(current)} rows.")
    return current, report
```

### How it works

**`_record`** adds one row to the report: the step's name, the row counts before and after, how many were removed, and an optional note.
- **The leading underscore** is a Python convention meaning "internal helper, not for users." It's a signal rather than a restriction.
- **The report starts as a list of dictionaries** (`report = []`), and each step appends one. At the end, `pd.DataFrame(report, columns=REPORT_COLUMNS)` turns the list into a table. Passing `columns` keeps the column order fixed, and gives the right columns even if no steps ran at all.

**`current`** always holds "the rows that have survived so far." Each step takes `current`, filters it, and replaces it.

**`before, current = current, exclude_reference_genomes(current)`** updates two variables in one line. Python evaluates the **whole right side first** (the old `current`, and the filtered result), *then* assigns them: `before` gets the old table and `current` gets the new one. It's the same as writing `before = current` and then `current = exclude_reference_genomes(current)` on separate lines. Every step then has both tables available to compare.

**Each step is wrapped in an `if`**, so it only runs when its arguments were given. Steps that don't run don't appear in the report.

**The coordinate step:**
- **`bounds = dict(...)`** gathers the four coordinate arguments into one dictionary.
- **`any(value is not None for value in bounds.values())`** is true if at least one bound was given.
- **`no_coords`** counts rows missing latitude **or** longitude **before** filtering. That's the "784 had no coordinates" message, placed exactly where you planned it in Phase 2.
- **`filter_bounding_box(current, **bounds)`**: the `**` **unpacks** the dictionary into named arguments. It's equivalent to writing `min_lat=min_lat, max_lat=max_lat, ...` by hand.

**The population step** works slightly differently, so it can report how many outliers it removed:
1. It calls `filter_group` with `include_outliers=True`, getting **everyone** in the matching groups.
2. `is_outlier` marks which of those are outliers.
3. Depending on `include_outliers`, it either keeps them all or removes the outliers, and the note records the count.

Calling `filter_group` only once also means any "unknown group" warning appears once, not twice.

**Deduplication runs last**, unconditionally in position, so it always sees the fully filtered rows.

**`verbose`**: when true (the default), the report is printed. Showing what was removed by default fits your transparency principle, and a user who wants quiet output can pass `verbose=False`.

### Make `select` available from the package

Update `src/aadrkit/__init__.py`:

```python
"""aadrkit: filter and export subsets of the Allen Ancient DNA Resource (AADR)."""

from aadrkit.anno import list_values, load_anno
from aadrkit.query import select

__version__ = "0.1.0"
```

### Write the tests

The individual filters are already tested in detail. These tests check something different: that `select` **connects** them correctly. That's the difference between **unit tests** (one function on its own) and **integration tests** (several pieces working together).

Create `tests/test_query.py`:

```python
import pandas as pd
import pytest

from aadrkit.filters import (
    deduplicate_individuals,
    exclude_present_day,
    exclude_reference_genomes,
    filter_min_snps,
)
from aadrkit.query import select


def test_defaults_remove_references_and_duplicates(anno):
    selected, report = select(anno, verbose=False)
    ids = set(selected["genetic_id"])
    assert not any(i.endswith(".REF") for i in ids)
    assert selected["individual_id"].is_unique
    assert list(report["step"]) == ["exclude reference genomes", "one row per person"]
    assert report.loc[0, "removed"] == 4


def test_only_requested_steps_run(anno):
    _, report = select(anno, min_snps=100000, verbose=False)
    assert list(report["step"]) == [
        "exclude reference genomes", "at least 100000 SNPs", "one row per person",
    ]


def test_matches_filters_applied_by_hand(anno):
    selected, _ = select(anno, exclude_present=True, min_snps=20000, verbose=False)
    by_hand = deduplicate_individuals(
        filter_min_snps(exclude_present_day(exclude_reference_genomes(anno)), 20000)
    )
    pd.testing.assert_frame_equal(selected, by_hand)


def test_reports_missing_coordinates(anno):
    selected, report = select(anno, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180,
                              include_references=True, deduplicate=False, verbose=False)
    assert len(selected) == 23089 - 784
    assert report.loc[0, "note"] == "784 had no coordinates"


def test_group_excludes_and_counts_outliers(anno):
    selected, report = select(anno, groups="Scotland_Viking", verbose=False)
    ids = set(selected["genetic_id"])
    assert "VK202.AG" in ids and "VK201.AG" not in ids
    assert report.loc[1, "note"].endswith("outliers excluded")


def test_arguments_must_be_named(anno):
    with pytest.raises(TypeError):
        select(anno, 3000, 5000)
    with pytest.raises(TypeError):
        select(anno, min_snp=5000)          # misspelled: min_snp, not min_snps
```

### What each test checks

- **Defaults:** with no options at all, reference genomes are gone, every person appears exactly once (`is_unique`), only the two default steps ran, and the first step removed exactly the **4** `.REF` rows you found. `report.loc[0, "removed"]` reads row 0 of the report, column `"removed"`.
- **Only requested steps run:** asking only for coverage adds exactly one step, in the right position, between the two defaults.
- **Matches the filters applied by hand:** the most important test here. It runs the same query two ways, through `select` and by calling each filter manually in the documented order, and checks the results are **identical**. If `select` skipped a step, ran them in a different order, or passed the wrong argument, this would catch it. `select` returns two values, but this test only needs the first, so the second is assigned to `_`, a conventional name for "I'm ignoring this."
- **Missing coordinates:** with references included and deduplication off, a whole-world box must give exactly **23,089 − 784** rows, and the report must say **784**. Both numbers come from your profiling. References are included here so the 784 count isn't affected by the reference rows, which also lack coordinates.
- **Outliers:** the VK202/VK201 pair once more, now through `select`. The report's population step (row 1, after the reference step) must state how many outliers were excluded.
- **Named arguments:** positional numbers and a misspelled option are both rejected with a `TypeError`, Python's error for calling a function the wrong way.

### Check, run, and commit

```bash
pytest --collect-only -q | tail -n 3
```

You should see **56 tests collected**: the previous 50 plus 6 new ones.

```bash
pytest -v
```

Then try it yourself, to see the report a user would see:

```bash
python -c "import aadrkit; a = aadrkit.load_anno('data/raw/v66.p1_1240K.aadr.PUB.anno'); s, r = aadrkit.select(a, min_bp=1000, max_bp=1500, countries='United Kingdom', min_snps=100000)"
```

You should see a small table listing each step, how many rows it removed, and the final count. That's `aadrkit` doing a complete, realistic query in one call.

```bash
git add src/aadrkit/query.py src/aadrkit/__init__.py tests/test_query.py
```

```bash
git commit -m "Add select() to run filters in fixed order with defaults and a report"
```

Paste the `pytest -v` summary and the report table from the example query.
- **Verificaiton:** I read through all of the design decisions and workflow that Claude suggested and made sure it aligned with the design I had in mind and did not add anything unnecessary. I then created the scripts and added code. I ran the pytest and the example run and all returned results as expected: 
```
02:39:58 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→ python -c "import aadrkit; a = aadrkit.load_anno('data/raw/v66.p1_1240K.aadr.PUB.anno'); s, r = aadrkit.select(a, min_bp=1000, max_bp=1500, countries='United Kingdom', min_snps=100000)"
                                     Step  Rows_before  Rows_after  Removed Note
                Exclude Reference Genomes        23089       23085        4
Date range (min_bp = 1000, max_bp = 1500)        23085        3301    19784
                   Country United Kingdom         3301         259     3042
                     At least 100000 SNPs          259         220       39
                       One row per person          220         208       12
Selected 208 rows.
02:42:29 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→
```

## Entry 14:
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Converting aadrkit from a tool that reads metadata into one that extracts the genotype data automatically. 
- **What I asked (verbatim):** "Next I need a Convertf wrapper. I need the tool to automate genotype extraction by choosing which individuals to keep, write a file with those chosen (.ind) and everyone else labeled as ignored, write a parameter file, run convertf -p, and check the output. Originally I had planned my own .geno reader, but instead of that I would like to do something more simple that consolidates everything that interacts with convertf to go into one place and can be called with a function. I want the output data to have a clear traceable trail. Please add any features or design as needed to fulfill the requirements and to ensure it has failsafes and future modification ability. Can you help me modify and add to my existing code?"
- **Exact output (verbatim):**
That report is exactly what `select` was built to show: each filter's effect, step by step. Notice the last line. In the United Kingdom between 1000 and 1500 BP, **12 rows** were extra datasets for people already selected, and deduplication removed them. Without that step, those 12 people would have been counted twice.

### The `convertf` wrapper

This step turns `aadrkit` from a metadata tool into a genotype tool. It automates the five manual steps:

| Manual step | Now done by code |
|---|---|
| Choose which individuals to keep | `select()` |
| Write a `.ind` with everyone else labeled `Ignore` | `write_selection_ind()` |
| Write the parameter file | `write_par()` |
| Run `convertf -p ...` | `subprocess.run(...)` |
| Check the output | count the output individuals; tests check the genotypes |

All of this goes into one function, **`extract_genotypes()`**.

### The "backend" idea from your proposal

You planned an `AADRBackend` design so (your own `.geno` reader) could replace `convertf` later without rewriting the filters. Here's a lighter version of that idea: **everything that touches `convertf` lives in one module, `convertf.py`, behind one public function, `extract_genotypes()`.** The filters and `select()` know nothing about `convertf`. A future module would just provide its own `extract_genotypes()` with the same inputs and outputs, and nothing else would change.

That keeps the design goal (swappable genotype reading) without extra machinery. 

### Keeping a record of every extraction

`extract_genotypes()` keeps **the modified `.ind`, the parameter file, and `convertf`'s log** next to the output files. Anyone looking at an output later can see exactly how it was made, and rerun it.

### Write `convertf.py`

Create `src/aadrkit/convertf.py`:

```python
"""Extract genotypes for selected individuals by running EIGENSOFT's convertf.

This module is aadrkit's "convertf backend": it is the only part of the
package that reads AADR's genotype files. A different backend (for example,
a pure-Python .geno reader) could replace it by providing the same
extract_genotypes() function.
"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd

# Output file suffixes for each convertf output format.
OUTPUT_SUFFIXES = {
    "EIGENSTRAT": (".geno", ".snp", ".ind"),
    "PACKEDANCESTRYMAP": (".geno", ".snp", ".ind"),
    "PACKEDPED": (".bed", ".bim", ".fam"),    # PLINK binary format
}


def read_ind(path):
    """Read an EIGENSTRAT .ind file: one line per individual (ID, sex, population)."""
    return pd.read_csv(path, sep=r"\s+", header=None,
                       names=["genetic_id", "sex", "population"], dtype=str)


def write_selection_ind(ind, genetic_ids, path):
    """Write a copy of `ind` where everyone not in `genetic_ids` is labeled "Ignore".

    Every line is kept, in the original order, because convertf matches
    the .ind lines to the genotype file by position.
    """
    marked = ind.copy()
    marked.loc[~marked["genetic_id"].isin(genetic_ids), "population"] = "Ignore"
    marked.to_csv(path, sep=" ", header=False, index=False)
    return marked


def write_par(path, settings):
    """Write a convertf parameter file, one "name: value" line per setting."""
    lines = [f"{name}: {value}" for name, value in settings.items()]
    Path(path).write_text("\n".join(lines) + "\n")


def extract_genotypes(selected, geno, snp, ind, out_prefix, output_format="EIGENSTRAT"):
    """Write genotype files containing only the individuals in `selected`.

    `selected` is a table from select() or the filters (it needs a
    genetic_id column). `geno`, `snp` and `ind` are the AADR genotype files.
    Outputs are written as out_prefix + suffix. The modified .ind, the
    parameter file and convertf's log are kept next to them as a record of
    exactly how the files were made. Returns a dict of output paths.
    """
    if output_format not in OUTPUT_SUFFIXES:
        raise ValueError(f"output_format must be one of {sorted(OUTPUT_SUFFIXES)}, "
                         f"got {output_format!r}")
    if shutil.which("convertf") is None:
        raise RuntimeError("convertf not found; run `conda activate aadr-project` first")
    for path in (geno, snp, ind):
        if not Path(path).exists():
            raise FileNotFoundError(path)

    ids = set(selected["genetic_id"])
    if not ids:
        raise ValueError("No individuals selected")
    full_ind = read_ind(ind)
    missing = ids - set(full_ind["genetic_id"])
    if missing:
        raise ValueError(f"{len(missing)} selected IDs are not in {ind}, "
                         f"e.g. {sorted(missing)[:5]}")

    out_prefix = Path(out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    geno_suffix, snp_suffix, ind_suffix = OUTPUT_SUFFIXES[output_format]
    outputs = {
        "geno": f"{out_prefix}{geno_suffix}",
        "snp": f"{out_prefix}{snp_suffix}",
        "ind": f"{out_prefix}{ind_suffix}",
        "selection_ind": f"{out_prefix}_selection.ind",
        "par": f"{out_prefix}.par",
        "log": f"{out_prefix}.log",
    }

    write_selection_ind(full_ind, ids, outputs["selection_ind"])
    write_par(outputs["par"], {
        "genotypename": geno,
        "snpname": snp,
        "indivname": outputs["selection_ind"],
        "outputformat": output_format,
        "genotypeoutname": outputs["geno"],
        "snpoutname": outputs["snp"],
        "indivoutname": outputs["ind"],
        "hashcheck": "NO",
    })

    result = subprocess.run(["convertf", "-p", outputs["par"]],
                            capture_output=True, text=True)
    Path(outputs["log"]).write_text(result.stdout + result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"convertf failed (exit code {result.returncode}); "
                           f"see {outputs['log']}")

    with open(outputs["ind"]) as handle:
        n_out = sum(1 for _ in handle)
    if n_out != len(ids):
        raise RuntimeError(f"Expected {len(ids)} individuals in {outputs['ind']}, "
                           f"found {n_out}")
    return outputs
```

### How it works

**`OUTPUT_SUFFIXES`** maps each output format to its three file extensions. EIGENSTRAT and packed formats use `.geno/.snp/.ind`. PLINK's binary format, which `convertf` calls `PACKEDPED`, uses `.bed/.bim/.fam`. This is how `aadrkit` delivers the PLINK export promised in your problem statement, through one setting.

**`read_ind`** reads the `.ind` file:
- **`sep=r"\s+"`** means "one or more spaces or tabs between columns." It also ignores the leading padding you saw.
- **`header=None`** says the file has no header row, and `names=[...]` supplies column names.
- **`dtype=str`** keeps every value as text, so no ID is ever accidentally converted to a number.

**`write_selection_ind`** is your `awk` command, in pandas:
- **`marked.loc[~marked["genetic_id"].isin(genetic_ids), "population"] = "Ignore"`** means: in rows whose ID is **not** selected, set the population column to `Ignore`. `.loc[rows, column] = value` is pandas' way of changing specific cells.
- **The docstring repeats the key rule**: every line stays, in its original order, because `convertf` matches `.ind` lines to the genotype file by position.

**`write_par`** turns a dictionary of settings into the `name: value` lines you wrote by hand.
- **`"\n".join(lines)`** joins the lines with line breaks.
- **`Path(path).write_text(...)`** writes the text to a file in one step.

**`extract_genotypes`**, in order:

1. **It checks everything before running anything slow**, so mistakes fail in seconds, not after `convertf` has worked for a minute:
   - an unknown output format;
   - `convertf` not available. **`shutil.which("convertf")`** looks for the program the same way your terminal's `which` command does, and the error message tells the user exactly what to do;
   - any of the three input files missing;
   - an empty selection;
   - **selected IDs that aren't in the `.ind`.** This would mean the `.anno` and genotype files don't belong together, the matching-by-ID principle from Step 5 in code.
2. **It creates the output folder if needed:** `mkdir(parents=True, exist_ok=True)` creates any missing parent folders and doesn't complain if the folder already exists.
3. **It builds all the output paths** in one dictionary, so the function returns them all together.
4. **It writes the selection `.ind` and the parameter file**, using the same settings as your hand-written `convertf_test.par`.
5. **It runs `convertf`** with `subprocess.run`:
   - The command is a **list**, `["convertf", "-p", par_path]`: the program and each argument as separate items. That's safer than one long string, because a path containing spaces or special characters can't be misinterpreted.
   - **`capture_output=True`** collects what `convertf` prints instead of showing it on screen, and **`text=True`** returns it as text rather than raw bytes.
   - The output is **always saved to the log file**, whether it succeeded or not.
   - **`result.returncode`** is the program's exit code: 0 means success; anything else means it failed. On failure, the error message points to the log, where `convertf`'s own explanation will be.
6. **It checks the result**, the automated version of `cat test_out.ind`:
   - **`sum(1 for _ in handle)`** counts the lines in the output individual file by adding 1 for each line.
   - The count must equal the number selected. This catches a failure even if `convertf` happened to exit with code 0.

### Make it available from the package

Update `src/aadrkit/__init__.py`:

```python
"""aadrkit: filter and export subsets of the Allen Ancient DNA Resource (AADR)."""

from aadrkit.anno import list_values, load_anno
from aadrkit.convertf import extract_genotypes
from aadrkit.query import select

__version__ = "0.1.0"
```

### Tests, fast and slow

Running `convertf` on the full 6.7 GB file takes over a minute. You don't want to wait for that every time you run the tests, but you do want it tested. pytest handles this with **markers**: labels on tests that let you choose which ones to run.

### Register the marker

Add this to the bottom of `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = ["slow: runs convertf on the full genotype file (about 1-2 minutes)"]
```

Registering a marker tells pytest it's intentional, rather than a typo, and the description shows up in pytest's help output.

### Add a fixture for the genotype files

Add this to `tests/conftest.py`, below the other fixtures:

```python
@pytest.fixture(scope="session")
def genotype_files():
    """Paths to the AADR genotype files: (.geno, .snp, .ind)."""
    paths = tuple(
        ROOT / "data" / "raw" / f"v66.p1_1240K.aadr.patch.PUB.{ext}"
        for ext in ("geno", "snp", "ind")
    )
    if not all(p.exists() for p in paths):
        pytest.skip("AADR genotype files not found; see README 'Data' section")
    return paths
```

The filenames are built with an f-string rather than pathlib's `with_suffix`, because `with_suffix` would treat `.PUB` as the extension and replace it, a subtle bug with names that contain several dots.

### Write the tests

Create `tests/test_convertf.py`:

```python
import pandas as pd
import pytest

from aadrkit.convertf import extract_genotypes, read_ind, write_par, write_selection_ind


# --- Fast tests: no convertf needed ---

def test_selection_ind_keeps_every_line_in_order(tmp_path):
    ind = pd.DataFrame({"genetic_id": ["A", "B", "C"],
                        "sex": ["M", "F", "U"],
                        "population": ["P1", "P2", "P3"]})
    path = tmp_path / "selection.ind"
    write_selection_ind(ind, {"B"}, path)
    assert path.read_text().splitlines() == ["A M Ignore", "B F P2", "C U Ignore"]


def test_write_par(tmp_path):
    path = tmp_path / "test.par"
    write_par(path, {"genotypename": "in.geno", "hashcheck": "NO"})
    assert path.read_text() == "genotypename: in.geno\nhashcheck: NO\n"


def test_rejects_unknown_output_format(tmp_path):
    selected = pd.DataFrame({"genetic_id": ["A"]})
    with pytest.raises(ValueError):
        extract_genotypes(selected, "x.geno", "x.snp", "x.ind",
                          tmp_path / "out", output_format="VCF")


# --- Slow test: runs convertf on the real genotype file ---

@pytest.mark.slow
def test_extracts_correct_genotypes(genotype_files, ground_truth, tmp_path):
    """Repeats the manual check: called SNPs per person match .anno."""
    ids = ["VK202.AG", "NA20813.DG", "I13976.SG"]
    out = extract_genotypes(pd.DataFrame({"genetic_id": ids}), *genotype_files,
                            tmp_path / "test")

    out_ids = read_ind(out["ind"])["genetic_id"].tolist()
    assert sorted(out_ids) == sorted(ids)

    chrom = pd.read_csv(out["snp"], sep=r"\s+", header=None, usecols=[1])[1]
    geno = pd.read_csv(out["geno"], header=None, dtype=str)[0]
    autosomal = geno[chrom <= 22]
    expected = ground_truth.set_index("genetic_id")["snps_1240k"]
    for i, gid in enumerate(out_ids):
        called = (autosomal.str[i] != "9").sum()
        assert called == expected[gid], gid
```

### What the tests check

**`tmp_path`** is a fixture built into pytest: a fresh, empty temporary folder for each test. It's the answer to the question about where test outputs should go. They never touch your repo, and pytest cleans up old temporary folders automatically.

**The three fast tests** run in a fraction of a second:
- **The selection `.ind`:** only B keeps its real population, every line is still there, and the order hasn't changed. That's the rule `convertf` depends on.
- **The parameter file:** the exact text that gets written, line breaks included.
- **An unknown format** like `VCF` is rejected **before** anything else happens. That's why the fake file names `x.geno` and so on don't matter: the function never gets far enough to look for them.

**The slow test** is your validation, automated:
- **`@pytest.mark.slow`** applies the marker.
- **`*genotype_files`** unpacks the three paths into three separate arguments. `*` does for a list or tuple what `**` does for a dictionary.
- **It extracts the same three individuals as before**, then checks that exactly those three came out.
- **It recounts each person's non-missing autosomal genotypes,** the job your `paste | awk` command did:
  - **`usecols=[1]`** reads only the chromosome column of the `.snp`.
  - **`dtype=str` on the genotype file is essential.** Without it, pandas would read a line like `029` as the number 29, dropping the leading zero, and every person's genotype would shift by one position. That's another leading-zero bug avoided.
  - **`geno[chrom <= 22]`** keeps the autosomes.
  - **`autosomal.str[i]`** takes the *i*-th character of every line, which is person *i*'s genotype.
- **Each count must equal that person's `snps_1240k` value** from your hand-verified ground truth: 810,231, 1,101,664, and 281. **`, gid`** after the `assert` is a message: if it fails, pytest shows which individual's count was wrong.

### Run the tests

**Fast tests only**, for everyday use:

```bash
pytest -m "not slow"
```

**`-m "not slow"`** runs every test except those marked slow. You should see **59 passed, 1 deselected**: the previous 56 plus the 3 fast tests, with the slow test skipped on purpose.

**Everything**, including the slow test:

```bash
pytest -v
```

This takes a minute or two longer, while the slow test runs `convertf` on the full file. You should see **60 passed**.

### Try a real extraction, including PLINK

The slow test checks EIGENSTRAT output. Here's one quick manual check of the **PLINK** format, which no test covers yet. It writes to `data/output/`, which git ignores because it's inside `data/`:

```bash
python -c "import aadrkit; a = aadrkit.load_anno('data/raw/v66.p1_1240K.aadr.PUB.anno'); s, r = aadrkit.select(a, groups='Scotland_Viking'); g = 'data/raw/v66.p1_1240K.aadr.patch.PUB'; print(aadrkit.extract_genotypes(s, g + '.geno', g + '.snp', g + '.ind', 'data/output/scotland_viking', output_format='PACKEDPED'))"
```

Then compare the number of individuals:

```bash
wc -l data/output/scotland_viking.fam
```

The count should equal the "Selected N rows" that `select` printed.

```bash
head -n 3 data/output/scotland_viking.fam
```

This shows how `convertf` lays out a PLINK `.fam` file. Paste those three lines; we'll check the individual IDs are where PLINK expects them, and if so, add a fast test for the PLINK path.

### Commit

```bash
git add src/aadrkit/convertf.py src/aadrkit/__init__.py pyproject.toml tests/conftest.py tests/test_convertf.py
```

```bash
git commit -m "Add convertf backend: extract genotypes for a selection, with tests"
```

Paste both `pytest` summaries and the `.fam` output.
- **What I asked next (verbatim):** "There was an error that occurred do to the spaces in my file path. I inspected the log file and it showed me so. I copy and pasted that into Claude and it helped me fix this: 
```
parameter file: /tmp/pytest-of-nelin/pytest-2/test_extracts_correct_genotype0/test.par
genotypename: /mnt/c/Users/nelin/Desktop/GWU Information/GWU Fall 2026/Applied_Computing/project-hds/data/raw/v66.p1_1240K.aadr.patch.PUB.geno
snpname: /mnt/c/Users/nelin/Desktop/GWU Information/GWU Fall 2026/Applied_Computing/project-hds/data/raw/v66.p1_1240K.aadr.patch.PUB.snp
indivname: /tmp/pytest-of-nelin/pytest-2/test_extracts_correct_genotype0/test_selection.ind
outputformat: EIGENSTRAT
genotypeoutname: /tmp/pytest-of-nelin/pytest-2/test_extracts_correct_genotype0/test.geno
snpoutname: /tmp/pytest-of-nelin/pytest-2/test_extracts_correct_genotype0/test.snp
indivoutname: /tmp/pytest-of-nelin/pytest-2/test_extracts_correct_genotype0/test.ind
hashcheck: NO
## convertf version: 8640
bad open /mnt/c/Users/nelin/Desktop/GWU
fatalx:
(openit) can't open file /mnt/c/Users/nelin/Desktop/GWU of type r
 error info: No such file or directory
 ```
 "
- **Exact output (verbatim):**
### The likely cause: spaces in the path

Look at the path in the error message:

```
/mnt/c/Users/nelin/Desktop/GWU Information/GWU Fall 2026/Applied_Computing/...
```

This is `Nicole-ASUS`, where the repo is still in a folder with **spaces** in its name. The parameter file now contains full paths like `genotypename: /mnt/c/Users/nelin/Desktop/GWU Information/...`. If `convertf` splits each line at spaces, as many older command-line programs do, it reads the path as just `/mnt/c/Users/nelin/Desktop/GWU`, a file that doesn't exist.

The log mentions a path that **stops at `GWU`** (or a "cannot open" or "file not found" message for a shortened path).

### Step 1: Make the tool fail clearly instead

Even after fixing your own setup, `aadrkit` should never hand `convertf` a path it can't handle and then report a cryptic "exit code −6." It should catch the problem **before** running and explain it.

In `src/aadrkit/convertf.py`, inside `extract_genotypes`, add this check **right after the output-format check**, before the `shutil.which` line:

```python
    for path in (geno, snp, ind, out_prefix):
        if any(ch.isspace() for ch in str(path)):
            raise ValueError(f"convertf cannot handle paths containing spaces: {path}. "
                             f"Move the files (or the project) to a folder without spaces.")
```

- **`str(path)`** turns a `Path` into text, so its characters can be checked.
- **`any(ch.isspace() for ch in ...)`** is true if any character is a space, tab, or other whitespace.
- **It goes before the `convertf` and file-existence checks**, so a path with spaces gets *this* clear message rather than a "file not found" error. It also means the check works even on a computer without `convertf`, which makes it easy to test.

Then add a fast test to `tests/test_convertf.py`, after `test_rejects_unknown_output_format`:

```python
def test_rejects_paths_with_spaces(tmp_path):
    selected = pd.DataFrame({"genetic_id": ["A"]})
    with pytest.raises(ValueError, match="spaces"):
        extract_genotypes(selected, "my data/x.geno", "x.snp", "x.ind", tmp_path / "out")
```

**`match="spaces"`** checks that the error is the *right* error with the helpful message, not some other `ValueError`.

### Step 2: Move the repo on this computer

On `Nicole-PC`, you already moved the repo to `/mnt/c/Users/nelin/projects/project-hds`, with no spaces. Doing the same here fixes the problem and makes the two computers match.

**a.** Close VS Code windows that have the project open.

**b.** Create the folder, if it doesn't exist on this computer yet:

```bash
mkdir -p /mnt/c/Users/nelin/projects
```

**c.** Move the repo:

```bash
mv "/mnt/c/Users/nelin/Desktop/GWU Information/GWU Fall 2026/Applied_Computing/project-hds" /mnt/c/Users/nelin/projects/
```

**d.** Go there:

```bash
cd /mnt/c/Users/nelin/projects/project-hds
```

**e. Reinstall the package in editable mode.** This step matters: as we discussed with OneDrive, `pip install -e .` recorded the *old* location of `src/aadrkit`, so imports would fail or point to a folder that no longer exists:

```bash
pip install -e .
```

**f.** Confirm the package now points to the new location:

```bash
python -c "import aadrkit; print(aadrkit.__file__)"
```

The path should start with `/mnt/c/Users/nelin/projects/project-hds`.

### Step 3: Run everything

```bash
pytest -v
```

You should see **61 passed**: the 59 from before, the new spaces test, and the slow `convertf` test, which should now pass. Expect it to take a minute or two longer than the fast tests, since that's `convertf` reading the full file.

Then add one line to the README's Setup section, such as *"Keep the project in a folder whose path has no spaces; EIGENSOFT's `convertf` cannot read paths that contain spaces."*, and commit:

```bash
git add src/aadrkit/convertf.py tests/test_convertf.py README.md
```

```bash
git commit -m "Reject paths with spaces before running convertf; document requirement"
```
- **Verificaiton:** I read through and thought about each point that Claude wrote on how to construct this. I decided whether it made sense or was unnesseary. I then typed out the code and ran the tests. I inspected all results myself. I followed all instructions to fix the error about the file path with spaces in it. All 61 tests passed once the fixes were applied.

## Entry 15:
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Running a full extraction with PLINK format.
- **What I asked (verbatim):** "Now that EIGENSTRAT output is confirmed, to answer the promise in my statement, I need you to help walk me through a full extraction in PLINK format as I have never used this before either. 
- **Exact output (verbatim):**
The slow test checks EIGENSTRAT output. PLINK output (`PACKEDPED`) is the other format promised in your problem statement, and nothing has checked it yet. This runs a complete, realistic query: select the Scottish Vikings, then extract their genotypes in PLINK format.

From the repo root, with `(aadr-project)` active:

```bash
python -c "import aadrkit; a = aadrkit.load_anno('data/raw/v66.p1_1240K.aadr.PUB.anno'); s, r = aadrkit.select(a, groups='Scotland_Viking'); g = 'data/raw/v66.p1_1240K.aadr.patch.PUB'; print(aadrkit.extract_genotypes(s, g + '.geno', g + '.snp', g + '.ind', 'data/output/scotland_viking', output_format='PACKEDPED'))"
```

What happens, in order:

1. **`load_anno`** reads the metadata.
2. **`select`** filters to `Scotland_Viking`, excluding outliers and deduplicating, and prints its report, ending with "Selected N rows."
3. **`extract_genotypes`** runs `convertf` with `PACKEDPED` output. It takes about a minute.
4. **`print(...)`** shows the dictionary of output paths: `.bed`, `.bim`, `.fam`, plus the selection `.ind`, `.par`, and `.log` record files.

The outputs go in `data/output/`, which git ignores because it's inside `data/`.

### Check the three PLINK files

PLINK's binary format has three files:

- **`.bed`**: the genotypes, in binary, so it can't be read directly.
- **`.bim`**: one line per SNP.
- **`.fam`**: one line per individual.

**1. The number of individuals:**

```bash
wc -l data/output/scotland_viking.fam
```

It should equal the "Selected N rows" that `select` printed. `extract_genotypes` already checks this count itself, so a mismatch would have raised an error, but it's good to see it with your own eyes.

**2. The individual layout:**

```bash
head -n 3 data/output/scotland_viking.fam
```

A PLINK `.fam` file has **six columns**: family ID, individual ID, father, mother, sex, and phenotype. The part to check is **which column holds the Genetic ID** (like `VK202.AG`). PLINK identifies people by the family ID and individual ID together, so the Genetic ID needs to be in a predictable place for anyone linking PLINK results back to the AADR metadata. I'm not certain how `convertf` fills the family ID column. It might copy the individual ID, or use the population label. The output will show us.

**3. The SNP layout:**

```bash
head -n 3 data/output/scotland_viking.bim
```

A `.bim` file has six columns: chromosome, SNP ID, genetic position, physical position, and the two alleles. You should recognize the first SNPs from the `.snp` file in Step 5, such as `rs3094315` on chromosome 1 at position 752566.

Paste all three outputs, plus the report table `select` printed. Once we know where the Genetic ID sits in the `.fam`, we'll add a slow test for the PLINK path, so both output formats are covered.
- **What I asked next (verbatim):** I pasted the output of all commands which ran successfully.
```bash
10:50:39 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→ python -c "import aadrkit; a = aadrkit.load_anno('data/raw/v66.
p1_1240K.aadr.PUB.anno'); s, r = aadrkit.select(a, groups='Scotland_Viking'); g = 'data/raw/v66.p1_1240K.aadr.patch.PUB'; print(aadrkit.extract_genotypes(s, g + '.geno', g + '.snp', g + '.ind', 'data/output/scotland_viking', output_format='PACKEDPED'))"
                     Step  Rows_before  Rows_after  Removed                Note
Exclude Reference Genomes        23089       23085        4     
    Group Scotland_Viking        23085           7    23078 3 outliers excluded
       One row per person            7           6        1     
Selected 6 rows.
{'geno': 'data/output/scotland_viking.bed', 'snp': 'data/output/scotland_viking.bim', 'ind': 'data/output/scotland_viking.fam', 'selection_ind': 'data/output/scotland_viking_selection.ind', 'par': 'data/output/scotland_viking.par', 'log': 'data/output/scotland_viking.log'}
10:54:42 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→ wc -l data/output/scotland_viking.fam
6 data/output/scotland_viking.fam
10:55:19 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→ head -n 3 data/output/scotland_viking.fam
     1       VK202.AG 0 0 1 2
     2       VK203.SG 0 0 1 2
     3       VK204.SG 0 0 1 2
10:55:24 (aadr-project) nelin@Nicole-ASUS project-hds ±|main ✗|→ head -n 3 data/output/scotland_viking.bim
1     rs3094315     0.020130       752566 G A
1    rs12124819     0.020242       776546 A G
1    rs28765502     0.022137       832918 T C
```
- **Exact output (verbatim):**
This is a complete, end-to-end run of the tool: from a population name to PLINK genotype files in one command. Here's what each piece shows.

### The `select` report

- **Population step:** 7 Scottish Vikings matched, and **3 outliers were excluded**. VK201 is one of them; there are two more you hadn't met. Those three would be in the data if you'd used a simple "contains Viking" search.
- **Deduplication:** 7 rows became **6 people**, so one Scottish Viking had two datasets.

### The `.fam` file

```
     1       VK202.AG 0 0 1 2
```

| Column | Value | Meaning |
|---|---|---|
| 1. Family ID | `1`, `2`, `3` | `convertf` numbers individuals in order; this is **not** the population label |
| 2. Individual ID | `VK202.AG` | **The Genetic ID**, which links back to AADR's metadata |
| 3–4. Father, mother | `0 0` | Unknown (no family relationships recorded) |
| 5. Sex | `1` | PLINK's code for male (2 = female, 0 = unknown). VK202 is `M` in the `.ind`, so this is correct |
| 6. Phenotype | `2` | Set by `convertf`. Not meaningful here; see below |

**Two things for your documentation:**

- **The Genetic ID is in column 2**, and the family ID is just a running number. Anyone linking PLINK results back to the metadata should match on column 2. Many PLINK commands identify people by family ID plus individual ID together, so users need to know the family ID is a sequence number, not a population.
- **The phenotype column isn't a real trait.** In PLINK, phenotype `2` often means "case" in a case/control study. `convertf` appears to fill in a placeholder, and nobody should read it as meaningful. Confirm it's the same for all six:

```bash
awk '{print $6}' data/output/scotland_viking.fam | sort | uniq -c
```

This prints each distinct phenotype value with its count. If you see only `6 2`, every row has the same placeholder.

### The `.bim` file

```
1     rs3094315     0.020130       752566 G A
```

It has the same SNPs as the `.snp` file from earlier (`rs3094315` on chromosome 1 at position 752566, alleles G and A) in PLINK's column order. The SNP information came through unchanged.

### A slow test for the PLINK format

The EIGENSTRAT test checks genotype values directly, by reading the text `.geno`. The PLINK `.bed` file is binary, so reading it would need either PLINK itself or a decoder. Instead, this test checks three things it *can* verify reliably:

1. **The Genetic IDs are in column 2** of the `.fam`.
2. **Sex is translated correctly** from the `.ind` (M → 1, F → 2). You saw these values: VK202 is male, NA20813 and I13976 are female.
3. **The `.bed` file is exactly the right size.** In PLINK's standard layout, a `.bed` file is a 3-byte header, then one block per SNP. Each genotype takes 2 bits, so 4 people fit in one byte, and every SNP takes `ceil(people ÷ 4)` bytes. For 3 people and 1,233,013 SNPs, that's 1 byte per SNP, so the file must be exactly **3 + 1,233,013 = 1,233,016 bytes**. If any SNPs were missing, or people were added or lost, the size would be wrong.

If `convertf` used PLINK's older "individual-major" layout instead, the size would come out differently and this test would fail, telling us so.

Add `from pathlib import Path` to the imports at the top of `tests/test_convertf.py`, then add this at the bottom:

```python
@pytest.mark.slow
def test_extracts_plink_files(genotype_files, tmp_path):
    """PLINK output: Genetic IDs in .fam column 2, sex coded 1/2, .bed has the right size."""
    ids = ["VK202.AG", "NA20813.DG", "I13976.SG"]
    out = extract_genotypes(pd.DataFrame({"genetic_id": ids}), *genotype_files,
                            tmp_path / "test", output_format="PACKEDPED")

    fam = pd.read_csv(out["ind"], sep=r"\s+", header=None, dtype=str)
    sex = dict(zip(fam[1], fam[4]))
    assert sex == {"VK202.AG": "1", "NA20813.DG": "2", "I13976.SG": "2"}

    with open(out["snp"]) as handle:
        n_snps = sum(1 for _ in handle)
    assert n_snps == 1233013

    bytes_per_snp = (len(ids) + 3) // 4
    assert Path(out["geno"]).stat().st_size == 3 + n_snps * bytes_per_snp
```

### How it works

- **`output_format="PACKEDPED"`** requests PLINK output. The returned dictionary still uses the keys `"geno"`, `"snp"`, and `"ind"`, but they now point to `.bed`, `.bim`, and `.fam`. That's why `out["ind"]` is the `.fam` file here.
- **`fam[1]` and `fam[4]`** are the second and fifth columns, the Genetic ID and sex code. Remember that pandas counts from 0.
- **`dict(zip(fam[1], fam[4]))`** pairs each ID with its sex code. `zip` walks two columns side by side, and `dict` turns the pairs into a lookup table. Comparing whole dictionaries checks every person's sex in one assertion, regardless of row order.
- **The `.bim` line count** must be the full 1,233,013 SNPs, the same number `convertf` reported in Step 5.
- **`(len(ids) + 3) // 4`** is the "round up" division: `//` divides and drops the remainder, so adding 3 first rounds up. 3 people gives 1 byte per SNP; 5 people would give 2.
- **`Path(...).stat().st_size`** is the file's size in bytes, the Python version of `ls -l`.

### Run, document, commit

```bash
pytest -v
```

You should see **62 passed**, with the two slow tests taking a few minutes together. For everyday runs, `pytest -m "not slow"` still skips them.

Remember to add a short **Output formats** section to the README. 

Then commit:

```bash
git add tests/test_convertf.py README.md
```

```bash
git commit -m "Add slow test for PLINK output; document output formats"
```

Paste the phenotype check and the `pytest -v` summary. 
- **Verificaiton:** I ran all commands, all ran successfully. The 6 rows selected matched the lines in the `wc -l` command. Then in the final PLINK test, all 62 passed. A section about output formats was added to the README.

## Entry 16
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Converting aadrkit to CLI.
- **What I asked (verbatim):** "Now that the core tool works, I need to add a CLI so users can use it without needing to write Python code using "aadrkit - command" or however it would be formatted. I have never developed something like this before so I need help. However I want the following functionality: (1) every option maps directly onto a select() argument, (2) every saved run produces a full record, (3) the terminal part is kept separate from the main code logic. Can you explain how the script or instructions will work? Will I need to add to other existing scripts? I also need test scripts written to see if this CLI will actually run. I want to see how it would work if researchers actually were using it." 
- **Exact output (verbatim):**
The core tool works end to end and is fully tested. The last piece is a **command-line interface (CLI)**, so `aadrkit` can be used from the terminal by someone who doesn't write Python.

### The command-line interface

When this step is done, a user will be able to type commands like:

```bash
aadrkit list country
aadrkit select --group Scotland_Viking --out data/output/vikings --genotypes --format plink
```

The CLI will have two **subcommands**, like `git add` and `git commit` are subcommands of `git`:

- **`aadrkit list COLUMN`** shows every value in a column with its count, `list_values()` from the terminal. It's how a user discovers exact labels before filtering.
- **`aadrkit select ...`** runs `select()` with options given as flags, and optionally saves the results and extracts genotypes.

### Design decisions

**Use `argparse`, Python's built-in tool for reading command-line options.** It's part of the standard library, so there's no new dependency to install and pin.

**Every option maps directly onto a `select()` argument,** with only small spelling changes for the terminal. Command-line flags conventionally use hyphens (`--min-bp`), while Python uses underscores (`min_bp`).

**Every saved run produces a full record.** With `--out PREFIX`, the command writes:

- **`PREFIX_selected.tsv`**: the selected individuals and their metadata, including publications and DOIs.
- **`PREFIX_report.tsv`**: the step-by-step report.
- **`PREFIX_command.txt`**: the exact command that was run, plus the `aadrkit` version.

So a folder of outputs always explains itself: what was selected, what each filter removed, and how to rerun it. With `--genotypes`, the `convertf` outputs and their own records are added alongside.

**The terminal handling is kept separate from the logic.** `main()` reads the command line and loads the file. Two separate functions, `run_list` and `run_select`, do the actual work on an already-loaded table. That way, the tests can call `run_select` directly with your session's `anno` fixture, instead of reloading the 13 MB file (about 18 seconds) for every test.

### Write `cli.py`

Create `src/aadrkit/cli.py`:

```python
"""Command-line interface: run aadrkit from the terminal.

Examples, run from the repository root:
    aadrkit list country
    aadrkit select --group Scotland_Viking --out data/output/vikings
    aadrkit select --min-bp 3000 --max-bp 5000 --country Spain --min-snps 100000 \\
        --out data/output/spain --genotypes --format plink
"""
import argparse
import shlex
import sys
from pathlib import Path

from aadrkit import __version__
from aadrkit.anno import list_values, load_anno
from aadrkit.convertf import extract_genotypes
from aadrkit.query import select

DEFAULT_ANNO = "data/raw/v66.p1_1240K.aadr.PUB.anno"
DEFAULT_GENO_PREFIX = "data/raw/v66.p1_1240K.aadr.patch.PUB"
FORMATS = {"eigenstrat": "EIGENSTRAT", "plink": "PACKEDPED"}


def build_parser():
    """Describe every command-line option."""
    parser = argparse.ArgumentParser(
        prog="aadrkit",
        description="Filter and export subsets of the Allen Ancient DNA Resource (AADR).",
    )
    parser.add_argument("--anno", default=DEFAULT_ANNO,
                        help=f"AADR .anno file (default: {DEFAULT_ANNO})")
    sub = parser.add_subparsers(dest="command", required=True)

    lst = sub.add_parser("list", help="show every value in a column, with counts")
    lst.add_argument("column", help="column name, e.g. country, group_id, assessment")

    sel = sub.add_parser("select", help="select individuals; optionally save and extract genotypes")
    sel.add_argument("--min-bp", type=int, help="minimum mean date, in years before 1950 CE")
    sel.add_argument("--max-bp", type=int, help="maximum mean date, in years before 1950 CE")
    sel.add_argument("--exclude-present", action="store_true",
                     help="remove present-day individuals (dated 0 BP)")
    sel.add_argument("--country", action="append",
                     help="country label (repeat for several); see 'aadrkit list country'")
    sel.add_argument("--min-lat", type=float, help="southern edge of a latitude/longitude box")
    sel.add_argument("--max-lat", type=float, help="northern edge")
    sel.add_argument("--min-lon", type=float, help="western edge")
    sel.add_argument("--max-lon", type=float, help="eastern edge (smaller than --min-lon "
                                                   "means the box crosses 180 degrees)")
    sel.add_argument("--group", action="append",
                     help="population base name (repeat for several); see 'aadrkit list group_id'")
    sel.add_argument("--group-regex", action="store_true",
                     help="treat --group values as regular expressions")
    sel.add_argument("--include-outliers", action="store_true",
                     help="keep population-genetic outliers ('-o' groups)")
    sel.add_argument("--min-snps", type=int, help="minimum SNPs covered on the 1240K panel")
    sel.add_argument("--include-references", action="store_true",
                     help="keep reference genomes (Chimp, Gorilla, ...)")
    sel.add_argument("--keep-duplicates", action="store_true",
                     help="keep every dataset per person instead of the best one")
    sel.add_argument("--out", help="output prefix; writes <out>_selected.tsv, "
                                   "<out>_report.tsv and <out>_command.txt")
    sel.add_argument("--genotypes", action="store_true",
                     help="also extract genotypes with convertf (requires --out)")
    sel.add_argument("--geno-prefix", default=DEFAULT_GENO_PREFIX,
                     help=f"prefix of the AADR .geno/.snp/.ind files (default: {DEFAULT_GENO_PREFIX})")
    sel.add_argument("--format", choices=sorted(FORMATS), default="eigenstrat",
                     help="genotype output format (default: eigenstrat)")
    sel.add_argument("--quiet", action="store_true", help="don't print the report")
    return parser


def run_list(args, anno):
    """`aadrkit list COLUMN`: print each value in a column with its count."""
    if args.column not in anno.columns:
        raise SystemExit(f"Unknown column {args.column!r}; choose from: {', '.join(anno.columns)}")
    print(list_values(anno, args.column).to_string())


def run_select(args, anno, command_line=""):
    """`aadrkit select ...`: run select() and save outputs if --out is given."""
    if args.genotypes and not args.out:
        raise SystemExit("--genotypes requires --out")

    selected, report = select(
        anno,
        min_bp=args.min_bp, max_bp=args.max_bp, exclude_present=args.exclude_present,
        countries=args.country,
        min_lat=args.min_lat, max_lat=args.max_lat, min_lon=args.min_lon, max_lon=args.max_lon,
        groups=args.group, group_regex=args.group_regex, include_outliers=args.include_outliers,
        min_snps=args.min_snps, include_references=args.include_references,
        deduplicate=not args.keep_duplicates, verbose=not args.quiet,
    )
    if not args.out:
        return {}

    prefix = Path(args.out)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    outputs = {
        "selected": f"{prefix}_selected.tsv",
        "report": f"{prefix}_report.tsv",
        "command": f"{prefix}_command.txt",
    }
    selected.to_csv(outputs["selected"], sep="\t", index=False)
    report.to_csv(outputs["report"], sep="\t", index=False)
    Path(outputs["command"]).write_text(f"# aadrkit {__version__}\n{command_line}\n")

    if args.genotypes:
        g = args.geno_prefix
        outputs.update(extract_genotypes(selected, f"{g}.geno", f"{g}.snp", f"{g}.ind",
                                         prefix, output_format=FORMATS[args.format]))
    if not args.quiet:
        for name, path in outputs.items():
            print(f"{name}: {path}")
    return outputs


def main(argv=None):
    """Entry point for the `aadrkit` command."""
    if argv is None:
        argv = sys.argv[1:]
    args = build_parser().parse_args(argv)
    if not Path(args.anno).exists():
        raise SystemExit(f"AADR .anno file not found: {args.anno} (see README 'Data' section)")
    anno = load_anno(args.anno)
    if args.command == "list":
        run_list(args, anno)
    else:
        run_select(args, anno, command_line=shlex.join(["aadrkit", *argv]))


if __name__ == "__main__":
    main()
```

### How `build_parser` works

`argparse` builds a **parser**: a description of every option the command accepts. It then reads the command line, checks it, and produces an object holding the values.

- **`ArgumentParser(prog=..., description=...)`** creates the main parser. The description appears in `aadrkit --help`.
- **`--anno` belongs to the main parser**, so it applies to both subcommands. Because of that, it goes **before** the subcommand name: `aadrkit --anno other.anno list country`.
- **`add_subparsers(dest="command", required=True)`** sets up subcommands. The chosen name (`list` or `select`) is stored in `args.command`, and `required=True` means a bare `aadrkit` with no subcommand is an error.
- **`add_argument` options:**
  - **`type=int` / `type=float`** converts the typed text into a number and rejects anything that isn't one. `--min-bp abc` gives a clear error.
  - **`action="store_true"`** creates an on/off switch. The flag takes no value; it's `True` if present and `False` if absent.
  - **`action="append"`** allows a flag to be repeated, collecting the values into a list: `--country Spain --country Portugal` becomes `["Spain", "Portugal"]`. That list goes straight into `select(countries=...)`, which already accepts lists.
  - **`choices=[...]`** restricts a value to fixed options. `--format vcf` is rejected with a message listing the valid ones.
  - **`default=...`** is used when the flag isn't given. The two path defaults match your repo's layout, so commands run from the repo root work without typing the long file names.
  - **`help=...`** is the description shown by `--help`. This is documentation that lives right next to the code it describes.
- **Hyphens become underscores automatically:** `--min-bp` is read back as `args.min_bp`.
- **Negative numbers work as values:** `--min-lon -170` is understood as the number −170, not a new flag.

### How the other functions work

**`run_list`** checks the column name, then prints `list_values`.
- **`raise SystemExit("message")`** is the standard way for a command-line program to stop with an error. It prints the message and exits with a failure code, without the long traceback a Python error would show. Tracebacks help programmers; a terminal user just needs to know what to fix.

**`run_select`:**
1. Rejects `--genotypes` without `--out`, before doing any work, since there would be nowhere to write the files.
2. Calls `select()` with each flag passed to the matching argument. `deduplicate=not args.keep_duplicates` turns the "keep duplicates" switch into `select`'s "deduplicate" option. `verbose=not args.quiet` does the same for printing.
3. Without `--out`, it stops after printing the report. That's useful for quick exploration ("how many would this select?").
4. With `--out`, it writes the three record files. `to_csv(..., sep="\t", index=False)` writes tab-separated files without pandas' row numbers.
5. With `--genotypes`, it calls `extract_genotypes`, translating the friendly format names (`eigenstrat`, `plink`) into `convertf`'s names. **`outputs.update(...)`** adds the genotype file paths to the same dictionary.
6. It lists every file it wrote.

**`main`** ties it together:
- **`argv=None`**: when run from the terminal, it reads the real command line, `sys.argv[1:]` (everything after the program name). Tests can pass their own list instead.
- **It checks the `.anno` file exists**, giving a friendly message rather than a traceback.
- **`shlex.join(["aadrkit", *argv])`** rebuilds the exact command as one line of text, adding quotes wherever needed. For example, a group name containing a space would be quoted, so the recorded command can be copied and rerun exactly. `*argv` spreads the list of arguments into the new list.
- **`if __name__ == "__main__": main()`** lets the file also be run as `python -m aadrkit.cli`. `__name__` equals `"__main__"` only when the file is run directly, not when it's imported.

### Register the `aadrkit` command

In `pyproject.toml`, add this section **directly after the `[project]` section**, before `[tool.setuptools.packages.find]`:

```toml
[project.scripts]
aadrkit = "aadrkit.cli:main"
```

This tells pip: "create a terminal command named `aadrkit` that runs the `main` function in `aadrkit/cli.py`." It's how `pytest` and `pip` themselves become commands.

pip only creates commands during installation, so reinstall:

```bash
pip install -e .
```

Then check it worked:

```bash
aadrkit --help
```

```bash
aadrkit select --help
```

The second shows every `select` option with its help text. That's the `help=` strings you wrote, formatted automatically.

### Write the tests

Create `tests/test_cli.py`:

```python
import pandas as pd
import pytest

from aadrkit.cli import build_parser, run_list, run_select


def parse(*argv):
    """Parse a command line the way the terminal would."""
    return build_parser().parse_args(list(argv))


# --- Parsing: no data needed ---

def test_parser_maps_options():
    args = parse("select", "--min-bp", "1000", "--country", "Spain", "--country", "Portugal",
                 "--group", "Poland_IA", "--min-lon", "-170", "--format", "plink")
    assert args.min_bp == 1000
    assert args.country == ["Spain", "Portugal"]
    assert args.group == ["Poland_IA"]
    assert args.min_lon == -170.0
    assert args.format == "plink"


def test_parser_rejects_unknown_format():
    with pytest.raises(SystemExit):
        parse("select", "--format", "vcf")


# --- Running commands on the real data ---

def test_genotypes_require_out(anno):
    with pytest.raises(SystemExit):
        run_select(parse("select", "--genotypes", "--quiet"), anno)


def test_select_writes_outputs(anno, tmp_path):
    args = parse("select", "--group", "Scotland_Viking", "--out", str(tmp_path / "vik"), "--quiet")
    outputs = run_select(args, anno, command_line="aadrkit select --group Scotland_Viking")

    selected = pd.read_csv(outputs["selected"], sep="\t")
    ids = set(selected["genetic_id"])
    assert len(selected) == 6
    assert "VK202.AG" in ids and "VK201.AG" not in ids

    report = pd.read_csv(outputs["report"], sep="\t")
    assert len(report) == 3          # reference genomes, group, one row per person

    assert "Scotland_Viking" in open(outputs["command"]).read()


def test_list_prints_values(anno, capsys):
    run_list(parse("list", "country"), anno)
    printed = capsys.readouterr().out
    assert "Spain" in printed and "802" in printed


def test_list_rejects_unknown_column(anno):
    with pytest.raises(SystemExit):
        run_list(parse("list", "planet"), anno)
```

### What the tests check

**`parse(*argv)`** is a small helper that turns `parse("select", "--min-bp", "1000")` into what the terminal would produce from `aadrkit select --min-bp 1000`. Each word of the command is a separate string, exactly as the terminal splits them.

**Parsing tests** (instant, no data):
- **Option mapping:** the date becomes a number, the repeated `--country` becomes a list, `-170` is read as a negative number rather than a flag, and the format is stored.
- **An invalid format** is rejected. `argparse` reports errors by raising `SystemExit`, which is why the test expects that rather than `ValueError`.

**Command tests** use the session `anno` fixture, so the file isn't reloaded:
- **`--genotypes` without `--out`** stops with a clear message.
- **A full saved run** uses the same query you ran by hand. The saved table must have **6** people, matching that run, with VK202 included and the outlier VK201 excluded. The report must have **3** steps, and the command file must record what was run. Counting the report's rows, rather than reading specific column names, keeps this test working with the column labels you've chosen.
- **`capsys`** is another built-in pytest fixture. It **captures everything printed** during the test, and `capsys.readouterr().out` returns it as text. That's how the test checks that `list country` printed "Spain" with its count of 802, the number you've now confirmed three different ways.
- **An unknown column** stops with a message listing the valid columns.

### Check, run, and try it

```bash
pytest --collect-only -q | tail -n 3
```

You should see **68 tests collected**: the previous 62 plus 6.

```bash
pytest -m "not slow"
```

Then use the tool the way a researcher would:

```bash
aadrkit list country | head -n 10
```

This shows the ten countries with the most individuals. `| head -n 10` keeps the output short.

```bash
aadrkit select --min-bp 1000 --max-bp 1500 --country "United Kingdom" --min-snps 100000
```

This is the same query as your earlier example, now from the terminal. The report should again end with **208**. The quotes keep "United Kingdom" together as one value; without them, the terminal would split it into two words.

```bash
aadrkit select --group Scotland_Viking --out data/output/vikings_cli --genotypes --format plink
```

This is the full workflow in one command: select, save the record files, and extract PLINK genotypes.

```bash
ls data/output/vikings_cli*
```

You should see the three record files (`_selected.tsv`, `_report.tsv`, `_command.txt`) plus the PLINK files and their records (`.bed`, `.bim`, `.fam`, `_selection.ind`, `.par`, `.log`).

```bash
cat data/output/vikings_cli_command.txt
```

This shows the version and the exact command, ready to be copied and rerun.

### Commit

```bash
git add src/aadrkit/cli.py pyproject.toml tests/test_cli.py
```

```bash
git commit -m "Add aadrkit command-line interface with list and select subcommands"
```

Paste the `pytest` summary and the output of the Scottish Viking command.
- **Verificaiton:** Upon testing: 68 tests were collected, 66 passed and 2 were deselected (slow runs), it correctly showed the 10 countries with the most individuals with `aadrkit list country | head -n 10`, correctly printed the same output from earlier from `aadrkit select --min-bp 1000 --max-bp 1500 --country "United Kingdom" --min-snps 100000` with 208 rows after and United Kingdowm kept as one value, the entire workflow passed producing the correct select search, record files, and extracted PLINK genotypes with `aadrkit select --group Scotland_Viking --out data/output/vikings_cli --genotypes --format plink`: 
```bash
 --genotypes --format plink
                     Step  Rows_before  Rows_after  Removed                Note
Exclude Reference Genomes        23089       23085        4
Group ['Scotland_Viking']        23085           7    23078 3 outliers excluded
       One row per person            7           6        1
Selected 6 rows.
selected: data/output/vikings_cli_selected.tsv
report: data/output/vikings_cli_report.tsv
command: data/output/vikings_cli_command.txt
geno: data/output/vikings_cli.bed
snp: data/output/vikings_cli.bim
ind: data/output/vikings_cli.fam
selection_ind: data/output/vikings_cli_selection.ind
par: data/output/vikings_cli.par
log: data/output/vikings_cli.log
```
, and finally produced the exact command written down and version of aadrkit ready to be copied. 
I caught a few coding errors (typos and indentations of my own fault) along the way and repaired and investigated as necessary. The tool is now fully functional.

## Entry 17
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Fixing Dockerfile.
- **What I asked (verbatim):** "I am still unfamiliar with Dockerfile, this is the current one I had as part of my Lab 1 from this course, how do I update it to work for aadrkit? (Pasted: 
FROM condaforge/miniforge3:latest
WORKDIR /workspace
COPY environment.yml .
RUN mamba env create -f environment.yml && mamba clean -afy
COPY scripts/ scripts/
SHELL ["conda", "run", "-n", "aadr-project", "/bin/bash", "-c"]
CMD ["conda", "run", "--no-capture-output", "-n", "aadr-project", "python", "--version"]
)
- **Exact output (verbatim):**
Your Dockerfile was written for Lab 1, before `aadrkit` existed, so it needs a few changes. One of them would make the build fail outright.

### What needs to change, and why

**1. The build would fail.** Your `environment.yml` now ends with `pip: - -e .`, which installs `aadrkit` from `pyproject.toml` and `src/`. But the Dockerfile only copies `environment.yml` before creating the environment, so pip would find nothing to install. The package files must be copied in **first**.

**2. It runs `python --version`.** That was the Lab 1 smoke test. The container should run `aadrkit` itself.

**3. Docker would try to send your 6.8 GB of data to the build.** When you run `docker build .`, Docker first packages up the **whole folder** (the "build context") and sends it to the Docker engine, even files the Dockerfile never copies. That includes `data/`. A **`.dockerignore`** file excludes them, the same way `.gitignore` works for git.

**4. The `SHELL` line does nothing.** `SHELL` only affects `RUN` lines that come after it, and there are none. It can go.

**5. `scripts/` isn't needed** in the container. Those are exploration scripts. Copying `tests/` instead lets a grader run your test suite inside the container, which is a strong reproducibility check.

### The new Dockerfile

```dockerfile
FROM condaforge/miniforge3:latest

WORKDIR /workspace

# environment.yml installs aadrkit itself (pip: -e .), so the package
# source must be in the image before the environment is created.
COPY environment.yml pyproject.toml ./
COPY src/ src/
RUN mamba env create -f environment.yml && mamba clean -afy

COPY tests/ tests/

# Run aadrkit by default; with no arguments, show its help.
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "aadr-project", "aadrkit"]
CMD ["--help"]
```

### How it works

- **`COPY environment.yml pyproject.toml ./`** copies both files into `/workspace`. When copying several files, the destination must end in `/`.
- **`COPY src/ src/`** brings in the package, so the `-e .` line in `environment.yml` can find it.
- **`RUN mamba env create ...`** builds the environment exactly as on your computers, including EIGENSOFT 9.0.0 and `aadrkit`. `mamba clean -afy` deletes downloaded package files afterward to keep the image smaller.
- **`COPY tests/ tests/`** comes *after* the environment, on purpose. Docker caches each step; if you change only a test, Docker reuses the cached environment instead of rebuilding it. The catch is that changing anything in `src/` does rebuild the environment, since it was copied before the `RUN` line. That's the price of the editable install, and worth knowing if rebuilds feel slow.
- **`ENTRYPOINT` and `CMD` work together:**
  - **`ENTRYPOINT`** is the fixed part: "run `aadrkit` inside the conda environment." `--no-capture-output` makes output appear live, the fix from Lab 1.
  - **`CMD`** is the default *arguments*, used only when you don't give any. So `docker run aadrkit` shows `--help`, and `docker run aadrkit list country` replaces `--help` with `list country`.

### The `.dockerignore` file

Create `.dockerignore` in the repo root:

```
data/
.git/
renv/library/
.pytest_cache/
**/__pycache__/
*.egg-info/
```

- **`data/`** is the important one: it keeps the 6.8 GB of AADR files out of the build.
- **`.git/`, caches, and `*.egg-info/`** are local files the image doesn't need. `*.egg-info` in particular is created by your editable install on your computer, and the image creates its own fresh one.

The data still reaches the container. You attach it when running, as shown below.

### Build and test it

From the repo root, in WSL. These assume Docker Desktop is running.

**1. Build the image:**

```bash
docker build -t aadrkit .
```

**`-t aadrkit`** names (tags) the image. The first build takes several minutes, mostly installing the environment.

**2. Run it with no arguments:**

```bash
docker run --rm aadrkit
```

You should see the `aadrkit` help text. **`--rm`** deletes the container when it finishes, so stopped containers don't pile up.

**3. Give it your data:**

```bash
docker run --rm -v "$(pwd)/data:/workspace/data" aadrkit list country
```

- **`-v HOST:CONTAINER`** is a **volume mount**: it makes your `data/` folder appear inside the container at `/workspace/data`. Nothing is copied; the container reads your files directly.
- **`$(pwd)`** is replaced by your current folder, so this works from anywhere the repo lives.
- Because `WORKDIR` is `/workspace` and the CLI's default paths are `data/raw/...`, the defaults just work inside the container, the same as on your computer.

**4. A full genotype extraction:**

```bash
docker run --rm -v "$(pwd)/data:/workspace/data" aadrkit select --group Scotland_Viking --out data/output/vikings_docker --genotypes --format plink
```

The outputs are written through the mount, so they appear in **your** `data/output/` folder when the container finishes:

```bash
ls data/output/vikings_docker*
```

You should see the same nine files as your `vikings_cli` run. If the container stops with **exit code 137**, it ran out of memory: Docker on WSL is limited by WSL's memory setting, and `convertf` needs about 8 GB.

**5. Run the test suite inside the container:**

```bash
docker run --rm -v "$(pwd)/data:/workspace/data" --entrypoint conda aadrkit run --no-capture-output -n aadr-project pytest -m "not slow"
```

- **`--entrypoint conda`** replaces the `aadrkit` entrypoint for this one run, since we want `pytest` instead.
- Everything after the image name becomes the arguments to `conda`: `run ... -n aadr-project pytest -m "not slow"`.
- You should see **66 passed, 2 deselected**. That's the same result as on your computers, from an environment built only from your repo's files. It's the strongest reproducibility evidence you can show.

### Optional: pin the base image

`FROM condaforge/miniforge3:latest` means "whatever version is newest when you build." Someone building next year could get a different base. To lock it, after your build succeeds, ask Docker for the exact image you used:

```bash
docker image inspect condaforge/miniforge3:latest --format '{{index .RepoDigests 0}}'
```

It prints something like `condaforge/miniforge3@sha256:...`. Replace the `FROM` line with that exact text. A digest identifies one specific image permanently, the same idea as the checksums on your AADR files.

### Update the README's Docker section

Replace the old commands with the ones from steps 1, 3, 4, and 5, plus a sentence explaining that the data isn't in the image and is attached with `-v`.

Then commit:

```bash
git add Dockerfile .dockerignore README.md
```

```bash
git commit -m "Run aadrkit in Docker: install package, mount data, run tests"
```

Paste the output of steps 2 and 5.
- **Verificaiton:**