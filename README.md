# Allen Ancient DNA Resource (AADR) Query and Subsetting Tool
[Explanation]

## Setup
Terms: 
- bash = Linux or macOS terminal. On Windows use WSL (Ubuntu); Git Bash and Command Prompt cannot run the conda environment or EIGENSOFT.
- R console = terminal within RStudio or running R in a terminal to move into an R prompt
- EIGENSOFT's `convertf` is required to read AADR's genotype files, and is only available after `conda activate aadr-project`. See `environment.yml`. 

### Python (conda)
In the bash terminal:
```bash
git clone https://github.com/nlinares-GWU2026/project-hds.git
cd project-hds
mamba env create -f environment.yml
conda activate aadr-project
which convertf
```

### R (renv)
In R or RStudio terminal:
- First, open the R project `project-hds`:
```r
renv::restore()
```

### Docker (optional)
The Dockerfile is included in this repo.
In the bash terminal after installing and setting up Docker:
```bash
docker build -t aadr-project .
docker run --rm aadr-project
```

## Data

This project uses the Allen Ancient DNA Resource (AADR), maintained by the Reich Lab at Harvard Medical School and distributed through the Harvard Dataverse (DOI: [10.7910/DVN/FFIDCW](https://doi.org/10.7910/DVN/FFIDCW)).

- **Dataset version:** 14.0 (contains AADR release v66.p1)
- **File:** `v66.p1_1240K.aadr.PUB.anno` (1240K panel metadata, patch 1 of release v66)

AADR data is not included in this repository. It is freely available with no access request required, so each user downloads their own copy. The `data/` directory and all AADR file types are listed in `.gitignore`.

### Download
From the repository root, in bash: 
```bash
mkdir -p data/raw
wget -O data/raw/v66.p1_1240K.aadr.PUB.anno "https://dataverse.harvard.edu/api/access/datafile/13994515" # .anno data
head -c 5 data/raw/v66.p1_1240K.aadr.patch.PUB.anno # "Genet" appears which is not the format but the beginning line of "Genetic ID" of the first column. The `.anno` file is a plain-text, tab-delimited annotation/metadata table.
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.geno "https://dataverse.harvard.edu/api/access/datafile/13994829" # .geno data
head -c 5 data/raw/v66.p1_1240K.aadr.patch.PUB.geno; echo # "TGENO" meaning transposed. The `.geno` file is a packed binary format used to store the genotype matrix of individuals across genetic markers. 
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.snp "https://dataverse.harvard.edu/api/access/datafile/13994514" # .snp data
head -c 5 data/raw/v66.p1_1240K.aadr.patch.PUB.snp; echo # Nothing appears because the `.snp` file type is a plain-text metadata that describes the genetic markers used in EIGENSTRAT or ADMIXTOOLS dataset
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.ind "https://dataverse.harvard.edu/api/access/datafile/13994513" # .ind data
head -c 5 data/raw/v66.p1_1240K.aadr.patch.PUB.ind; echo # Nothing appears because the `.ind` file type is a plain-text metadata that describes the individual samples or populations included in EIGENSTRAT or ADMIXTOOLS dataset

```

### Verify 
```bash
sha256sum -c docs/data_checksums.txt
sha256sum data/raw/v66.p1_1240K.aadr.patch.PUB.geno >> docs/data_checksums.txt # So the `.anno` line stays 
sha256sum data/raw/v66.p1_1240K.aadr.patch.PUB.snp >> docs/data_checksums.txt
sha256sum data/raw/v66.p1_1240K.aadr.patch.PUB.ind >> docs/data_checksums.txt
sha256sum -c docs/data_checksums.txt # EXPECT "OK" FOR ALL\
md5sum data/raw/v66.p1_1240K.aadr.PUB.anno
# Expected output:
# a2db1ac16f0f3558ed66fb251e1d5c7d  data/raw/v66.p1_1240K.aadr.PUB.anno
md5sum data/raw/v66.p1_1240K.aadr.patch.PUB.*
# Expected output: 
# 5ea1d2675a271c81e55b8f8b08b3ff3b  data/raw/v66.p1_1240K.aadr.patch.PUB.geno
# 19a434ac954bcd10dbb8dba1d1188a09  data/raw/v66.p1_1240K.aadr.patch.PUB.ind
# 50f66178fc81b8aa087cc4b135317e59  data/raw/v66.p1_1240K.aadr.patch.PUB.snp
```
Expected output: 
- data/raw/v66.p1_1240K.aadr.PUB.anno: OK`. The file's MD5 checksum (`a2db1ac16f0f3558ed66fb251e1d5c7d`) also matches the value listed on its Dataverse page.
- data/raw/v66.p1_1240K.aadr.PUB.geno: OK`. The file's MD5 checksum (`5ea1d2675a271c81e55b8f8b08b3ff3b`) also matches the value listed on its Dataverse page.

[Download instructions for the genotype files (`.geno`, `.snp`, `.ind`) will be added when `convertf` integration begins.]

## Check Everything Works
In terminal:
```bash
python scripts/profile_anno.py
```

## Repository Layout
```text
project-hds/
├── data/                          # NOT tracked by git; created by the download steps (see Data)
│   ├── raw/                       # AADR v66.p1 files (.anno, .geno, .snp, .ind)
│   └── test_convertf/             # Temporary outputs from the manual convertf test
├── docs/                          # Proposal, notes, and checksums
│   ├── Nicole_Linares_Proposal_aadrkit.pdf  # Approved project proposal
│   ├── anno_notes.md              # Findings and design decisions from exploring AADR
│   ├── data_checksums.txt         # SHA-256 checksums for the downloaded AADR files
│   └── lab1-addendum.md           # Lab 1 addendum (to remove after the semester)
├── renv/                          # R environment files managed by renv
│   ├── .gitignore                 # Keeps renv's local package library out of git
│   ├── activate.R                 # Activates renv when the project opens
│   └── settings.json              # renv settings
├── scripts/                       # Exploration scripts (not part of the package)
│   ├── convertf_test.par          # Parameter file for the manual convertf test
│   ├── count_suffixes.py          # Counts suffixes (e.g., -o outliers) in AADR group names
│   ├── explore_anno.py            # First look at the .anno file: size and column names
│   ├── find_test_indiv.py         # Finds candidate individuals for edge-case tests
│   ├── profile_anno.py            # Profiles column types, missing values, and value counts
│   └── profile_ids.py             # Checks repeated individuals and publication/DOI completeness
├── src/
│   ├── aadrkit/                   # The aadrkit Python package
│   │   └── __init__.py            # Package entry point and version number
│   ├── placeholder.py             # Lab 1 placeholder (run by the Dockerfile for now)
│   └── placeholder.R              # Lab 1 placeholder (keeps dplyr recorded for renv)
├── tests/                         # pytest tests and hand-verified test data
│   ├── ground_truth.tsv           # Ten AADR individuals verified by hand with grep
│   └── test_import.py             # Checks that the package installs and imports
├── .gitignore                     # Files and folders git should not track
├── .Rprofile                      # Activates renv when R starts in this project
├── AI_USAGE.md                    # Log of AI assistance and how it was validated
├── Dockerfile                     # Container build for the environment
├── README.md                      # This file
├── environment.yml                # Conda environment: Python, pandas, EIGENSOFT, pytest, aadrkit
├── project-hds.Rproj              # RStudio project file
├── pyproject.toml                 # Package metadata pip uses to install aadrkit
└── renv.lock                      # Exact R package versions        
```

## Citation

If you use AADR data obtained with this tool, cite all three of the following:
1. **The AADR paper:** Mallick, S., Micco, A., Mah, M., Ringbauer, H., Lazaridis, I., Olalde, I., Patterson, N., & Reich, D. (2024). The Allen Ancient DNA Resource (AADR) a curated compendium of ancient human genomes. *Scientific Data*, 11(1). https://doi.org/10.1038/s41597-024-03031-7
2. **The dataset version you downloaded:** Mallick, Swapan; Reich, David, 2023, "The Allen Ancient DNA Resource (AADR): A curated compendium of ancient human genomes", https://doi.org/10.7910/DVN/FFIDCW, Harvard Dataverse, V14
3. **The original publications** for every individual included in your analysis. The AADR is a compilation of previously published data, and its authors state that citing the AADR is not a substitute for citing the original studies. The source publication for each individual is recorded in the `.anno` file.
