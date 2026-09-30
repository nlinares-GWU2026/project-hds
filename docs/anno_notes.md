# AADR .anno File Notes
## Exploring data before writing tool code (1-9):
Step 1: Explored the metadata. Loaded all 23089 rows and 49 columns and matched columns to planned filters. 
Step 2: Profiled the columns. Checked what was inside the date, location, coverage, country, population, data type, and quality (filters I will use). Identified hidden problems like ".." for misisng values, a chimpanzee and gorilla REF was labeled as present, messy capitalization, and 784 people had no long. and lat. coordinates. 
Step 3: Choosing hand verified "test"/"ground truth" individuals to test my tool against (8-10 individuals I will check myself). From the profiling, the tricky cases and individuals I would want to choose are: 1. present-day (0 BP), 2. reference genome (like `Chimp.REF`), 3. the one post-1950 individual (-4 BP), 4. someone with missing coordinates, 5. someone with low coverage, 6. someone from a place AADR lists separately (Canary Islands), 7. Someone whose group matches a pattern like "Viking, 8. a person with several rows. First check duplicates and publications to see how often one person appears in several rows before choosing test. Next, choose individuals. Finally, verify each one by hand with `grep` and record expected  values.  

## Output `profile_anno.py`:
=== Column 10: Date mean in BP in years before 1950 CE [OxCal mu for a dire ===
pandas dtype: int64
values that are not numbers: 0
Series([], Name: count, dtype: int64)
count     23089.000000
mean       2859.387587
std        3849.763639
min          -4.000000
25%         800.000000
50%        1938.000000
75%        4300.000000
max      185000.000000
Name: Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date], dtype: float64

=== Column 17: Latitude ===
pandas dtype: str
values that are not numbers: 784
Latitude
..    784
Name: count, dtype: int64
count    22305.000000
mean        40.044975
std         17.875584
min        -55.250000
25%         36.638333
50%         46.283333
75%         50.815000
max         75.240000
Name: Latitude, dtype: float64

=== Column 18: Longitude ===
pandas dtype: str
values that are not numbers: 784
Longitude
..    784
Name: count, dtype: int64
count    22305.000000
mean        24.251194
std         49.426079
min       -175.115520
25%          5.096183
50%         17.384680
75%         41.583968
max        174.450000
Name: Longitude, dtype: float64

=== Column 26: SNPs hit on autosomal targets (Computed using easystats on 1 ===
pandas dtype: int64
values that are not numbers: 0
Series([], Name: count, dtype: int64)
count    2.308900e+04
mean     6.155170e+05
std      3.882377e+05
min      2.810000e+02
25%      2.257580e+05
50%      6.836130e+05
75%      9.852110e+05
max      1.150639e+06
Name: SNPs hit on autosomal targets (Computed using easystats on 1240k snpset), dtype: float64

Rows missing both lat and long: 784
Dates below 0 BP: 1
Dates exactly 0 BP: 3970

=== Column 16: Political Entity ===
unique values: 145
".." entries: 10
empty cells: 0
Political Entity
Russia            1890
United Kingdom    1496
China             1479
Hungary           1475
Italy              944
Austria            878
Spain              802
Germany            770
Denmark            654
France             644
Name: count, dtype: int64

=== Column 14: Group ID ===
unique values: 3897
".." entries: 0
empty cells: 0
Group ID
Austria_Avar                       714
Belgium_HighMedieval               183
England_Cambridgeshire_Medieval    148
Sweden_Viking                      145
Poland_IA                          130
Czechia_EBA_Unetice                113
Spain_C                            112
TSI                                108
GWD                                106
France_Yonne_N                     105
Name: count, dtype: int64

=== Column 21: Data type ===
unique values: 28
".." entries: 0
empty cells: 0
Data type
1240k                                                                                    11079
Shotgun                                                                                   6630
Shotgun.diploid                                                                           3800
Twist1.4M                                                                                  537
1240k,Twist1.4M                                                                            490
1240k,Shotgun                                                                              203
Shotgun pulled down only on 1240k autosomal targets - need to make a whole genome bam       86
Immune Capture                                                                              44
1240K                                                                                       43
Shotgun,WholeGenomeCapture                                                                  36
Name: count, dtype: int64

=== Column 47: ASSESSMENT ===
unique values: 9
".." entries: 0
empty cells: 0
ASSESSMENT
Pass                        18549
PROVISIONAL_PASS             2908
Questionable                  962
CRITICAL                      373
MERGE_PASS                    183
PROVISIONAL_CRITICAL           83
PROVISIONAL_QUESTIONABLE       22
MERGE_QUESTIONABLE              7
MERGE_CRITICAL                  2
Name: count, dtype: int64

=== All countries (column 16), sorted ===
['..', 'Abkhazia', 'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belgium', 'Belize', 'Bolivia', 'Bosnia-Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Cambodia', 'Cameroon', 'Canada', 'Canary Islands', 'Central African Republic', 'Channel Islands', 'Chile', 'China', 'Colombia', 'Congo', 'Crimea', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Democratic Republic of the Congo', 'Denmark', 'Dominican Republic', 'Egypt', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Federated States of Micronesia', 'Finland', 'France', 'French Polynesia', 'Gambia', 'Georgia', 'Germany', 'Gibraltar', 'Greece', 'Greenland', 'Guadeloupe', 'Guam', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Lithuania', 'Luxembourg', 'Malawi', 'Malaysia', 'Malta', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nigeria', 'North Macedonia', 'Norway', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Republic of Korea', 'Romania', 'Russia', 'Saint Helena', 'Saint Lucia', 'Senegal', 'Serbia', 'Sierra Leone', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Tonga', 'Tunisia', 'Turkey', 'Turkmenistan', 'USA', 'Uganda', 'Ukraine', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia']

=== Data type for rows at or below 0 BP ===
Data type
Shotgun.diploid     3726
Shotgun              240
Reference Genome       4
1240k                  1
Name: count, dtype: int64

=== Full Date text for rows at or below 0 BP ===
Full Date One of two formats. (Format 1) 95.4% CI calibrated radiocarbon age (Conventional Radiocarbon Age BP, Lab number) e.g. 2624-2350 calBCE (3990+-40 BP, Ua-35016). (Format 2) Archaeological context range, e.g. 2500-1700 BCE
present    3970
1954 CE       1
Name: count, dtype: int64

=== Unusual rows at or below 0 BP ===
         genetic_id  date_bp full_date                    group_id         data_type
11582  Ancestor.REF        0   present                    Ancestor  Reference Genome
11620     Chimp.REF        0   present                       Chimp  Reference Genome
11688   Gorilla.REF        0   present                     Gorilla  Reference Genome
11712      Href.REF        0   present                     hg19ref  Reference Genome
16586      JHF05.AG        0   present              Malaysia_Jehai             1240k
19755      Khwit.SG       -4   1954 CE  Georgia_Tkhina_20thCentury           Shotgun


## Notes: 
### 1. File details
- File: v66.p1_1240K.aadr.PUB.anno (Dataverse file ID 13994515)
- Downloaded: 09/25/2026
- Size: 23,089 rows × 49 columns (pandas count matches `wc -l` minus the header)
-  Checksums: see docs/data_checksums.txt; MD5 matched Dataverse

### 2. Columns used by each filter
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

### 3. Column name quirks
- Column 33 duplicate name, renamed with ".1" by pandas because file has two columns with exactly the same name
- Column 25 has trailing space at end of its name (code that types space won't find column)
- AADR column names are long and might have trailing space so aadrkit will adopt short names in place of typing out long real column names for ease
- Missing values are written as ".."
- One person can have several rows (Column 0 explains ".AG, .DG, .SG" and other data types for individuals), a filter could return the samer person twice so aadirkit will handle duplicates
- Exact text matching works if users know precise name. Pattern matching (using regex) lets users search for terms but patterns need precise boundaries so it does not accidentally catch unrelated names. Group ID links filter outputs to .ind files for convertf. 

### 4. Missing values
- AADR marks missing values as ".." 
- Columns with missing values (Latitude (17) and Longitude (18)) confirmed 784 - implement coordinate based region filter

### 5. Dates below 0 BP or at 0 BP
- Every row dated 0 BP says "present" so BP isn't being used as a placeholder for unknown dates, consistently means present day. 
- The -4 row reads 1954 CE 
- There are 4 rows labelled present that are ref rows including chimp, gorilla, and ancestor - we do not necessarily want to include this. Since pop geneticits use chimp or gorilla for comparing populations in kinds of analysis that ADMIXTOOLS runs, best option would to be exclude the references as default and have an option to include them 
- The "ancient" filter does not necessarily mean "ancient" - it means dated before present which includes historic individuals

### 6. Messy data
- Column 21 data type contains mixed casing, mulitple values combined with commas, and free-text notes. Leave a data-type filter out of scope of my tool - it is messy and requires extra string splitting while Column 26 (Coverage/SNP hit) alraedy measures data quantity more directly. 

### 7. Coverage
- User chooses the min SNP count with no hidden default

### 8. Design decisions
- Loading: use na_values=[".."] so AADR's missing-value marker becomes a real missing value.
- Present-day: date_bp == 0 means present-day. All 3,970 such rows say "present" in v66.p1. Because this is an assumption about the data, it deserves its own test, so the package notices if a future AADR version breaks it.
- Reference genomes: four .REF rows aren't individuals. Exclude them from present-day and ancient selections by default, with an option to include them (for example, for a chimpanzee outgroup).
- Dates: negative values are valid (post-1950). The date filter uses the mean date and should say so in the documentation. The word "ancient" should be defined as "dated before present."
- Region: match country labels exactly but case-insensitively, and provide a helper that lists available labels. The coordinate filter reports how many individuals it excludes for missing coordinates (784).
- Population: offer exact match and anchored regular-expression matching on Group ID, plus a helper to list groups (3,897 of them).
- Coverage: the user chooses the minimum SNP count (column 26); no hidden default.
- Quality: look up what PROVISIONAL_ and MERGE_ mean before designing a quality filter.
- Data type: messy (case variants, comma-combined values, free-text notes) and out of scope as a filter.

### 9. Open questions
- Duplicates: one row per person or keep all?
- Citations: column 5 (first pub), 6 (this data's pub), or both?
- Date filer: mean only, or range using the uncertainty column (11)?
- Can the country column cover individuals missing coords?
- Do Genetic IDs match the first column of the .ind file exactly?
- Is the .geno file in TGENO format, and can convertf 9.0.0 read it?


## 