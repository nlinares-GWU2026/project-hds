import pandas as pd
import pytest

from aadrkit.anno import list_values
from aadrkit.filters import (
    base_group,
    deduplicate_individuals,
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
    filter_date_range,
    filter_group,
    filter_min_snps,
    is_outlier,
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

@pytest.fixture
def places(): # A and B: Spain vs Canary Islands, C: Secondary country for testing lists, D and E: Tonga and Vanuatu on opposite sides of 180 line, F: missing everything, G: country but no coordinates
    """A tiny hand-made table covering the region edge cases."""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "F", "G"],
        "country": ["Spain", "Canary Islands", "United Kingdom", "Tonga",
                    "Vanuatu", float("nan"), "Uzbekistan"],
        "lat": [40.0, 28.0, 59.1, -21.2, -15.4, float("nan"), float("nan")],
        "lon": [-3.0, -15.5, -3.0, -175.2, 167.0, float("nan"), float("nan")],
    })

# Region: toy table tests

def test_country_ignores_capitalization_and_territories(places):
    assert list(filter_country(places, "spain")["genetic_id"]) == ["A"]


def test_country_accepts_a_list(places):
    result = filter_country(places, ["Spain", "United Kingdom"])
    assert list(result["genetic_id"]) == ["A", "C"]


def test_country_finds_individuals_without_coordinates(places):
    assert list(filter_country(places, "Uzbekistan")["genetic_id"]) == ["G"]


def test_country_warns_about_unknown_names(places):
    with pytest.warns(UserWarning, match="spian"):
        result = filter_country(places, "Spian")
    assert result.empty


def test_bounding_box_basic(places):
    result = filter_bounding_box(places, min_lat=35, max_lat=60, min_lon=-10, max_lon=0)
    assert list(result["genetic_id"]) == ["A", "C"]


def test_bounding_box_crosses_180_degrees(places):
    result = filter_bounding_box(places, min_lon=160, max_lon=-170)
    assert list(result["genetic_id"]) == ["D", "E"]


def test_bounding_box_rejects_invalid_bounds(places):
    with pytest.raises(ValueError):
        filter_bounding_box(places, min_lat=-100)
    with pytest.raises(ValueError):
        filter_bounding_box(places, min_lat=60, max_lat=35)

# Region: real data tests

def test_country_on_real_data(anno):
    spain = filter_country(anno, "Spain")
    assert len(spain) == list_values(anno, "country")["Spain"] == 802
    assert "gun005.SG" not in set(spain["genetic_id"])               # Canary Islands
    assert "gun005.SG" in set(filter_country(anno, "canary islands")["genetic_id"])


def test_whole_world_box_excludes_missing_coordinates(anno):
    world = filter_bounding_box(anno, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180)
    assert len(world) == 23089 - 784
    assert not {"I8508.AG", "Khwit.SG", "Chimp.REF"} & set(world["genetic_id"])



@pytest.fixture
def pops(): # A = plain group, B = same group w bare outlier suffix, C = different viking gorup for pattern matching, D = tests anchoring with $,
    # E = outlier with a description after the suffix, F = E's base group, G = another described outlier
    """A tiny hand-made table covering the population edge cases."""
    return pd.DataFrame({
        "genetic_id": ["A", "B", "C", "D", "E", "F", "G"],
        "group_id": ["Scotland_Viking", "Scotland_Viking-o", "Sweden_Viking",
                     "Poland_IA", "England_BellBeaker-ohighEEF",
                     "England_BellBeaker", "Russia_Karasuk-oAegean"],
    })

# Population: toy table tests

def test_base_group_strips_outlier_suffix(pops): # checked row by row including the suffixes
    assert list(base_group(pops["group_id"])) == [
        "Scotland_Viking", "Scotland_Viking", "Sweden_Viking", "Poland_IA",
        "England_BellBeaker", "England_BellBeaker", "Russia_Karasuk",
    ]

def test_is_outlier(pops):  # checked row by row including the suffixes
    assert list(is_outlier(pops["group_id"])) == [False, True, False, False, True, False, True]

def test_group_exact_excludes_outliers(pops): # excludes outliers by default (only A) and includes them on request (A and B)
    # "Viking" matches no group exactly on its own, so the result is empty and a warning names what failed
    assert list(filter_group(pops, "Scotland_Viking")["genetic_id"]) == ["A"]

def test_group_exact_can_include_outliers(pops): # excludes outliers by default (only A) and includes them on request (A and B)
    # finds both Scottish and Swedish Vikings, adds outlier only when asked
    result = filter_group(pops, "Scotland_Viking", include_outliers=True)
    assert list(result["genetic_id"]) == ["A", "B"]

def test_group_exact_ignores_capitalization(pops): # finds both Scottish and Swedish Vikings, adds outlier only when asked
    assert list(filter_group(pops, "scotland_VIKING")["genetic_id"]) == ["A"]

def test_group_exact_does_not_match_partial_names(pops):
    with pytest.warns(UserWarning, match="viking"):
        result = filter_group(pops, "Viking")
    assert result.empty

def test_group_regex_contains(pops): # finds both Scottish and Swedish Vikings, adds outlier only when asked
    assert list(filter_group(pops, "Viking", regex=True)["genetic_id"]) == ["A", "C"]
    result = filter_group(pops, "Viking", regex=True, include_outliers=True)
    assert list(result["genetic_id"]) == ["A", "B", "C"]

def test_group_regex_keeps_outlier_descriptions_with_their_group(pops):
    result = filter_group(pops, "BellBeaker", regex=True, include_outliers=True)
    assert list(result["genetic_id"]) == ["E", "F"]

def test_group_regex_anchored_end(pops): # Finds names only ending in _IA
    assert list(filter_group(pops, "_IA$", regex=True)["genetic_id"]) == ["D"]

def test_group_regex_warns_when_nothing_matches(pops):
    with pytest.warns(UserWarning, match="Neanderthal"):
        result = filter_group(pops, "Neanderthal", regex=True)
    assert result.empty

# Population: real data test

def test_group_on_real_data(anno):
    default = set(filter_group(anno, "Scotland_Viking")["genetic_id"])
    with_outliers = set(filter_group(anno, "Scotland_Viking", include_outliers=True)["genetic_id"])
    assert "VK202.AG" in default and "VK201.AG" not in default
    assert {"VK202.AG", "VK201.AG"} <= with_outliers



@pytest.fixture
def reps(): # Covers each deduplication rule 
    """Repeated individuals, a tie, and rows without an Individual ID."""
    return pd.DataFrame({
        "genetic_id": ["P1.AG", "P1.SG", "P2.AG", "P3.AG", "P3.TW", "X.AG", "Y.AG"],
        "individual_id": ["P1", "P1", "P2", "P3", "P3", float("nan"), float("nan")],
        "snps_1240k": [500, 900, 300, 700, 700, 100, 200],
    })

# Coverage and deduplication toy-table tests

def test_min_snps_is_inclusive(reps):
    assert list(filter_min_snps(reps, 700)["genetic_id"]) == ["P1.SG", "P3.AG", "P3.TW"]

def test_min_snps_rejects_negative(reps):
    with pytest.raises(ValueError):
        filter_min_snps(reps, -1)

def test_dedupe_keeps_highest_coverage_row(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert "P1.SG" in ids and "P1.AG" not in ids

def test_dedupe_breaks_ties_by_genetic_id(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert "P3.AG" in ids and "P3.TW" not in ids

def test_dedupe_keeps_rows_without_individual_id(reps):
    ids = set(deduplicate_individuals(reps)["genetic_id"])
    assert {"X.AG", "Y.AG"} <= ids

def test_dedupe_preserves_original_order(reps):
    assert list(deduplicate_individuals(reps)["genetic_id"]) == [
        "P1.SG", "P2.AG", "P3.AG", "X.AG", "Y.AG",
    ]

# Coverage and deduplication: real-data tests

def test_min_snps_on_real_data(anno):
    assert "I13976.SG" in set(filter_min_snps(anno, 281)["genetic_id"])       # exactly 281
    assert "I13976.SG" not in set(filter_min_snps(anno, 282)["genetic_id"])

def test_dedupe_on_real_data(anno):
    result = deduplicate_individuals(anno)
    assert len(result) == 21433
    ych = result[result["individual_id"] == "YCH017"]
    assert list(ych["genetic_id"]) == ["YCH017.AG"]
