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