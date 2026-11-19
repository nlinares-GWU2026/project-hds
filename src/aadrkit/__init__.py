"""aadrkit: filter and export subsets of the Allen Ancient DNA Resource (AADR)."""

# Users can write aadrkir.load_anno(...) instead of having to konw the function lives in the anno module
from aadrkit.anno import list_values, load_anno
from aadrkit.convertf import extract_genotypes
from aadrkit.query import select

__version__ = "0.1.0"