import pandas as pd
import pytest

from aadrkit.cli import build_parser, run_list, run_select


def parse(*argv):
    """Parse a command line the way the terminal would."""
    return build_parser().parse_args(list(argv))


# Parsing: no data needed

def test_parser_maps_options():
    args = parse("select", "--min-bp", "1000", "--country", "Spain", "--country", "Portugal",
                 "--group", "Poland_IA", "--min-lon", "-170", "--format", "plink")
    assert args.min_bp == 1000
    assert args.country == ["Spain", "Portugal"]
    assert args.group == ["Poland_IA"]
    assert args.min_lon == -170.0
    assert args.format == "plink"


def test_parser_rejects_unknown_format():
    with pytest.raises(SystemExit):
        parse("select", "--format", "vcf")


# Running commands on the real data

def test_genotypes_require_out(anno):
    with pytest.raises(SystemExit):
        run_select(parse("select", "--genotypes", "--quiet"), anno)


def test_select_writes_outputs(anno, tmp_path):
    args = parse("select", "--group", "Scotland_Viking", "--out", str(tmp_path / "vik"), "--quiet")
    outputs = run_select(args, anno, command_line="aadrkit select --group Scotland_Viking")

    selected = pd.read_csv(outputs["selected"], sep="\t")
    ids = set(selected["genetic_id"])
    assert len(selected) == 6
    assert "VK202.AG" in ids and "VK201.AG" not in ids

    report = pd.read_csv(outputs["report"], sep="\t")
    assert len(report) == 3          # reference genomes, group, one row per person

    assert "Scotland_Viking" in open(outputs["command"]).read()


def test_list_prints_values(anno, capsys):
    run_list(parse("list", "country"), anno)
    printed = capsys.readouterr().out
    assert "Spain" in printed and "802" in printed


def test_list_rejects_unknown_column(anno):
    with pytest.raises(SystemExit):
        run_list(parse("list", "planet"), anno)