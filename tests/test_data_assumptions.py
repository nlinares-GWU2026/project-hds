from aadrkit.filters import is_outlier, base_group
import pandas as pd

"""Facts about AADR v66.p1 that aadrkit's design relies on.
These test the data, not the code. If they fail after switching to a 
different AADR release, revisit the design decisions in docs/anno_notes.md."""

def test_zero_bp_means_present_day(anno):
    """Every individual dated 0 BP is labeled 'present'."""
    at_zero = anno[anno["date_bp"] == 0]
    assert len(at_zero) == 3970 # Asserts there are exactly 3970 rows at 0 BP in release v66.p1
    assert (at_zero["full_date"] == "present").all() # .al() is true only if every value in the column is true

def test_reference_genomes(anno):
    """Exactly four rows are reference genomes, not individuals."""
    refs = anno[anno["genetic_id"].str.endswith(".REF")]
    assert sorted(refs["genetic_id"]) == [
        "Ancestor.REF", "Chimp.REF", "Gorilla.REF", "Href.REF"
    ]
    assert (refs["data_type"] == "Reference Genome").all()

def test_outlier_rule_matches_simple_search(anno):
    """The precise "-o" rule finds the same 499 groups as a plain text search."""
    groups = pd.Series(anno["group_id"].unique())
    precise = is_outlier(groups).sum()
    simple = groups.str.contains("-o", regex=False).sum()
    assert precise == simple == 499


def test_known_capitalization_differences_in_group_ids(anno):
    """v66.p1 has exactly one pair of Group IDs differing only by capitalization.
    
    Both are outliers of Hungary_EarlyAvar from the same study - the outlier 
    description is written "Low" in one and "low" in the other."""
    labels = anno["group_id"].dropna().drop_duplicates()
    collide = sorted(labels[labels.str.casefold().duplicated(keep=False)])
    assert collide == ["Hungary_EarlyAvar-oLowEastAsia", "Hungary_EarlyAvar-olowEastAsia"]

def test_base_groups_are_distinct_ignoring_capitalization(anno):
    """Case-insensitive matching never merges two different base groups.
    
    filter_group matches on base names (outlier suffix removed),
    the assumption that matters for flitering."""
    bases = base_group(anno["group_id"].dropna()).unique()
    assert len({b.casefold() for b in bases}) == len(bases)