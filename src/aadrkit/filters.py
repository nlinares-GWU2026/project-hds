"""Filter functions for AADR annotation tables returned by load_anno().
Each function takes a DataFrame and returns a new, filtered DataFrame,
so filters can be combined in any order."""
import pandas as pd

def filter_date_range(anno, min_bp=None, max_bp=None):
    """Keep individuals whose mean date (years BP) is within [min_bp, max_bp].
    BP means "before present", where present = 1950 CE, so larger numbers
    are older. Both bounds are inclusive, and either can be None for no limit.
    Individuals with a missing date are excluded whenever aa bound is given."""
    if min_bp is not None and max_bp is not None and min_bp > max_bp:
        raise ValueError(f"The minimum years BP ({min_bp}) is greater than the maximum years BP ({max_bp})")
    keep = pd.Series(True, index=anno.index) # Keep everything so far
    if min_bp is not None:
        keep &= anno["date_bp"] >= min_bp # Keep true only if already true, narrowing further
    if max_bp is not None: 
        keep &= anno["date_bp"] <= max_bp
    return anno[keep] 

def exclude_present_day(anno):
    """Remove present day individuals (date_bp == 0, labeled "present" in AADR).
    Individuals dated after 1950 CE (negative BP, such as 1954 CE) are kept, because 
    they have a real historical date rather than "present". """
    return anno[anno["date_bp"] != 0]

def exclude_reference_genomes(anno):
    """Remove reference genomes (Genetic IDs ending in ".REF:), which are not individuals."""
    return anno[~anno["genetic_id"].str.endswith(".REF")]