# AI USAGE LOG
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
- **Verificaiton:**
