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
git commit -m "Add numeric column profiling for anno file"
```
- **Verificaiton:** I developed the script, ran it, and visually inspected the results and interpreted them on my own before continuing. 