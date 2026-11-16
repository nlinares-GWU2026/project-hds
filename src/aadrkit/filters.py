"""Filter functions for AADR annotation tables returned by load_anno().

Each function takes a DataFrame and returns a new, filtered DataFrame,
so filters can be combined in any order.
"""
import pandas as pd
import warnings


def filter_date_range(anno, min_bp=None, max_bp=None):
    """Keep individuals whose mean date (years BP) is within [min_bp, max_bp].

    BP means "before present", where present = 1950 CE, so larger numbers
    are older. Both bounds are inclusive, and either can be None for no
    limit. Individuals with a missing date are excluded whenever a bound
    is given.
    """
    if min_bp is not None and max_bp is not None and min_bp > max_bp:
        raise ValueError(f"min_bp ({min_bp}) is greater than max_bp ({max_bp})")
    keep = pd.Series(True, index=anno.index)
    if min_bp is not None:
        keep &= anno["date_bp"] >= min_bp
    if max_bp is not None:
        keep &= anno["date_bp"] <= max_bp
    return anno[keep]


def exclude_present_day(anno):
    """Remove present-day individuals (date_bp == 0, labeled "present" in AADR).

    Individuals dated after 1950 CE (negative BP, such as 1954 CE) are kept,
    because they have a real historical date rather than "present".
    """
    return anno[anno["date_bp"] != 0]


def exclude_reference_genomes(anno):
    """Remove reference genomes (Genetic IDs ending in ".REF"), which are not individuals."""
    return anno[~anno["genetic_id"].str.endswith(".REF")]

def filter_country(anno, countries):
    """Keep individuals whose country (AADR "Political Entity) is in `countries`.
    
    `countries` can be one name or a list of names. Matching ignores capitalization but is 
    otherwise exact: AADR records some territories separately (for example, "Canary Islands" is not part of "Spain").
    Use list_values(anno, "country") to see the available labels. Rows with a missing country are never kept."""

    if isinstance(countries, str):
        countries = [countries]
    wanted = {c.strip().casefold() for c in countries}
    present = anno["country"].str.casefold()
    for name in sorted(wanted - set(present.dropna())):
        warnings.warn(
            f"No rows with country {name!r}; check spelling with "
            f"list_values(anno, 'country')",
            UserWarning,
            stacklevel=2,
        )
    return anno[present.isin(wanted)]

def filter_bouding_box(anno, min_lat=None, max_lat=None, min_lon=None, max_lon=None):
    """Keep individuals whose coordinates fall inside a latitude/longitude box.
    
    Bounds are inclusive, and any bound can be None for no limit. If min_long is 
    greater than max_lon, the box crosses the 180-degree line. Individuals with missing
    coordinates are excluded whenever a bound is given. 
    """

    for name, value, limit in [("min_lat", min_lat, 90), ("max_lat", max_lat, 90),
                               ("min_lon", min_lon, 180), ("max_lon", max_lon, 180)]:
        if value is not None and not -limit <= value <= limit:
            raise ValueError(f"{name} must be between {-limit} and {limit}, got {value}")
    if min_lat is not None and max_lat is not None and min_lat > max_lat:
        raise ValueError(f"min_lat ({min_lat}) is greater than max_lat ({max_lat})")

    keep = pd.Series(True, index=anno.index)
    if min_lat is not None:
        keep &= anno["lat"] >= min_lat
    if max_lat is not None:
        keep &= anno["lat"] <= max_lat
    if min_lon is not None and max_lon is not None and min_lon > max_lon:
        keep &= (anno["lon"] >= min_lon) | (anno["lon"] <= max_lon)
    else:
        if min_lon is not None:
            keep &= anno["lon"] >= min_lon
        if max_lon is not None:
            keep &= anno["lon"] <= max_lon
    return anno[keep]