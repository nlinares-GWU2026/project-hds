# AADR .anno File Notes
## Progress: 
### (Before transitioning to different notes format) Exploring data before writing tool code (1-9):
Step 1: Explored the metadata. Loaded all 23089 rows and 49 columns and matched columns to planned filters. 
Step 2: Profiled the columns. Checked what was inside the date, location, coverage, country, population, data type, and quality (filters I will use). Identified hidden problems like ".." for misisng values, a chimpanzee and gorilla REF was labeled as present, messy capitalization, and 784 people had no long. and lat. coordinates. 
Step 3: Choosing hand verified "test"/"ground truth" individuals to test my tool against (8-10 individuals I will check myself). From the profiling, the tricky cases and individuals I would want to choose are: 1. present-day (0 BP), 2. reference genome (like `Chimp.REF`), 3. the one post-1950 individual (-4 BP), 4. someone with missing coordinates, 5. someone with low coverage, 6. someone from a place AADR lists separately (Canary Islands), 7. Someone whose group matches a pattern like "Viking, 8. a person with several rows. First check duplicates and publications to see how often one person appears in several rows before choosing test. Next, choose individuals. Finally, verify each one by hand with `grep` and record expected  values.  
1. File details
- File: v66.p1_1240K.aadr.PUB.anno (Dataverse file ID 13994515)
- Downloaded: 09/25/2026
- Size: 23,089 rows × 49 columns (pandas count matches `wc -l` minus the header)
-  Checksums: see docs/data_checksums.txt; MD5 matched Dataverse

2. Columns used by each filter
How the columns map to filters
|Filter| Column | Notes |
 Filter: ID for covertf | Columns: 0 Genetic Identity | Should match the IDs in the `.ind` file, which is how the filter results connect to geno extraction
Filter: Region | Columns : 16 Political Entity, 15 Locality, 17 -18 Latitude/Longitutde | Country for simple filtering, coordinates allow for bound-box filter
Filter: Time Period | Columns: 10 Date mean in BP | "BP" means years before 1950 CE, so 5000 BP is about 3050 BCE 
Filter: Population | Columns: 14 Group ID | Likely same labels as .ind file's population column
Filter: Lineage | Columns: 35 Y haplogroup (ISOGG), 38 mtDNA haplogroup 
Filter: Coverage | Columns: 26 SNPs hit on 1240K snpset | Use 26, not 25 or 27-29 because those count SNPs on other panels, and this project uses 1240K panel
Filter: Quality | Columns: 47 ASSESSMENT
Filter : Publication | Columns: 5 First publication (abbrev. earliest paper that reported data on indiv.), 6 Publication abbrev, 7 doi for publication of this representation of the data | They can differ and a correct citation list may need both. Some rows may have ".." instead of a DOI in column 7

3. Column name quirks
- Column 33 duplicate name, renamed with ".1" by pandas because file has two columns with exactly the same name
- Column 25 has trailing space at end of its name (code that types space won't find column)
- AADR column names are long and might have trailing space so aadrkit will adopt short names in place of typing out long real column names for ease
- Missing values are written as ".."
- One person can have several rows (Column 0 explains ".AG, .DG, .SG" and other data types for individuals), a filter could return the samer person twice so aadirkit will handle duplicates
- Exact text matching works if users know precise name. Pattern matching (using regex) lets users search for terms but patterns need precise boundaries so it does not accidentally catch unrelated names. Group ID links filter outputs to .ind files for convertf. 

4. Missing values
- AADR marks missing values as ".." 
- Columns with missing values (Latitude (17) and Longitude (18)) confirmed 784 - implement coordinate based region filter

5. Dates below 0 BP or at 0 BP
- Every row dated 0 BP says "present" so BP isn't being used as a placeholder for unknown dates, consistently means present day. 
- The -4 row reads 1954 CE 
- There are 4 rows labelled present that are ref rows including chimp, gorilla, and ancestor - we do not necessarily want to include this. Since pop geneticits use chimp or gorilla for comparing populations in kinds of analysis that ADMIXTOOLS runs, best option would to be exclude the references as default and have an option to include them 
- The "ancient" filter does not necessarily mean "ancient" - it means dated before present which includes historic individuals

6. Messy data
- Column 21 data type contains mixed casing, mulitple values combined with commas, and free-text notes. Leave a data-type filter out of scope of my tool - it is messy and requires extra string splitting while Column 26 (Coverage/SNP hit) alraedy measures data quantity more directly. 

7. Coverage
- User chooses the min SNP count with no hidden default

8. Design decisions
- Loading: use na_values=[".."] so AADR's missing-value marker becomes a real missing value.
- Present-day: date_bp == 0 means present-day. All 3,970 such rows say "present" in v66.p1. Because this is an assumption about the data, it deserves its own test, so the package notices if a future AADR version breaks it.
- Reference genomes: four .REF rows aren't individuals. Exclude them from present-day and ancient selections by default, with an option to include them (for example, for a chimpanzee outgroup).
- Dates: negative values are valid (post-1950). The date filter uses the mean date and should say so in the documentation. The word "ancient" should be defined as "dated before present."
- Region: match country labels exactly but case-insensitively, and provide a helper that lists available labels. The coordinate filter reports how many individuals it excludes for missing coordinates (784).
- Population: offer exact match and anchored regular-expression matching on Group ID, plus a helper to list groups (3,897 of them).
- Coverage: the user chooses the minimum SNP count (column 26); no hidden default.
- Quality: look up what PROVISIONAL_ and MERGE_ mean before designing a quality filter.
- Data type: messy (case variants, comma-combined values, free-text notes) and out of scope as a filter.

9. Open questions
- Duplicates: one row per person or keep all?
- Citations: column 5 (first pub), 6 (this data's pub), or both?
- Date filer: mean only, or range using the uncertainty column (11)?
- Can the country column cover individuals missing coords?
- Do Genetic IDs match the first column of the .ind file exactly?
- Is the .geno file in TGENO format, and can convertf 9.0.0 read it?
## Completed:
1.  Planned the project and wrote the proposal. Chose AADR, named the tool, decided to use convertf rather than write a decoder from scratch, found similar existing tools and explained how yours differs, and added the citation-export idea.	The proposal is 10% of your grade and must be approved. The planning decisions keep the project finishable solo in eight weeks.
2. Cleaned up the repo. Stopped tracking .Rhistory, kept .Rprofile, and made git ignore the data/ folder.	Keeps the repo tidy and guarantees the large AADR files never get uploaded, which you promised in the proposal.
3. Checked the tools. Confirmed convertf works inside aadr-project and pinned EIGENSOFT 9.0.0 in environment.yml.	The whole tool depends on convertf. Pinning the version means anyone rebuilding your environment gets the same version you tested with.
4. Downloaded and verified the data. Got the metadata file, discovered its real name (v66.p1), matched the MD5 checksum, and saved a SHA-256 checksum to the repo.	Proves you're working from the exact file the Reich Lab published, and lets anyone confirm they have the same file.
5. Documented setup, data, and citations in the README.	Reproducibility: a stranger should be able to go from clone to results by following the README.
6. Step 1 `explore_anno.py`: Explored the metadata. Loaded all 23,089 rows and 49 columns, and matched columns to each planned filter. Also fixed the Windows-Python and Git Bash mix-up.	You can't write a filter for a column you haven't found. The environment fix ensures every result comes from your pinned setup.
7. Step 2 `profile_anno.py`: Profiled the columns. Checked what's actually inside the date, location, coverage, country, population, data type, and quality columns.	This is where the hidden problems surfaced: ".." for missing values, a chimpanzee and gorilla labeled "present," messy capitalization, and 784 people without coordinates. Each would have become a bug if you'd written filters first.
8. Step 3 `profile_ids.py`: Choose ground truth test individuals whose values I checked myself. Later when I write the tests, it will be structured like "if I filter for Poland in the Iron Age, individual X must be included and individual Y must not be." I will be profiling the tricky cases: a present-day individual (0 BP), a reference genome (like Chimp.REF), the one post-1950 individual (−4 BP), someone with missing coordinates, someone with very low coverage, someone from a place AADR lists separately, like the Canary Islands, someone whose group matches a pattern, like Viking, a person with several rows. Step 3a: check duplicates and publications, Step 3b: choose individuals, Step 3c: verify each one by hand with `grep` and record the expected values. 
**Genetic ID is unique for every row (23,089 IDs for 23,089 rows) which makes it the reliable key for identifying a specific dataset and it is the ID `convertf` will use. Individual ID is not unique (21,433 different people so about 1650 rows are repeat appearances), most people (20,171) have one row, 936 have two, and one person, YCH017, has 11 (YCH017's rows show why. They're all the same individual from Late Classic Mexico, but they come from different datasets: .AG is 1240K capture and .IM is immune capture, plus several _alt and _d versions. I don't know exactly what _alt and _d mean, so that's another one to look up rather than guess. Their data quality varies hugely, from 7,796 SNPs up to 1,064,203 for YCH017.AG). DEDUPLICATION SHOULD BE ON BY DEFAULT AND FILTER FIRST THEN DEDUPLICATE.**
**Publications:** Every row has a publicaiton label - no missing values from 5 or 6. 647 rows have no DOI - export can only give the label. 2781 rows have a different first publication. So the export should list both columns (paper that first reported the individual and the individual paper for this version of data). *Some labels are not published papers so they should be flagged accordingly.* **The labels are inconsistent so they are just names and not structured citations. So DOI should be the main identifier in the export with the label as the fallback.** Many names contain non-English characters, **so aadrkit must use UTF-8 encoding explicitly.**
** 358 unique publicaitons**
9. Choosing test individuals: Already have 1. reference gnome `Chimp.REF` (must be excluded from present-day and ancient selections by default), 2. Post-1950 date `Kwhit.Sg` (only negative date), 3. Present day/Unusual data type `JHF05.AG` (present-day but captured with an ancient method), 4. Person with many rows `YCH017` (deduplication). Still need: missing coordinates, very low coverage, Canary Islands (that AADR lists separately from Europe), a "Viking" group (group matching pattern), a standard present day individual, an "unpublished" row, and a row with a missing DOI. --> `find_test_indiv.py`. Then followed the grep regex commands per Claude's help to verify that they were individually findable, not jut through pandas. (From AADR v66.p1)
```
**Genetic ID	What it tests**
1	Chimp.REF	Reference genome: excluded by default. Also "Unpublished," with no country or coordinates
2	Khwit.SG	The only post-1950 date (−4 BP, 1954 CE)
3	JHF05.AG	Present-day individual with an "ancient-style" data type (1240k)
4	NA20813.DG	Standard present-day individual (TSI, Italy)
5	YCH017.AG	Person with 11 rows: deduplication must keep this one
6	I8508.AG	Missing coordinates, but has a country (Uzbekistan)
7	I13976.SG	Lowest coverage in the file (281 SNPs)
8	gun005.SG	Canary Islands: must not appear when filtering for Spain
9	VK202.AG	Scotland_Viking; also has no DOI
10	VK201.AG	Scotland_Viking-o: the outlier test
``` 
All were successful and information about the outlier, low coverage, and contamination suffixes was found. As a design decision, the population filter could offer explicigt options to include all of those different 3 options. But as a check before deciding on that I checked the suffixes: -o was 499 groups or about 13% of all 3897 which is a lot of outlier groups so it needs proper handling. The text after -o describes how the individual differs from their group. EEF = Early European Farmer with low or high ancestry tied to it. _o had 0 groups which confirmed that v66 replaced the underscore with the hyphen. The paper's convention does not apply to this version. contam had 0 groups. v66.p1 does not mark contamination in group names. Contamination appears to be in the quality columns so the quality filter would cover it. lc had 2 groups but both with false positives that just picked up the letters "lc" in an anctual population name. Low-coverage is handled by the SNP count column anyway. 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
**Suffix Regex Rule: -o[^]*$**
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
10. Downloading the .geno, .snp, and .ind files and checking if convertf 9.0.0 can read them. Make sure you have enough free disk space to download using `df -h /mnt/c ~`. At time of downloading I had 695 G available on my system and 927G on the root file system of Linux. The file size of the 3 files: `v66.p1_1240K.aadr.patch.PUB.geno` (each genotype is 2 bits) was 6.6 GB, `v66.p1_1240K.aadr.patch.PUB.ind` was 993.6 KB (one line per individual), and `v66.p1_1240K.aadr.patch.PUB.snp` (one line per SNP) was 74.1 MB. *Note: these three files include "aadr.patch.PUB." while the .anno file does not contain ".patch". The aadrkit must have the file paths set separately. Saved to data/raw. `.geno` file link: `https://dataverse.harvard.edu/api/access/datafile/13994829` and MD5 number: 5ea1d2675a271c81e55b8f8b08b3ff3b, `.snp` file link: `https://dataverse.harvard.edu/api/access/datafile/13994514` and MD5 number: 50f66178fc81b8aa087cc4b135317e59, `.ind` file link: `https://dataverse.harvard.edu/api/access/datafile/13994513` and MD5 number:19a434ac954bcd10dbb8dba1d1188a09. The same steps to download the `.anno` file were completed in for the `.geno`, `.snp`, `.ind` and recorded in the `README.md`.
## Current:
11. `convertf` file to run against test individuals. It is a small command-line program from EIGENSOFT. Means "convert format". It (1) reads genotype data in one format and writes it in another (like AADR's packed binary format into EIGENSTRAT text format or PLINK format) and (2) leaves out individuals you do not want while it converts (what aadrkit relies on). It works on `.geno`, `.snp`, and `.ind`. The `.geno` file only makes sense with the other two, the `.ind` says which column is which person, and the `.snp` says while row is which marker. `convertf` is given a parameter file (short plain-text file of settings) run by `convertf -p myfile.par`. `convertf` leaves people out by editing the population label in a copy of the `.ind` file - any individual labeled "Ignore" is skipped. Also why `hascheck: NO` because genotype files srecord a "hash" of original `.ind` and `.snp` files. 
- This is necessary for `aadrkit` because everytime it is used the package will: (1) Filter the `.anno` metadata with pandas (dates, region, coverage, etc.) to get a list of Genetic IDs, (2) Write a modified `.ind` where everyone not on that list is set to "Ignore", (3) Write a parameter file, (4) Run `convertf` using Python's `subprocess` module, and (5) Check the output to confirm the right individuals came out. First I will be testing a present day Tuscan (1.1 million SNPs), a VIking (810,000 SNPs), and the lowest coverage (281 SNPs).
We don't know whether the `.anno` lists individuals in the same order as the `.ind` file. So `aadrkit` should always match the two files by Genetic ID, never by row position. 
- The TGENO file worked correctly in `real    1m18.590s`. Interpreting the results, I sae that the `records read: 3` (my 3 individuals), `before compress: ... 23089` (correct, the total number of individuals), `after compress: ... 3`, `numsnps output: 1233013` (kept all SNPs). *`convertf` used 8GB of RAM - WSL limits how much of the computer's memory it can use so user's should be aware of how much they have.*