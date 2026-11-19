"""Extract genotypes for selected individuals by running EIGENSOFT's convertf.

This module is aadrkit's "convertf backend": it is the only part of the package that 
reads AADR's genotype files. A different backend (for example, a pure Python .geno reader)
could replace it by providing the same extract_genotypes() function."""
import shutil
import subprocess
import pandas as pd
from pathlib import Path

# Output file suffixes for each convertf output format
OUTPUT_SUFFIXES = {
    "EIGENSTRAT": (".geno", ".snp", ".ind"),
    "PACKEDANCESTRYMAP": (".geno", ".snp", ".ind"),
    "PACKEDPED": (".bed", ".bim", ".fam"), # PLINK binary format
}

def read_ind(path): 
    """Read an EIGENSTRAT .ind file: one line per individual (ID, sex, population)."""
    return pd.read_csv(path, sep=r"\s+", header=None, # Reads the ind file, spaces or tabs between columns, file has no header row
                       names=["genetic_id", "sex", "population"], dtype=str) # keeps every value as text

def write_selection_ind(ind, genetic_ids, path):
    """Write a copy of `ind` where everyone not in `genetic_ids` is labelled "Ignore".
    
    Every line is kept, in the original order, because convertf matches the .ind lines 
    to the genotype file by position."""
    marked = ind.copy()
    marked.loc[~marked["genetic_id"].isin(genetic_ids), "population"] = "Ignore" # in rows whose ID is NOT selected, set the population column to Ignore (changing specific cells in pandas)
    marked.to_csv(path, sep=" ", header=False, index=False)
    return marked

def write_par(path, settings): 
    """Write a convertf parameter file, one "name: value" line per setting."""
    lines = [f"{name}: {value}" for name, value in settings.items()] # Turns a dict of settings into the "name: value" written by hand
    Path(path).write_text("\n".join(lines) +"\n") # joins the lines with line breaks and write the text to file

def extract_genotypes(selected, geno, snp, ind, out_prefix, output_format="EIGENSTRAT"): # Checks everything in order before running a slow step
    """Write genotype files containing only the individuals in `selected`.
    
    `selected` is a table from select() or the filters (it needs a genetic_id column). 
    `geno`, `snp, `ind` are the AADR genotype files. Outputs are written as out_prefix + suffix.
    The modfied .ind, the parameter file, and convertf's log are kept next to them as a record of exactly
    how the files were made. Returns a dict of output paths."""

    if output_format not in OUTPUT_SUFFIXES: # Checks an unknown output format 
        raise ValueError(f"output_format must be one of {sorted(OUTPUT_SUFFIXES)}, "
                         f"got {output_format!r}")
    for path in (geno, snp, ind, out_prefix):
        if any(ch.isspace() for ch in str(path)):
            raise ValueError (f"convertf cannot handle paths containing spaces: {path}."
                              f"Move the files (or the project) to a folder without spaces.")
        
    if shutil.which("convertf") is None: # Checks if convertf is not available
        raise RuntimeError("convertf not found; run `conda activate aadr-project` first")
    for path in (geno, snp, ind): # Checks if any of the 3 input files are missing
        if not Path(path).exists():
            raise FileNotFoundError(path)

    ids = set(selected["genetic_id"])
    if not ids: # Checks if there is empty selection
        raise ValueError("No individuals selected")
    full_ind = read_ind(ind)
    missing = ids - set(full_ind["genetic_id"])
    if missing: # Checks that selected IDs are not in the .ind, meaning the .anno and genotype files do not belong together
        raise ValueError(f"{len(missing)} selected IDs are not in {ind}, "
                         f"e.g. {sorted(missing)[:5]}")

    out_prefix = Path(out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True) # Creates any missing parent folders and if already exists, passes
    geno_suffix, snp_suffix, ind_suffix = OUTPUT_SUFFIXES[output_format]
    outputs = {
        "geno": f"{out_prefix}{geno_suffix}",
        "snp": f"{out_prefix}{snp_suffix}",
        "ind": f"{out_prefix}{ind_suffix}",
        "selection_ind": f"{out_prefix}_selection.ind",
        "par": f"{out_prefix}.par",
        "log": f"{out_prefix}.log",
    } # Builds all the outpaths into one dictionary so function returns all together

    write_selection_ind(full_ind, ids, outputs["selection_ind"])
    write_par(outputs["par"], {
        "genotypename": geno,
        "snpname": snp,
        "indivname": outputs["selection_ind"],
        "outputformat": output_format,
        "genotypeoutname": outputs["geno"],
        "snpoutname": outputs["snp"],
        "indivoutname": outputs["ind"],
        "hashcheck": "NO",
    }) # Writes the selection .ind and the parameter file using same settings as `convertf_test.par`

    result = subprocess.run(["convertf", "-p", outputs["par"]],
                            capture_output=True, text=True) # Program and argument separate items, collects what convertf prints and returns as text vs raw bytes
    Path(outputs["log"]).write_text(result.stdout + result.stderr) # Output is saved to a log file regardless if successful
    if result.returncode != 0:
        raise RuntimeError(f"convertf failed (exit code {result.returncode}); "
                           f"see {outputs['log']}") # Exit code: 0 means success and anything else means it failed, description of failure in the log

    with open(outputs["ind"]) as handle:
        n_out = sum(1 for _ in handle) # Counts the lines in the output individual file 
    if n_out != len(ids): # Output must equal the number selected which catches failure even if exit code 0
        raise RuntimeError(f"Expected {len(ids)} individuals in {outputs['ind']}, "
                           f"found {n_out}")
    return outputs # Checks the result