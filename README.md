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
wget -O data/raw/v66.p1_1240K.aadr.PUB.anno "https://dataverse.harvard.edu/api/access/datafile/13994515"
```

### Verify 
```bash
sha256sum -c docs/data_checksums.txt
```
Expected output: data/raw/v66.p1_1240K.aadr.PUB.anno: OK`. The file's MD5 checksum (`a2db1ac16f0f3558ed66fb251e1d5c7d`) also matches the value listed on its Dataverse page.

[Download instructions for the genotype files (`.geno`, `.snp`, `.ind`) will be added when `convertf` integration begins.]

## Check Everything Works
In terminal:
```bash
python scripts/profile_anno.py
```

## Repository Layout
project-hds/
├── docs/                                      # Project report, proposal, documentation, notes
│   ├── Nicole_Linares_Proposal_HDS.pdf        # Individual project proposal
│   ├── Linares_Dunkel-Bayogha_Proposal_HDS.pdf (REMOVE)
│   ├── anno_notes.md                          # Dataset and project progress notes
│   ├── data_checksums.md                      # Verification hashes (MD5/SHA256) to ensure raw data integrity
│   └── lab1-addendum.md                       # Temporary lab submission addendum TO REMOVE AFTER SEMESTER 
├── renv/                                      # R environment configuration files managed by the renv package                 
│   ├── .gitignore                             # Prevents committing local renv library builds and binaries to Git
│   ├── activate.R                             # R script that automatically initializes the project's renv environment
│   └── settings.json                          # Configuration settings for renv project behaviors
├── scripts/                                   # Executable Python scripts for data processing and analysis                  
│   ├── count_suffixes.py                      # Utility script counting file extensions/suffixes across project files 
│   ├── explore_anno.py                        # Exploratory script analyzing sample metadata in the annotation file
│   ├── find_test_indiv.py                     # Script to locate representative test individuals for validation filtering
│   ├── profile_anno.py                        # Main profiling script inspecting column missingness, data types, and value counts
│   └── profile_ids.py                         # Script verifying unique individual IDs across AADR metadata files
├── tests/                                     # Test suites and reference data used to validate code accuracy
│   └── ground_truth.tsv                       # Reference dataset containing expected results to check filtering logic
├── .Rprofile                                  # R startup script that auto-loads project settings and activates renv
├── .gitignore                                 # Specifies intentional untracked files and folders to exclude from Git
├── AI_USAGE.md                                # Documentation logging AI assistance and usage throughout the project
├── Dockerfile                                 # Instructions to build a containerized environment reproducing the setup
├── README.md                                  # Project documentation and setup (this file)
├── environment.yml                            # Conda environment definition listing Python and system dependencies
├── project-hds.Rproj                          # RStudio project file for organizing workspace settings
└── renv.lock                                  Dependency lockfile tracking exact R package versions for reproducibility           

## Citation

If you use AADR data obtained with this tool, cite all three of the following:
1. **The AADR paper:** Mallick, S., Micco, A., Mah, M., Ringbauer, H., Lazaridis, I., Olalde, I., Patterson, N., & Reich, D. (2024). The Allen Ancient DNA Resource (AADR) a curated compendium of ancient human genomes. *Scientific Data*, 11(1). https://doi.org/10.1038/s41597-024-03031-7
2. **The dataset version you downloaded:** Mallick, Swapan; Reich, David, 2023, "The Allen Ancient DNA Resource (AADR): A curated compendium of ancient human genomes", https://doi.org/10.7910/DVN/FFIDCW, Harvard Dataverse, V14
3. **The original publications** for every individual included in your analysis. The AADR is a compilation of previously published data, and its authors state that citing the AADR is not a substitute for citing the original studies. The source publication for each individual is recorded in the `.anno` file.
