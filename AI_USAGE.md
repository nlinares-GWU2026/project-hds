# AI USAGE LOG
- **Tool:**
- **What I was doing:**
- **What I asked (verbatim):**
- **Exact output (verbatim):** 
## Entry 1
- **Tool:** Claude (Opus 5.5)
- **What I was doing:** Downloading the `.anno` file from AADR
- **What I asked (verbatim):** "How do I download the `.anno` file correctly from Harvard Dataverse via terminal?"
- **Exact output (verbatim):**
I found something important while looking up the v66 files, and you need to know it before you submit the proposal on October 7.

## Heads-up: similar tools already exist

There are two Python packages on PyPI that overlap with `aadrkit`:

- **`aadr-subset`** selects a cohort from an AADR `.anno` file using a YAML selector and writes out a list of sample IDs, which you then pass to plink2 to build the actual subset.
- **`aadr-resolve`** reads `.anno` files across one or more AADR releases and matches the same individuals across versions using the Master ID column.

That means the sentence in your problem statement saying no lightweight, reusable tool exists isn't accurate. I should have searched for existing tools when we drafted that sentence, and I didn't. A grader who knows the field could find these quickly, so it's worth fixing before you submit.

This doesn't sink the project. The course asks for a real-world applied task using course concepts, not a new research contribution, and there's a real difference:

- `aadr-subset` stops at a list of IDs and hands off to plink2 for the genotype extraction.
- `aadrkit` plans to go all the way to the genotype subset files through `convertf`, in both EIGENSTRAT and PLINK formats.

There are two ways to handle it:

1. **Revise the sentence.** Acknowledge that these tools exist and state what `aadrkit` does differently: end-to-end extraction through EIGENSOFT, built as a tested, reproducible package.
2. **Also use `aadr-subset` as a check.** Run the same filter in both tools and compare the sample lists. Comparing against an independent implementation is exactly the kind of "scientific oversight" the rubric rewards. I haven't tested these packages myself, so treat them as reference points to evaluate, not as guaranteed ground truth.

I'd lean toward doing both.

## A second heads-up, for later

One user reported that the public 2M release was in a TGENO (transposed packed) format that older EIGENSOFT-style builds could not read properly. This doesn't affect today's `.anno` download. When you get to the `.geno` file, though, check early that `convertf` 9.0.0 can read it. It's also worth adding to your proposal's Risks section.

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
- **How I verified:** I completed all steps and the file downloaded accurately. MD5 checksum: a2db1ac16f0f3558ed66fb251e1d5c7d

Send me the column count, line count, and whether the MD5 matched. After that, we can add the data and citation section to the README and update the problem statement for the existing tools.
