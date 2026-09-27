# Allen Ancient DNA Resource (AADR) Query and Subsetting Tool
[Explanation]

## Setup
Terms: 
- bash = your terminal (Git Bash, WSL, Command Prompt)
- R console = terminal within RStudio or running R in a terminal to move into an R prompt
- EIGENSOFT's `convertf ` is required to read AADR's genotype files, and is only available after `conda activate aadr-project`. See `environment.yml`. 

### Python (conda)
In the bash terminal:
```bash
git clone https://github.com/nlinares-GWU2026/project-hds.git
cd project-hds
mamba env create -f environment.yml
conda activate aadr-project
python src/placeholder.py
```

### R (renv)
In R or RStudio terminal:
```r
renv::restore()
source("src/placeholder.R")
```

### Docker (optional)
The Dockerfile is included in this repo.
In the bash terminal after installing and setting up Docker:
```bash
docker build -t aadr-project .
docker run --rm aadr-project
```
