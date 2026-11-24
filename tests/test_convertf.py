import pandas as pd
import pytest
from aadrkit.convertf import extract_genotypes, read_ind, write_par, write_selection_ind
from pathlib import Path

# Fast tests: no convertf needed
def test_selection_ind_keeps_every_line_in_order(tmp_path): # tmp_path is empty temp folder for each test
    ind = pd.DataFrame({"genetic_id": ["A", "B", "C"],
                        "sex": ["M", "F", "U"],
                        "population": ["P1", "P2", "P3"]})
    path = tmp_path / "selection.ind"
    write_selection_ind(ind, {"B"}, path)
    assert path.read_text().splitlines() == ["A M Ignore", "B F P2", "C U Ignore"]
    # Only B keeps its real population, every line is still there and the order hasn't changed

def test_write_par(tmp_path):
    path = tmp_path / "test.par"
    write_par(path, {"genotypename": "in.geno", "hashcheck": "NO"})
    assert path.read_text() == "genotypename: in.geno\nhashcheck: NO\n"
    # Exact text that gets written, line breaks included

def test_rejects_unknown_output_format(tmp_path):
    selected = pd.DataFrame({"genetic_id": ["A"]})
    with pytest.raises(ValueError):
        extract_genotypes(selected, "x.geno", "x.snp", "x.ind",
                          tmp_path / "out", output_format="VCF")
        # Unknown format like VCF is rejected before anything else happens

def test_rejects_paths_with_spaces(tmp_path):
    selected = pd.DataFrame({"genetic_id": ["A"]})
    with pytest.raises(ValueError, match="spaces"):
        extract_genotypes(selected, "my data/x.geno", "x.snp", "x.ind", tmp_path / "out")

# Slow test: runs convertf on the real genotype file 
@pytest.mark.slow # Applies marker for longer tests 
def test_extracts_correct_genotypes(genotype_files, ground_truth, tmp_path):
    """ Repeats the manual check: called SNPs per person match .anno."""
    ids = ["VK202.AG", "NA20813.DG", "I13976.SG"]
    out = extract_genotypes(pd.DataFrame({"genetic_id": ids}), *genotype_files,
                            tmp_path / "test") # Unpacks the three paths into three separate arguments
    out_ids = read_ind(out["ind"])["genetic_id"].tolist() # Extracts the same three individuals as before 
    assert sorted(out_ids) == sorted(ids) # Check that exactly those three came out

    # Recounts each person's non-missing autosomal genotypes
    chrom = pd.read_csv(out["snp"],  sep=r"\s+", header=None, usecols=[1])[1] # reads only the chromosome column of .snp
    geno = pd.read_csv(out["geno"], header=None, dtype=str)[0] # Without this, pandas would read a like like 029 as 29 dropping the leading zeros and every person genotype would shift by one position
    autosomal = geno[chrom <= 22] # Keeps the autosomes
    expected = ground_truth.set_index("genetic_id")["snps_1240k"]
    for i, gid in enumerate(out_ids):
        called = (autosomal.str[i] != "9").sum() # takes the ith char of every line, which is person i's genotype
        assert called == expected[gid], gid # If it fails, pytest shows which individual's count was wrong
        # Each count must equal that person's snps_1240k value from the hand verified ground truth
        


@pytest.mark.slow
def test_extracts_plink_files(genotype_files, tmp_path):
    """PLINK output: Genetic IDs in the .fam column 2, sex coded 1/2, .bed has the right size."""
    ids = ["VK202.AG", "NA20813.DG", "I13976.SG"]
    out = extract_genotypes(pd.DataFrame({"genetic_id": ids}), *genotype_files,
                            tmp_path / "test", output_format="PACKEDPED") # Requests PLINK output, returned output still uses keys "geno", "snp", "ind" but they now point to .bed, .bim, .fam

    fam = pd.read_csv(out["ind"], sep=r"\s+", header=None, dtype=str)
    sex = dict(zip(fam[1], fam[4])) # Second and fifth columns, Genetic ID and sex code - pandas counts from 0
    # Pairs each ID with its sex code. zip walks 2 columns side by side, dict turns pairs into lookup table
    # Comparing whole dictionaries checks every person's sex in one assertion, regardless of row order
    assert sex == {"VK202.AG": "1", "NA20813.DG": "2", "I13976.SG": "2"}

    with open(out["snp"]) as handle:
        n_snps = sum(1 for _ in handle)
    assert n_snps == 1233013 # .bim line counts must be the full 1,233,013 SNPs, the same number reported by convertf

    bytes_per_snp = (len(ids) + 3) // 4 # "Round up" division, 3 people gives 1 byte per SNP, 5 people would give 2
    assert Path(out["geno"]).stat().st_size == 3 + n_snps * bytes_per_snp