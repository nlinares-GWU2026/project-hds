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

    if isinstance(countries, str): # Checks whether user passed single name like "Spain" instead of a list. If so, wrapped in a list. 
        # Prevents Python from treating the string as a sequence of letters 
        countries = [countries]
    wanted = {c.strip().casefold() for c in countries} # Set comprehension. Accidental spaces, conversion to lowercase for each name
    present = anno["country"].str.casefold()
    for name in sorted(wanted - set(present.dropna())): # Country column converted to lowercase so both sides of the comparison use the same capitalization
        # Set subtraction, requested names that don't appear in the table at all
        warnings.warn( # For each one, issues a warning that points user to list_values
            f"No rows with country {name!r}; check spelling with "
            f"list_values(anno, 'country')",
            UserWarning,
            stacklevel=2, # Warning points to user's own line that called filter_country
        )
    return anno[present.isin(wanted)] # Is true for rows whose country is in the requested set. Missing countries are never in the set so rows never kept. 

def filter_bounding_box(anno, min_lat=None, max_lat=None, min_lon=None, max_lon=None):
    """Keep individuals whose coordinates fall inside a latitude/longitude box.
    
    Bounds are inclusive, and any bound can be None for no limit. If min_long is 
    greater than max_lon, the box crosses the 180-degree line. Individuals with missing
    coordinates are excluded whenever a bound is given. 
    """

    for name, value, limit in [("min_lat", min_lat, 90), ("max_lat", max_lat, 90),
                               ("min_lon", min_lon, 180), ("max_lon", max_lon, 180)]: # Checks each given bound against its legal range
        if value is not None and not -limit <= value <= limit:
            raise ValueError(f"{name} must be between {-limit} and {limit}, got {value}")
    if min_lat is not None and max_lat is not None and min_lat > max_lat:
        raise ValueError(f"min_lat ({min_lat}) is greater than max_lat ({max_lat})")

    keep = pd.Series(True, index=anno.index) # Start with all True and narrow with &=
    if min_lat is not None:
        keep &= anno["lat"] >= min_lat
    if max_lat is not None:
        keep &= anno["lat"] <= max_lat
    if min_lon is not None and max_lon is not None and min_lon > max_lon: # If min_lon > max_lon, the box crosses the 180 deg line, so a row is kept if it's on either side. Otherwise, its an ordinary range handled like lat
        keep &= (anno["lon"] >= min_lon) | (anno["lon"] <= max_lon)
    else:
        if min_lon is not None:
            keep &= anno["lon"] >= min_lon
        if max_lon is not None:
            keep &= anno["lon"] <= max_lon
    return anno[keep]

# Outlier groups end in "-o", optionally followed by a description with no underscore, like "Scotland_Viking-o" or "England_BellBeaker-ohighEEF"
OUTLIER_SUFFIX = r"-o[^_]*$" # every function uses the same definition

def is_outlier(group_ids): # Returns True/False for each Group ID
    """True for each Group ID marked as a population-genetic outlier ("-o" suffix)."""
    return group_ids.str.contains(OUTLIER_SUFFIX, regex=True, na=False) # checks whether the pattern appears and treats missing Group ID as not an outlier, 
    # rather than producing a missing value that would break T/F logic later

def base_group(group_ids): # Uses the OUTLIER_SUFFIX rule to replace the suffix with nothing, removing it. Names without a suffix are unchanged.
    """Remove any outlier suffix: "England_BellBeaker-ohighEEF" -> "England_BellBeaker".""" 
    return group_ids.str.replace(OUTLIER_SUFFIX, "", regex=True)

def filter_group(anno, groups, include_outliers=False, regex=False):
    """Keep individuals whose population label (AADR "Group ID") matches `groups`.

    Matching uses the base group name, with any outlier suffix ("-o", "-ohighEEF", ...) removed,
    and ignores capitalization. Outliers are excluded unless include_outliers=True.

    regex=False: `groups` are exact base names, like "Scotland_Viking".
    regex=True: `groups` are regular-expression patterns searched within the base name, like "_IA$" (ends with "_IA") or "Viking" (contains "Viking").
    `groups` can be one name/pattern or a list.
    """

    if isinstance(groups, str): # Single name handling (same as filter_country)
        groups  = [groups]
    base = base_group(anno["group_id"]).str.casefold() # Holds every row's base group in lower case

    if regex:
        keep = pd.Series(False, index=anno.index) # Starts with keeping all as False because each pattern adds matches (opposite of the date and region filters which start with everything and narrow down)
        for pattern in groups:
            hits = base.str.contains(pattern, case=False, regex=True, na=False) # For each pettern, finds the base names containing it
            if not hits.any(): # If pattern matches nothing, a warning is issued
                warnings.warn(f"Pattern {pattern!r} matched no groups", UserWarning, stacklevel=2)
            keep |= hits
    else:
        wanted = {g.strip().casefold() for g in groups}
        for name in sorted(wanted - set(base.dropna())):
            warnings.warn( # Reminds users to give the name without a suffix, since typing "Scotland-Viking-o" would otherwise find nothing with no explanation
                f"No group {name!r}. Give the name without any outlier suffix "
                f"(use include_outliers=True for outliers), and check spelling "
                f"with list_values(anno, 'group_id')",
                UserWarning,
                stacklevel=2,
            )
        keep = base.isin(wanted)

    if not include_outliers: # Removes every outlier unless include_outliers=True
        keep &= ~is_outlier(anno["group_id"])
    return anno[keep]