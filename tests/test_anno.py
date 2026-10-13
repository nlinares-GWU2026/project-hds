from pathlib import Path
import pandas as pd
import pytest
from aadrkit.anno import COLUMN_PATTERNS, find_columns, load_anno
# Imports custom helper constants and functions (COLUMN_PATTERNS, find_columns, and load_anno from aadrkit.anno)

ROOT = Path(__file__).resolve().parent.parent
ANNO_PATH = ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno"

##### Tests that need  data #####
@pytest.fixture(scope="module") # Marks anno() as a reusable setup function that provides data or objects to test functions
# Any test with `anno` as an input automatically receives the loaded table
# `scope="module"` allows file to be reusable by every test in this file instead of being reloaded per test 
def anno():
    """Load the real .anno file once for all tests in this file"""
    if not ANNO_PATH.exists():
        pytest.skip("AADR .anno file not found. See README 'Data' section") # If someone runs test without having downloaded data, tests are marked as "skipped" instead of just failing
    return load_anno(ANNO_PATH)

##### Tests that need NO data #####
def test_find_columns_rejects_two_matches():
    with pytest.raises(ValueError):
        find_columns(["Genetic ID (copy 1)", "Genetic ID (copy 2)"])

def test_find_columns_rejects_missing_column():
    with pytest.raises(ValueError):
        find_columns(["Something unrelated"])

def test_find_columns_finds_every_pattern():
    """Every pattern is matched, not just the first one."""
    names = [
        "Genetic ID (suffixes...)", "Individual ID", "First publication: ...",
        "Publication abbreviation", "doi for publication ...", "Date mean in BP ...",
        "Full Date ...", "Group ID", "Political Entity", "Latitude", "Longitude",
        "Data type",
        "SNPs hit on autosomal targets (Computed using easystats on 1240k snpset)",
        "Y haplogroup  in ISOGG notation ...", "mtDNA haplogroup ...", "ASSESSMENT",
    ]
    assert len(find_columns(names)) == len(COLUMN_PATTERNS)

##### Tests on the real file #####
def test_shape(anno):
    assert anno.shape == (23089, len(COLUMN_PATTERNS))
# Checks the loaded df has exactly 23,089 rows and a column count equal to number of expected short names in COLUMN_PATTERNS

def test_short_column_names(anno):
    assert list(anno.columns) == list(COLUMN_PATTERNS)
# Asserts that the df column headers match the exact list and order of short alias keys defined in COLUMN_PATTERNS

def test_genetic_id_is_unique(anno):
    assert anno["genetic_id"].is_unique
# Asserts that every value in the "genetic_id" column is strictly unique with zero duplicate entries

def test_missing_marker_becomes_nan(anno):
    assert pd.api.types.is_float_dtype(anno["lat"])
    assert anno["lat"].isna().sum() == 784
# Checks that the lat column was converted to floating-point num data type 
# Asserts that AADR's placeholder missing markers were correctly replaced with NaN, yielding 784 missing latitude entries