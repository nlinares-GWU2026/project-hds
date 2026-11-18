"""Run a full AADR selection: filters in a fixed order, sensible defaults, and a report."""
import pandas as pd

from aadrkit.filters import (
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

REPORT_COLUMNS = ["Step", "Rows_before", "Rows_after", "Removed", "Note"]

def _record(report, step, before, after, note=""): # "_record" is internal helper function, do not need to call it directly
    """Add one row to the selection report."""
    report.append({
        "Step" : step,
        "Rows_before" : len(before),
        "Rows_after" : len(after),
        "Removed" : len(before) - len(after),
        "Note" : note,
    })

def select(anno, *, min_bp=None, max_bp=None, exclude_present=False,
           countries=None, min_lat=None, max_lat=None, min_lon=None, max_lon=None,
           groups=None, group_regex=False, include_outliers=False,
           min_snps=None, include_references=False, deduplicate=True,
           verbose=True):
    """Select individuals from a load_anno() table.
    
    Steps run in a fixed order, so the same arguments always give the same result and report:
    1. reference genomes removed (unless include_references=True)
    2. present-day individuals removed (if exclude_present=True)
    3. date range (min_bp, max_bp)
    4. country (countries)
    5. coordinates (min_lat, max_lat, min_lon, max_lon)
    6. population (groups, group_regex, include_outliers)
    7. coverage (min_snps)
    8. one row per person (unless deduplicate=False); ALWAYS LAST
    
    Steps whose arguments are not given are skipped. Outliers only matter in the population step,
    where they are excluded unless include_outliers=True. All arguments after `anno` must be named.
    
    Returns (selected, report): the selected rows, and a table of how many rows each step removed. 
    The report is also printed if verbose=True."""
    report = []
    current = anno

    if not include_references:
        before, current = current, exclude_reference_genomes(current)
        _record(report, "Exclude Reference Genomes", before, current)

    if exclude_present:
        before, current = current, exclude_present_day(current)
        _record(report, "Exclude Present-day", before, current)

    if min_bp is not None or max_bp is not None:
        before, current = current, filter_date_range(current, min_bp, max_bp)
        _record(report, f"Date range (min_bp = {min_bp}, max_bp = {max_bp})", before, current)

    if countries is not None:
        before, current = current, filter_country(current, countries)
        _record(report, f"Country {countries}", before, current)

    bounds = dict(min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)
    if any(value is not None for value in bounds.values()):
        no_coords = int((current["lat"].isna() | current["lon"].isna()).sum())
        before, current = current, filter_bounding_box(current, **bounds)
        _record(report, "coordinates", before, current,f"{no_coords} had no coordinates")

    if groups is not None:
        before = current
        matched = filter_group(current, groups, include_outliers=True, regex=group_regex)
        outliers = is_outlier(matched["group_id"])
        if include_outliers:
            current, note = matched, "Outliers included"
        else:
            current, note = matched[~outliers], f"{int(outliers.sum())} outliers excluded"
        _record(report, f"Group {groups}", before, current, note)

    if min_snps is not None:
        before, current = current, filter_min_snps(current, min_snps)
        _record(report, f"At least {min_snps} SNPs", before, current)

    if deduplicate:
        before, current = current, deduplicate_individuals(current)
        _record(report, "One row per person", before, current)

    report = pd.DataFrame(report, columns=REPORT_COLUMNS)
    if verbose:
        print(report.to_string(index=False))
        print(f"Selected {len(current)} rows.")
    return current, report