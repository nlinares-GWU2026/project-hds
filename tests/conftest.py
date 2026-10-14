""" Shared pytest fixtures for the aadrkit test suite."""
from pathlib import Path
import pandas as pd
import pytest
from aadrkit.anno import load_anno

ROOT = Path(__file__).resolve().parent.parent
ANNO_PATH = ROOT / "data" / "raw" / "v66.p1_1240K.aadr.PUB.anno"
GROUND_TRUTH_PATH = ROOT / "tests" / "ground_truth.tsv"

@pytest.fixture(scope="session") # Instead of module
def anno():
    """The real AADR v66.p1 .anno file, loaded once for the whole test run."""
    if not ANNO_PATH.exists():
        pytest.skip("AADR .anno file not found; see README 'Data' section")
    return load_anno(ANNO_PATH)

@pytest.fixture(scope="session")
def ground_truth():
    """Ten individuals whose values were verified by hand with grep."""
    return pd.read_csv(
        GROUND_TRUTH_PATH, sep="\t", encoding="utf-8",
        keep_default_na=False, na_values=[".."],
    )