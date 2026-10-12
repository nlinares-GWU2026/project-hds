""" Load the AADR annotation (.anno) file into a tidy pandas DataFrame.
Column patterns were written for AADR release v66.p1 (1240K panel)."""

import re
from pathlib import Path
import pandas as pd

# Short name: Regex matching the start of the real column name
# Each pattern must match exactly ONE column, or load_anno() raises an error

COLUMN_PATTERNS = {
    "genetic_id": r"Genetic ID", # raw string passed to Regex untouched instead of being interpreted first, ignore escape seqs & backslashes
    "individual_id": r"Individual ID$", # "$" matches end of string
    "first_publication": r"First publication",
    "publication": r"Publication abbreviations$",
    "doi": r"doi for publication",
    "date_bp": r"Date mean in BP",
    "full_date": r"Full Date",
    "group_id": r"Group ID$",
    "country": r"Political Entity$",
    "lat": r"Latitude$",
    "lon": r"Longitude$",
    "data_type": r"Data type$",
    "snps_1240k": r"SNPs hit on autosomal targets .*on 1240k snpset", # "." matches any single char except for newline, "*" matches zer or more of preceding element,
    # ".*" means wildcard that matches anything of any length then "on"
    "y_haplogroup": r"Y haplogroup\s+in ISOGG", # matches one or more whitespace chars
    "mt_haplogroup": r"mtDNA haplogroup",
    "assessment": r"ASSESSMENT$",
}

# AADR writes missing values as "..". Empty cells are also missing.
MISSING_VALUES = ["..", ""]

def find_columns(names):
    """Map each short name to exactly one real column name.
    Raises ValueError if any pattern matches zero or several columns."""

    found = {} # empty dict to store the final mapped pairs 
    for short, pattern in COLUMN_PATTERNS.items(): #
        matches = [name for name in names if re.match(pattern, name.strip())] # Searches through all candidate header strings in names,
        # removes any leading or trailing whitespace before matching, checks if regex pattern matches the stripped column name starting from beginning of string, then collects name from names that matches into list of matches
        if len(matches) != 1:
            raise ValueError(
                f"Expected 1 column matching {pattern!r} for '{short}', "
                f"found {len(matches)}: {matches}"
            )
        found[short] = matches[0]
        return found

def load_anno(path):
    """Read an AADR .anno file and return the key columns under short names. 
    
    AADR's missing value marker ".." and empty cells become NaN. pandas' other default missing 
    missing value strings are deliberately not applied, so real values are never mistaken for missing ones."""

    raw = pd.read_csv(
        Path(path), sep="\t", encoding="utf-8", low_memory=False,
        keep_default_na=False, na_values=MISSING_VALUES, 
    )
    columns = find_columns(raw.columns) # Calls the find_columns helper function passing list of full column headers from the raw file
    # Returns dict where keys are short aliases and values are the actual header names found in file
    anno = raw[list(columns.values())].copy()
    anno.columns = list(columns.keys())
    return anno
    # Filters raw to extract only the target columns and creates independent copy of that df subset
    # Renames subsetted columns from their original long names to clean short aliases
    