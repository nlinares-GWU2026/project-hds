# Allen Ancient DNA Resource (AADR) Query and Subsetting Tool
[Explanation]

## Setup
Terms: 
- bash = Linux or macOS terminal. On Windows use WSL (Ubuntu); Git Bash and Command Prompt cannot run the conda environment or EIGENSOFT.
- R console = terminal within RStudio or running R in a terminal to move into an R prompt
- EIGENSOFT's `convertf` is required to read AADR's genotype files, and is only available after `conda activate aadr-project`. See `environment.yml`.
*Keep the project in a folder whose path has no spaces. EIGENSOFT's `convertf` cannot read paths that contain spaces.* 

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

## Usage

Run commands from the repository root with `conda activate aadr-project`. 

### Command line

```bash
# See the exact labels available for filtering
aadrkit list country
aadrkit list group_id

# Preview a selection (prints a step-by-step report, saves nothing)
aadrkit select --min-bp 1000 --max-bp 1500 --country "United Kingdom" --min-snps 100000

# Save the selection and extract PLINK genotypes
aadrkit select --group Scotland_Viking --out data/output/vikings --genotypes --format plink

# Pattern matching on population labels: every Iron Age group in Poland
aadrkit select --group "_IA$" --group-regex --country Poland
```

Run `aadrkit select --help` for every option.

**Defaults:** reference genomes (Chimp, Gorilla, etc.) are excluded. Population-genetic outliers ("-o" groups) are excluded from population matches unless `--include-outliers` is given. Each person appears once (the dataset with the most SNPs is kept). There is no default coverage threshold, so set `--min-snps` explicitly.

### Python

```python
import aadrkit

anno = aadrkit.load_anno("data/raw/v66.p1_1240K.aadr.PUB.anno")
selected, report = aadrkit.select(anno, groups="Scotland_Viking", min_snps=100000)

g = "data/raw/v66.p1_1240K.aadr.patch.PUB"
aadrkit.extract_genotypes(selected, f"{g}.geno", f"{g}.snp", f"{g}.ind",
                          "data/output/vikings", output_format="PACKEDPED")
```

### Outputs

With `--out PREFIX`:
- `PREFIX_selected.tsv`: selected individuals with their metadata, including publications and DOIs
- `PREFIX_report.tsv`: how many rows each filtering step removed
- `PREFIX_command.txt`: the `aadrkit` version and the exact command, for rerunning

With `--genotypes`, also: genotype files (`.geno/.snp/.ind`, or `.bed/.bim/.fam` for PLINK),
plus `_selection.ind`, `.par`, and `.log` recording exactly how `convertf` was run.

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

## Testing 

```bash
pytest -m "not slow" # fast tests
pytest -v            # all tests, including two that run convertf
```

Tests that need AADR data are skipped automatically if the files have not been downloaded. `test/ground_truth.tsv` holds ten individuals whose values were verified by hand with `grep`, independently of aadrkit's code. Tests compare aadrkit's results against them.

## Output Formats
`extract_genotypes` writes EIGENSTRAT (`.geno/.snp/.ind`) or PLINK binary (`output_format="PACKEDPED"`: `.bed/.bim/.fam`). In PLINK output, the Genetic ID is the individual ID (column 2 of the `.fam`). The family ID is a sequence number, and the phenotype column is a placeholder set by `convertf`. Each run also writes `_selection.ind`, `.par`, and `.log` files recording exactly how the output was made.

## Repository Layout
```text
```text
project-hds/
├── data/                                    # NOT tracked by git; created by the download steps (see Data)
│   ├── output/                              # aadrkit outputs: selections, genotypes, and their records
│   ├── raw/                                 # AADR v66.p1 files (.anno, .geno, .snp, .ind)
│   └── test_convertf/                       # Temporary outputs from the manual convertf test
├── docs/                                    # Proposal, notes, and checksums
│   ├── Nicole_Linares_Proposal_aadrkit.pdf  # Approved project proposal
│   ├── anno_notes.md                        # Findings and design decisions from exploring AADR
│   ├── data_checksums.txt                   # SHA-256 checksums for the downloaded AADR files
│   └── lab1-addendum.md                     # Lab 1 addendum (to remove after the semester)
├── renv/                                    # R environment files from Lab 1 (not needed for aadrkit)
│   ├── .gitignore                           # Keeps renv's local package library out of git
│   ├── activate.R                           # Activates renv when the project opens
│   └── settings.json                        # renv settings
├── scripts/                                 # Exploration scripts (not part of the package)
│   ├── convertf_test.par                    # Parameter file for the manual convertf test
│   ├── count_suffixes.py                    # Counts suffixes (e.g., -o outliers) in group names
│   ├── explore_anno.py                      # First look at the .anno file: size and column names
│   ├── find_case_collisions.py              # Finds Group IDs that differ only by capitalization
│   ├── find_test_indiv.py                   # Finds candidate individuals for edge-case tests
│   ├── profile_anno.py                      # Profiles column types, missing values, value counts
│   └── profile_ids.py                       # Checks repeated individuals and publication/DOI data
├── src/
│   ├── aadrkit/                             # The aadrkit Python package
│   │   ├── __init__.py                      # Package entry point: version and main functions
│   │   ├── anno.py                          # Loads the .anno file with short column names
│   │   ├── cli.py                           # The `aadrkit` terminal command (list, select)
│   │   ├── convertf.py                      # Runs convertf to extract genotypes for a selection
│   │   ├── filters.py                       # Date, region, population, coverage filters; dedup
│   │   └── query.py                         # select(): filters in order, defaults, and a report
│   ├── placeholder.py                       # Lab 1 placeholder (run by the Dockerfile for now)
│   └── placeholder.R                        # Lab 1 placeholder (keeps dplyr recorded for renv)
├── tests/                                   # pytest tests and hand-verified test data
│   ├── conftest.py                          # Shared fixtures: AADR data and ground truth
│   ├── ground_truth.tsv                     # Ten AADR individuals verified by hand with grep
│   ├── test_anno.py                         # Loader tests, including against ground truth
│   ├── test_cli.py                          # Command-line interface tests
│   ├── test_convertf.py                     # Genotype extraction tests (two marked slow)
│   ├── test_data_assumptions.py             # Facts about AADR v66.p1 the design relies on
│   ├── test_filters.py                      # Filter tests on toy tables and real data
│   ├── test_import.py                       # Checks that the package installs and imports
│   └── test_query.py                        # select() tests: order, defaults, and report
├── .gitignore                               # Files and folders git should not track
├── .Rprofile                                # Activates renv when R starts in this project
├── AI_USAGE.md                              # Log of AI assistance and how it was validated
├── Dockerfile                               # Container build for the environment
├── README.md                                # This file
├── environment.yml                          # Conda environment: Python, pandas, EIGENSOFT, pytest, aadrkit
├── project-hds.Rproj                        # RStudio project file
├── pyproject.toml                           # Package metadata; registers the `aadrkit` command
└── renv.lock                                # Exact R package versions
```       
```

## Requirements and limitations

- **Linux, macOS, or WSL on Windows.** EIGENSOFT is not available for native Windows.
- **No spaces in file paths.** `convertf` cannot read paths containing spaces; aadrkit checks for this and stops with an explanation.
- **About 8 GB of free memory** for genotype extraction.
- **Built and tested for AADR v66.p1.** Column names and data conventions (such as "-o" outlier labels and 0 BP meaning present-day) can change between AADR releases. The tests in `tests/test_data_assumptions.py` check these conventions and will fail if a different release breaks them.
- **Dates** are filtered on AADR's mean date (years before 1950 CE), not the full uncertainty range.
- **Country labels** match AADR exactly (ignoring capitalization). Some territories are listed separately, like "Canary Islands", is not included in "Spain".

## Citation

If you use AADR data obtained with this tool, cite all three of the following:
1. **The AADR paper:** Mallick, S., Micco, A., Mah, M., Ringbauer, H., Lazaridis, I., Olalde, I., Patterson, N., & Reich, D. (2024). The Allen Ancient DNA Resource (AADR) a curated compendium of ancient human genomes. *Scientific Data*, 11(1). https://doi.org/10.1038/s41597-024-03031-7
2. **The dataset version you downloaded:** Mallick, Swapan; Reich, David, 2023, "The Allen Ancient DNA Resource (AADR): A curated compendium of ancient human genomes", https://doi.org/10.7910/DVN/FFIDCW, Harvard Dataverse, V14
3. **The original publications** for every individual included in your analysis. The AADR is a compilation of previously published data, and its authors state that citing the AADR is not a substitute for citing the original studies. The source publication for each individual is recorded in the `.anno` file.
