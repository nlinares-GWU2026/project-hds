# Fresh-clone reproducibility test

- **Date:** 2026-11-25
- **Computer:** Same as development of project. (ASUS Zenbook 14; Intel(R) Core(TM) Ultra 9 285H 2.9 GHz; 32 GB RAM, 128 MB Intel(R) Arc(TM) 140T GPU (16GB)
- **Commit tested:** 2d367ce (HEAD -> main, origin/main, origin/HEAD) Enhance README with Docker instructions and usage details

## Steps and results:
In terminal:
0. Setup:
`mkdir -p ~/fresh-test`
`cd ~/fresh-test`
1. Clone: 
`git clone https://github.com/nlinares-GWU2026/project-hds.git`
2. Environment: instead of "conda activate", used "mamba activate"
`cd project-hds`
`mamba env create -f environment.yml -n aadr-fresh`
`mamba activate aadr-fresh`
3. Tests without data:
`python -c "import aadrkit; print(aadrkit.__file__)"`
`pytest -m "not slow"` # 66 passed, 2 deselected
4. Data download and verification:
`mkdir -p data/raw`
`wget -O data/raw/v66.p1_1240K.aadr.PUB.anno "https://dataverse.harvard.edu/api/access/datafile/13994515"`
`wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.geno "https://dataverse.harvard.edu/api/access/datafile/13994829"`
`wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.snp "https://dataverse.harvard.edu/api/access/datafile/13994514"`
`wget -c -O data/raw/v66.p1_1240K.aadr.patch.PUB.ind "https://dataverse.harvard.edu/api/access/datafile/13994513"`
`sha256sum -c docs/data_checksums.txt`
5. Full test suite: 68 passed
`pytest -v`
6. Usage examples:
`aadrkit list country` # Listed all countries
`aadrkit list group_id` # Listed all group_id's
`aadrkit select --min-bp 1000 --max-bp 1500 --country "United Kingdom" --min-snps 100000`
```bash
Step  Rows_before  Rows_after  Removed Note Exclude Reference Genomes        23089       23085        4
Date range (min_bp = 1000, max_bp = 1500)        23085        3301    19784 
Country ['United Kingdom']         
3301         259     3042 
At least 100000 SNPs          
259         220       39
One row per person          220         208       12
```
`aadrkit select --group Scotland_Viking --out data/output/vikings --genotypes --format plink` 
```bash
Step  Rows_before  Rows_after  Removed                Note
Exclude Reference Genomes        23089       23085        4
Group ['Scotland_Viking']        23085           7    23078 3 outliers excluded
       One row per person            7           6        1
Selected 6 rows.
selected: data/output/vikings_selected.tsv
report: data/output/vikings_report.tsv
command: data/output/vikings_command.txt
geno: data/output/vikings.bed
snp: data/output/vikings.bim
ind: data/output/vikings.fam
selection_ind: data/output/vikings_selection.ind
par: data/output/vikings.par
log: data/output/vikings.log
```
`aadrkit select --group "_IA$" --group-regex --country Poland` 
```bash
Step  Rows_before  Rows_after  Removed                Note
Exclude Reference Genomes        23089       23085        4
       Country ['Poland']        23085         513    22572
           Group ['_IA$']          513         130      383 1 outliers excluded
       One row per person          130         129        1
Selected 129 rows.
```
7. Docker:
`docker build -t aadrkit-fresh .`
`docker run --rm aadrkit-fresh`

## Problems found and fixes
No issues found. Only change was the activation of the environment via mamba instead of conda. 
