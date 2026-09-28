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

## Missing values
- AADR marks missing values as ".." 
- Columns with missing values (Latitude (17) and Longitude (18)) confirmed 784 - implement coordinate based region filter

## Dates below 0 BP or at 0 BP
- 1 date below 0 BP (-4) edge case but 3,970 dates at exactly 0 which likely marks present day individuals for comparison NOT CONFIRMED (possible that unconfirmed individuals have 0)

## Open questions
- Duplicates: one row per person or keep all?
- Citations: column 5 (first pub), 6 (this data's pub), or both?
- Date filer: mean only, or range using the uncertainty column (11)?
- Can the country column cover individuals missing coords?
- Do Genetic IDs match the first column of the .ind file exactly?
- Is the .geno file in TGENO format, and can convertf 9.0.0 read it?
- Is 0 present day or present day + unconfirmed? 