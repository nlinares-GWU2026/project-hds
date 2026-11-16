import pandas as pd
import pytest

from aadrkit.anno import list_values
from aadrkit.filters import (
    exclude_present_day,
    exclude_reference_genomes,
    filter_bounding_box,
    filter_country,
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

@pytest.fixture
def places():
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