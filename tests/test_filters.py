import pandas as pd
import pytest

from aadrkit.filters import (
    exclude_present_day,
    exclude_reference_genomes,
    filter_date_range,
)

@pytest.fixture
def toy():
    """A tiny hand-made table covering the edge cases"""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "Ref.REF"],
        "date_bp": [ 0, -4, 1000, 1500, float("nan"), 0], # Matched to A, B, C, D, E, Ref.REF
    })

# Toy-table tests 
def test_date_range_bounds_are_inclusive(toy): # accepts toy df
    result = filter_date_range(toy, min_bp=1000, max_bp=1500) # filters toy table for samples dated between 1000 and 1500 BP
    assert list(result["genetic_id"]) == ["C", "D"] # both boundary values retained matching C and D

def test_date_range_one_sided(toy): 
    assert list(filter_date_range(toy, min_bp=1000)["genetic_id"]) == ["C", "D"] # asserts that passing only min_bp=1000 keeps all samples dated >= 1000 BP
    assert list(filter_date_range(toy, max_bp=0)["genetic_id"]) == ["A", "B", "Ref.REF"] # asserts that passing only max_bp=0 keeps all samples dated <= 0 BP 

def test_date_range_without_bounds_keeps_everything(toy): # asserts that calling filter_date_range without bounds specified leaves the table unchanged and returns all 6 original rows
    assert len(filter_date_range(toy)) == len(toy)

def test_date_range_rejects_reversed_bounds(toy):
    with pytest.raises(ValueError):
        filter_date_range(toy, min_bp=5000, max_bp=3000)

def test_exclude_present_day_keeps_post_1950_and_missing(toy): # asserts that 
    assert list(exclude_present_day(toy)["genetic_id"]) == ["B", "C", "D", "E"] # asserts that exclude_present_day removes 0 BP entries like A nad Ref.REF but preserves
    # negative post-1950 dates (B or -4 BP, ancient samples C and D, and misisng dates)

def test_exclude_reference_genome(toy):
    assert list(exclude_reference_genomes(toy)["genetic_id"]) == ["A", "B", "C", "D", "E"]

# Real data tests using verified individuals (by hand verified)
def test_date_range_on_real_data(anno): # accepts real anno dataset fixture
    ids = set(filter_date_range(anno, min_bp=1000, max_bp=1500)["genetic_id"]) # filters the real AADR dataset for samples dated between 1000 BP and 1500 BP and converts the resulting genetic IDs to a set
    assert {"VK202.AG", "VK201.AG", "YCH017.AG"} <= ids # 1000, 1460, 1075 BP | uses subest comparison (<=) to assert that known in-range samples are present in filtered set
    assert not {"gun005.SG", "I8508.AG", "NA20813.DG"} & ids # 992, 6356, 0 BP | uses set intersection (&) to assert that out of range samples are excluded

def test_exclude_present_day_on_real_data(anno):
    result = exclude_present_day(anno) # runs exclude_present_day on the real AADR dataset 
    ids = set(result["genetic_id"]) # and converts remaining IDs to a set
    assert len(result) == 23089 - 3970 # asserts the total row count equals 23,089 - 3,970 (removing exactly the 3,970 present day 0 BP individuals)
    assert "Khwit.SG" in ids # -4 BP retained
    assert not {"NA20813.DG", "JHF05.AG", "Chimp.REF"} & ids # asserts that present day controls and ref genomes are excluded 