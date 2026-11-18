import pandas as pd
import pytest

from aadrkit.filters import (
    deduplicate_individuals,
    exclude_present_day,
    exclude_reference_genomes,
    filter_min_snps,
)
from aadrkit.query import select

def test_defaults_remove_references_and_duplicates(anno):
    selected, report = select(anno, verbose=False)
    ids = set(selected["genetic_id"])
    assert not any(i.endswith(".REF") for i in ids)
    assert selected["individual_id"].is_unique
    assert list(report["Step"]) == ["Exclude Reference Genomes", "One row per person"]
    assert report.loc[0, "Removed"] == 4

def test_only_requested_steps_run(anno):
    _, report = select(anno, min_snps=100000, verbose=False)
    assert list(report["Step"]) == [
        "Exclude Reference Genomes", "At least 100000 SNPs", "One row per person",
    ]

def test_matches_filter_applied_by_hand(anno): 
    selected, _ = select(anno, exclude_present=True, min_snps=20000, verbose=False)
    by_hand = deduplicate_individuals(
        filter_min_snps(exclude_present_day(exclude_reference_genomes(anno)), 20000)
    )
    pd.testing.assert_frame_equal(selected, by_hand)

def test_reports_missing_coordinates(anno):
    selected, report = select(anno, min_lat=-90, max_lat=90, min_lon=-180,
                              include_references=True, deduplicate=False, verbose=False)

    assert len(selected) == 23089 - 784
    assert report.loc[0, "Note"] == "784 had no coordinates"

def test_group_excludes_and_counts_outliers(anno):
    selected, report = select(anno, groups="Scotland_Viking", verbose=False)
    ids = set(selected["genetic_id"])
    assert "VK202.AG" in ids and "VK201.AG" not in ids
    assert report.loc[1, "Note"].endswith("outliers excluded")

def test_arguments_must_be_named(anno):
    with pytest.raises(TypeError):
        select(anno, 3000, 5000)
    with pytest.raises(TypeError):
        select(anno, min_snp=5000) # misspelled: min_snp, not min_snps