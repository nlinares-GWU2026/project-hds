# AADR .anno File Notes

## 1. File details
- File: v66.p1_1240K.aadr.PUB.anno (Dataverse file ID 13994515)
- Downloaded: 09/25/2026
- Size: 23,089 rows × 49 columns (pandas count matches `wc -l` minus the header)
-  Checksums: see docs/data_checksums.txt; MD5 matched Dataverse

## 2. Columns used by each filter
How the columns map to filters
|Filter| Column | Notes |
 Filter: ID for covertf | Columns: 0 Genetic Identity | Should match the IDs in the `.ind` file, which is how the filter results connect to geno extraction
Filter: Region | Columns : 16 Political Entity, 15 Locality, 17 -18 Latitude/Longitutde | Country for simple filtering, coordinates allow for bound-box filter
Filter: Time Period | Columns: 10 Date mean in BP | "BP" means years before 1950 CE, so 5000 BP is about 3050 BCE 
Filter: Population | Columns: 14 Group ID | Likely same labels as .ind file's population column
Filter: Lineage | Columns: 35 Y haplogroup (ISOGG), 38 mtDNA haplogroup 
Filter: Coverage | Columns: 26 SNPs hit on 1240K snpset | Use 26, not 25 or 27-29 because those count SNPs on other panels, and this project uses 1240K panel
Filter: Quality | Columns: 47 ASSESSMENT
Filter : Publication | Columns: 5 First publication (abbrev. earliest paper that reported data on indiv.), 6 Publication abbrev, 7 doi for publication of this representation of the data | They can differ and a correct citation list may need both. Some rows may have ".." instead of a DOI in column 7

## Column name quirks
- Column 33 duplicate name, renamed with ".1" by pandas because file has two columns with exactly the same name
- Column 25 has trailing space at end of its name (code that types space won't find column)
- AADR column names are long and might have trailing space so aadrkit will adopt short names in place of typing out long real column names for ease
- Missing values are written as ".."
- One person can have several rows (Column 0 explains ".AG, .DG, .SG" and other data types for individuals), a filter could return the samer person twice so aadirkit will handle duplicates
- Exact text matching works if users know precise name. Pattern matching (using regex) lets users search for terms but patterns need precise boundaries so it does not accidentally catch unrelated names. Group ID links filter outputs to .ind files for convertf. 

## Missing values
- AADR marks missing values as ".." 
- Columns with missing values (Latitude (17) and Longitude (18)) confirmed 784 - implement coordinate based region filter

## Dates below 0 BP or at 0 BP
- Every row dated 0 BP says "present" so BP isn't being used as a placeholder for unknown dates, consistently means present day. 
- The -4 row reads 1954 CE 
- There are 4 rows labelled present that are ref rows including chimp, gorilla, and ancestor - we do not necessarily want to include this. Since pop geneticits use chimp or gorilla for comparing populations in kinds of analysis that ADMIXTOOLS runs, best option would to be exclude the references as default and have an option to include them 
- The "ancient" filter does not necessarily mean "ancient" - it means dated before present which includes historic individuals

## Messy data
- Column 21 data type contains mixed casing, mulitple values combined with commas, and free-text notes. Leave a data-type filter out of scope of my tool - it is messy and requires extra string splitting while Column 26 (Coverage/SNP hit) alraedy measures data quantity more directly. 

## Coverage
- User chooses the min SNP count with no hidden default

## Design decisions
- Loading: use na_values=[".."] so AADR's missing-value marker becomes a real missing value.
- Present-day: date_bp == 0 means present-day. All 3,970 such rows say "present" in v66.p1. Because this is an assumption about the data, it deserves its own test, so the package notices if a future AADR version breaks it.
- Reference genomes: four .REF rows aren't individuals. Exclude them from present-day and ancient selections by default, with an option to include them (for example, for a chimpanzee outgroup).
- Dates: negative values are valid (post-1950). The date filter uses the mean date and should say so in the documentation. The word "ancient" should be defined as "dated before present."
- Region: match country labels exactly but case-insensitively, and provide a helper that lists available labels. The coordinate filter reports how many individuals it excludes for missing coordinates (784).
- Population: offer exact match and anchored regular-expression matching on Group ID, plus a helper to list groups (3,897 of them).
- Coverage: the user chooses the minimum SNP count (column 26); no hidden default.
- Quality: look up what PROVISIONAL_ and MERGE_ mean before designing a quality filter.
- Data type: messy (case variants, comma-combined values, free-text notes) and out of scope as a filter.

## Open questions
- Duplicates: one row per person or keep all?
- Citations: column 5 (first pub), 6 (this data's pub), or both?
- Date filer: mean only, or range using the uncertainty column (11)?
- Can the country column cover individuals missing coords?
- Do Genetic IDs match the first column of the .ind file exactly?
- Is the .geno file in TGENO format, and can convertf 9.0.0 read it?