# Allen Ancient DNA Resource (AADR) Query and Subsetting Tool

[Explanation]

## Setup
Terms: 
- bash = your terminal (Git Bash, WSL, Command Prompt)
- R console = terminal within RStudio or running R in a terminal to move into an R prompt

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

## Graduate Addendum: Environment Workflow Comparison
Setting up the conda environment was straightforward, following the Week 2 practical directly; I asked Claude to identify which bioconda package would be relevant for working with AADR data (my project’s actual use case, in place of samtools) and used Google’s AI-assisted search (aka Google) to confirm which pandas version was compatible with my installed Python version. I successfully deleted and recreated the environment purely from environment.yml, confirming it was reproducible. The renv workflow felt comparatively more fragile. It depends on opening the project through RStudio’s .Rproj file rather than working from a plain terminal, and I ran into more places where the setup could silently break. For example, package installs landing in the wrong library if the project was not properly activated. Given that I am also more experienced working in WSL/conda from prior coursework, I would lean toward conda or a similar Python-based tool for a real project, though I was ultimately able to get renv working. I was also able to complete a full deactivate and then restore to confirm the environment was reproducible.
