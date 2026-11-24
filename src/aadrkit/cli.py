"""Command-line interface: run aadrkit from the terminal.

Examples, run from the repository root:
    aadrkit list country
    aadrkit select --group Scotland_Viking --out data/output/vikings
    aadrkit select --min-bp 3000 --max-bp 5000 --country Spain --min-snps 100000 \\
        --out data/output/spain --genotypes --format plink"""

import argparse
import shlex
import sys
from pathlib import Path

from aadrkit import __version__
from aadrkit.anno import list_values, load_anno
from aadrkit.convertf import extract_genotypes
from aadrkit.query import select

DEFAULT_ANNO = "data/raw/v66.p1_1240K.aadr.PUB.anno"
DEFAULT_GENO_PREFIX = "data/raw/v66.p1_1240K.aadr.patch.PUB"
FORMATS = {"eigenstrat": "EIGENSTRAT", "plink": "PACKEDPED"}

def build_parser():
    """Describe every command-line option."""
    parser = argparse.ArgumentParser(
        prog="aadrkit",
        description="Filter and export subsets of Allen Ancient DNA Resource (AADR).",
    )
    parser.add_argument("--anno", default=DEFAULT_ANNO,
                        help=f"AADR .anno file (default: {DEFAULT_ANNO})")

    sub = parser.add_subparsers(dest="command", required=True)

    lst = sub.add_parser("list", help="Show every value in a column, with counts")
    lst.add_argument("column", help="Column name, e.g. country, group_id, assessment")

    sel = sub.add_parser("select", help="Select individuals; optionally save and extract genotypes")
    sel.add_argument("--min-bp", type=int, help="Minimum mean date, in years before 1950 CE")
    sel.add_argument("--max-bp", type=int, help="Maximum mean date, in years before 1950 CE")
    sel.add_argument("--exclude-present", action="store_true", help="Remove present-day individuals (dated 0 BP)")
    sel.add_argument("--country", action="append", help="Country label (repeat for several); see 'aadrkit list country'")
    sel.add_argument("--min-lat", type=float, help="Southern edge of a latitude/longitude box")
    sel.add_argument("--max-lat", type=float, help="Northern edge of a latitude/longitude box")
    sel.add_argument("--min-lon", type=float, help="Western edge of a latitude/longitude box")
    sel.add_argument("--max-lon", type=float, help="eastern edge of a latitude/longitude box (smaller than --min-lon means the box crosses 180 degrees)")
    sel.add_argument("--group", action="append", help="Population base name (repeat for several); see 'aadrkit list group_id'")
    sel.add_argument("--group-regex", action="store_true", help="Treaet --group values as regular expressions")
    sel.add_argument("--include-outliers", action="store_true", help="Keep population-genetic outliers ('-o' groups)")
    sel.add_argument("--min-snps", type=int, help="Minimum SNPs covered on the 1240K panel")
    sel.add_argument("--include-references", action="store_true", help="Keep reference genomes (Chimp, Gorilla, ...)")
    sel.add_argument("--keep-duplicates", action="store_true", help="Keep every dataset per person instead of the best one")
    sel.add_argument("--out", help="Output prefix; writes <out>_selected.tsv, <out>_report.tsv, and <out>_command.txt")
    sel.add_argument("--genotypes", action="store_true", help="Also extract genotypes with convertf (requires --out)")
    sel.add_argument("--geno-prefix", default=DEFAULT_GENO_PREFIX, help=f"Prefix of the AADR .geno/.snp/.ind files (default: {DEFAULT_GENO_PREFIX})")
    sel.add_argument("--format", choices=sorted(FORMATS), default="eigenstrat", help="Genotype output format (default: EIGENSTRAT)")
    sel.add_argument("--quiet", action="store_true", help="Do not print the report")
    return parser

def run_list(args, anno): # Checks column name and then prints list_values
    """`aadrkit list COLUMN`: print each value in a column with its count."""
    if args.column not in anno.columns:
        raise SystemExit(f"Unknown column {args.column!r}; choose from: {', '.join(anno.columns)}") # Standard way for command-line proram to stop with an error
    print(list_values(anno, args.column).to_string())

def run_select(args, anno, command_line=""):
    """`aadrkit select ...`: run select() and save outputs if --out is given."""
    if args.genotypes and not args.out:
        raise SystemExit("--genotypes requires --out")

    selected, report = select(
        anno,
        min_bp=args.min_bp, max_bp=args.max_bp, exclude_present=args.exclude_present,
        countries=args.country, 
        min_lat=args.min_lat, max_lat=args.max_lat, min_lon=args.min_lon, max_lon=args.max_lon,
        groups=args.group, group_regex=args.group_regex, include_outliers=args.include_outliers,
        min_snps=args.min_snps, include_references=args.include_references,
        deduplicate=not args.keep_duplicates, verbose=not args.quiet,
    )

    if not args.out:
        return {}

    prefix = Path(args.out)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    outputs = {
        "selected": f"{prefix}_selected.tsv",
        "report": f"{prefix}_report.tsv",
        "command": f"{prefix}_command.txt",
    }
    selected.to_csv(outputs["selected"], sep="\t", index=False)
    report.to_csv(outputs["report"], sep="\t", index=False)
    Path(outputs["command"]).write_text(f"# aadrkit {__version__}\n{command_line}\n")

    if args.genotypes:
        g = args.geno_prefix
        outputs.update(extract_genotypes(selected, f"{g}.geno", f"{g}.snp", f"{g}.ind", prefix, output_format=FORMATS[args.format]))

    if not args.quiet:
        for name, path in outputs.items():
            print(f"{name}: {path}")
    return outputs

def main(argv=None): # When run from the terminal, it reads the real command line
    """Entry point for the `aadrkit` command."""
    if argv is None:
        argv = sys.argv[1:] # Everything after the program name
    args = build_parser().parse_args(argv)
    if not Path(args.anno).exists(): # Checks that the .anno file exists
        raise SystemExit(f"AADR .anno file not found: {args.anno} (see README 'Data' section)")
    anno = load_anno(args.anno)
    if args.command == "list":
        run_list(args, anno)
    else:
        run_select(args, anno, command_line=shlex.join(["aadrkit", *argv])) # Rebuilds the exact command as one line of text, adding quotes wherever needed

if __name__ == "__main__": # Lets the file be run as python -m aadrkit.cli. __name__ equals "__main__" only when the file is run directly, not imported.
    main()