# Allen Ancient DNA Resource (AADR) Query and Subsetting Tool
[Explanation]

## Setup
Terms: 
- bash = your terminal (Git Bash, WSL, Command Prompt)
- R console = terminal within RStudio or running R in a terminal to move into an R prompt
- EIGENSOFT's `convertf` is required to read AADR's genotype files, and is only available after `conda activate aadr-project`. See `environment.yml`. 

### Python (conda)
In the bash terminal:
```bash
git clone https://github.com/nlinares-GWU2026/project-hds.git
cd project-hds
mamba env create -f environment.yml
conda activate aadr-project
python scripts/profile_anno.py
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

- **Dataset version:** 14.0
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

## Citation

If you use AADR data obtained with this tool, cite all three of the following:
1. **The AADR paper:** Mallick, S., Micco, A., Mah, M., Ringbauer, H., Lazaridis, I., Olalde, I., Patterson, N., & Reich, D. (2024). The Allen Ancient DNA Resource (AADR) a curated compendium of ancient human genomes. *Scientific Data*, 11(1). https://doi.org/10.1038/s41597-024-03031-7
2. **The dataset version you downloaded:** Mallick, Swapan; Reich, David, 2023, "The Allen Ancient DNA Resource (AADR): A curated compendium of ancient human genomes", https://doi.org/10.7910/DVN/FFIDCW, Harvard Dataverse, V14
3. **The original publications** for every individual included in your analysis. The AADR is a compilation of previously published data, and its authors state that citing the AADR is not a substitute for citing the original studies. The source publication for each individual is recorded in the `.anno` file.
