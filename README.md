# aadrkit: Allen Ancient DNA Resource (AADR) Query and Subsetting Tool

`aadrkit` is a Python package and command-line tool for selecting individuals from the Allen Ancient DNA Resource (AADR) and exporting their genotypes. It filters by date, country, coordinates, population, label, and coverage; reports how many individuals each filter removed; keeps one dataset per person; and uses EIGENSOFT's `convertf` to write EIGENSTRAT or PLINK files ready for downstream tools such as ADMIXTOOLS. Built for PUBH 6854 (Applied Computing), GWU, Fall 2026.

## Requirements

- **Linux, macOS, or WSL on Windows.** EIGENSOFT is not available for native Windows. Git Bash and Command Prompt cannot run the conda environment or EIGENSOFT.
- **No spaces in file paths.** `convertf` cannot read paths containing spaces; aadrkit checks for this and stops with an explanation.
- **About 8 GB of free memory** for genotype extraction.
- **conda or mamba** (example, Miniforge).

## Setup

Terms: 
- bash = Linux or macOS terminal. On Windows use WSL (Ubuntu); Git Bash and Command Prompt cannot run the conda environment or EIGENSOFT.
- R console = terminal within RStudio or running R in a terminal to move into an R prompt
- EIGENSOFT's `convertf` is required to read AADR's genotype files, and is only available after `conda activate aadr-project`. See `environment.yml`.
*Keep the project in a folder whose path has no spaces. EIGENSOFT's `convertf` cannot read paths that contain spaces.* 

In the bash terminal:
```bash
git clone https://github.com/nlinares-GWU2026/project-hds.git
cd project-hds
mamba env create -f environment.yml
conda activate aadr-project
which convertf
aadrkit --help
```
`mamba` may suggest `mamba activate`. `conda activate` works the same way. EIGENSOFT's `convertf` (needed to read AADR's genotype files) and the `aadrkit` command are only available after `conda activate aadr-project`. If `which convertf` prints a path and `aadrkit --help` prints the help text, the environment is complete and ready to use. 

If you prefer a container, see [Docker](#docker) below.

## Data

This project uses the Allen Ancient DNA Resource (AADR), maintained by the Reich Lab at Harvard Medical School and distributed through the Harvard Dataverse (DOI: [10.7910/DVN/FFIDCW](https://doi.org/10.7910/DVN/FFIDCW)).

- **Dataverse dataset version:** 14.0 (contains AADR release v66.p1)
- **Files (1240K panel, patch 1 of release v66):**
  - `v66.p1_1240K.aadr.PUB.anno`: metadata for each individual (plain-text table)
  -  `v66.p1_1240K.aadr.patch.PUB.geno`: genotypes (about 6.7 GB, packed binary in transposed "TGENO" format)
  -  `v66.p1_1240K.aadr.patch.PUB.snp`: one line per SNP
  -  `v66.p1_1240K.aadr.patch.PUB.ind`: one line per individual

Note that the genotype files include `.patch` in their names and the `.anno` file does not.

AADR data is not included in this repository. It is freely available with no access request required, so each user downloads their own copy. the `data/` directory and all AADR file types are listed in `.gitignore`.

## Download

From the repository root:
```bash
mkdir -p data/raw
wget -O data/raw/v66.p1_1240K.aadr.PUB.anno "https://dataverse.harvard.edu/api/access/datafile/13994515"
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.geno "https://dataverse.harvard.edu/api/access/datafile/13994829"
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.snp "https://dataverse.harvard.edu/api/access/datafile/13994514"
wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.ind "https://dataverse.harvard.edu/api/access/datafile/13994513"
```

`-c` resumes an interrupted download. Rerun the same command to continue.

### Verify

```bash
sha256sum -c docs/data_checksums.txt
```

Expected output:
```text
data/raw/v66.p1_1240K.aadr.PUB.anno: OK
data/raw/v66.p1_1240K.aadr.patch.PUB.geno: OK
data/raw/v66.p1_1240K.aadr.patch.PUB.snp: OK
data/raw/v66.p1_1240K.aadr.patch.PUB.ind: OK
```

The checksums in `docs/data_checksums.txt` were recorded from files whose MD5 checksums matched the values listed on Dataverse. To check against Dataverse directly:
```bash
md5sum data/raw/v66.p1_1240K.aadr.PUB.anno data/raw/v66.p1_1240K.aadr.patch.PUB.*
```

```text
a2db1ac16f0f3558ed66fb251e1d5c7d  data/raw/v66.p1_1240K.aadr.PUB.anno
5ea1d2675a271c81e55b8f8b08b3ff3b  data/raw/v66.p1_1240K.aadr.patch.PUB.geno
19a434ac954bcd10dbb8dba1d1188a09  data/raw/v66.p1_1240K.aadr.patch.PUB.ind
50f66178fc81b8aa087cc4b135317e59  data/raw/v66.p1_1240K.aadr.patch.PUB.snp
```

Checksumming the 6.7 GB `.geno` takes a few minutes.

## Check everything works

```bash
aadrkit list country | head -n 5
pytest -m "not slow"
```

The first command should list the five countries with the most individuals (Russia first). The second should report **66 passed, 2 deselected**.

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

**Defaults:** reference genomes (Chimp, Gorilla, etc.) are excluded. Population-genetic outliers ("-o" groups) are excluded from population matches unless `--include-outliers` is given. Each person appears once (the dataset with the most SNPs is kept).  There is no default coverage threshold, so set `--min-snps` explicitly. 

## Python 

```python
import aadrkit

anno = aadrkit.load_anno("data/raw/v66.p1_1240K.aadr.PUB.anno")
selected, report = aadrkit.selection(anno, groups="Scotland_Viking", min_snps=100000)

g = "data/raw/v66.p1_1240K.aadr.patch.PUB"
aadrkit.extract_genotypes(selected, f"{g}.geno", f"{g}.snp", f"{g}.ind",
                          "data/output/vikings", output_format="PACKEDPED")
```

### Outputs

With `--out PREFIX`:
- `PREFIX_selected.tsv`: selected individuals with their metadata, including publications and DOIs
- `PREFIX_report.tesv`: how many rows each filtering step removed
- `PREFIX_command.txt`: the `aadrkit` version and the exact command, for rerunning

With `--genotypes`, also:
- **Genotype files:** EIGENSTRAT (`.geno/.snp/.ind`, the default) or PLINK binary (`--format plink`: `.bed/.bim/.fam`)
- **A record of the extraction:** `_selection.ind`, `.par`, and `.log`, showing exactly how `convertf` was run

In PLINK output, the Genetic ID is the individual ID (column 2 of the `.fam`). The family ID is a sequence number, and the phenotype column is a palceholder set by `convertf`. 

## Testing

```bash
pytest -m "not slow"      # fast tests
pytest -v                 # all tests, including two that run convertf
```

Tests that need AADR data are skipped automatically if the files have not been downloaded. `tests/ground_truth.tsv` holds ten individuals whose values were verified by hand with `grep`, independently of aadrkit's code. Tests compare aadrkit's results against them. `docs/fresh_clone_test.md` records a full reproducibility test from a fresh clone.

## Docker
The Dockerfile builds the same environment in a container. The data is not in the image; it is attached at runtime with `-v`. `-v HOST:CONTAINER` makes the `data/` folder appear inside the container at `/workspace/data`. Nothing is copied: the container reads the files directly from the computer.

After installing Docker, from the repository root:
```bash
docker build -t aadrkit .
docker run --rm aadrkit
docker run --rm -v "$(pwd)/data:/workspace/data" aadrkit list country
docker run --rm -v "$(pwd)/data:/workspace/data" aadrkit select --group Scotland_Viking --out data/output/vikings_docker --genotypes --format plink
ls data/output/vikings_docker*
docker run --rm -v "$(pwd)/data:/workspace/data" --entrypoint conda aadrkit run --no-capture-output -n aadr-project pytest -m "not slow"
```

## Limitations

- **Built and tested for AADR v66.p1**: Column names and data conventions (such as "-o" outlier labels and 0 BP meaning present-day) can change between AADR releases. The tests in `tests/test_data_assumptions.py` check these conventions and will fail if a different release breaks them.
- **Dates** are filtered on AADR's mean date (years before 1950 CE), not the full uncertainty range.
- **Country labels** match AADR exactly (ignoring capitalization). Some territories are listed separately. For example: "Canary Islands" is not included in "Spain". 

## Repository layout
 
```text
project-hds/
├── data/                                    # NOT tracked by git; created by the download steps (see Data)
│   ├── output/                              # aadrkit outputs: selections, genotypes, and their records
│   ├── raw/                                 # AADR v66.p1 files (.anno, .geno, .snp, .ind)
│   └── test_convertf/                       # Temporary outputs from the manual convertf test
├── docs/                                    # Proposal, notes, checksums, and test records
│   ├── Nicole_Linares_Proposal_aadrkit.pdf  # Approved project proposal
│   ├── anno_notes.md                        # Findings and design decisions from exploring AADR
│   ├── data_checksums.txt                   # SHA-256 checksums for the downloaded AADR files
│   ├── fresh_clone_test.md                  # Record of the fresh-clone reproducibility test
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
│   ├── placeholder.py                       # Lab 1 placeholder (no longer used)
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
├── .dockerignore                            # Keeps data/ and local files out of Docker builds
├── .gitignore                               # Files and folders git should not track
├── .Rprofile                                # Activates renv when R starts in this project
├── AI_USAGE.md                              # Log of AI assistance and how it was validated
├── Dockerfile                               # Container build: environment plus aadrkit
├── README.md                                # This file
├── environment.yml                          # Conda environment: Python, pandas, EIGENSOFT, pytest, aadrkit
├── project-hds.Rproj                        # RStudio project file
├── pyproject.toml                           # Package metadata; registers the `aadrkit` command
└── renv.lock                                # Exact R package versions
```

## R environment (Lab 1)
 
The R environment was set up for Lab 1 and is **not needed to use aadrkit**. To restore it, open `project-hds.Rproj` in RStudio (so renv activates), then in the R console: 
```r
renv::restore()
```
 
## Citation
 
If you use AADR data obtained with this tool, cite all three of the following:
 
1. **The AADR paper:** Mallick, S., Micco, A., Mah, M., Ringbauer, H., Lazaridis, I., Olalde, I., Patterson, N., & Reich, D. (2024). The Allen Ancient DNA Resource (AADR) a curated compendium of ancient human genomes. *Scientific Data*, 11(1). https://doi.org/10.1038/s41597-024-03031-7
2. **The dataset version you downloaded:** Mallick, Swapan; Reich, David, 2023, "The Allen Ancient DNA Resource (AADR): A curated compendium of ancient human genomes", https://doi.org/10.7910/DVN/FFIDCW, Harvard Dataverse, V14
3. **The original publications** for every individual included in your analysis. The AADR is a compilation of previously published data, and its authors state that citing the AADR is not a substitute for citing the original studies. The source publication for each individual is recorded in the `.anno` file and in `PREFIX_selected.tsv`.
