WHAT GOES IN THIS FOLDER
========================
Updated 16 Sept 2026, 7:35pm ET.

THIS FOLDER holds the EXTRACTION results: the CSVs Gemini Notebook gives back
when it reads the episodes and pulls out who each analyst recommended.

2021: USE  2021_MERGED_USE_THIS.csv
----------------------------------
418 rows, 19 episodes, 4 shows. That is the merge of all nine files you saved.
DO NOT use any single fantasy_takes_2021*.csv file. Here is why:

   fantasy_takes_2021.csv       72 rows    all 72 unique
   fantasy_takes_2021_v2.csv   127 rows    all 127 unique
   fantasy_takes_2021_v3.csv   118 rows    all 118 unique
   fantasy_takes_2021_v4.csv   135 rows     17 new
   v5, v6, v7, v8              135 rows      0 new  (byte-identical to v4)
   fantasy_takes_2021_v9.csv   219 rows     84 new

The biggest file is not the complete one. v9 does not contain a single row from
the first two files. Keeping only v9 would have thrown away 199 of 418 rows.
The notebook said it was tracking what it had done. It was not.

Those nine files are kept as raw evidence. Work from the merged one.
2021 is about 29% covered: 19 episodes of the 65 links on the list.

2022 - 2025: NOT STARTED
------------------------
Save each batch as its own file:   2022_batch1.csv, 2022_batch2.csv, ...
One file per batch, never one growing file. If a batch comes back wrong you
throw away one file instead of untangling a merged one.

THE OTHER FOLDERS ARE INPUTS, AND THEY ARE FINISHED
---------------------------------------------------
..\..\The Takes Corpus\        the raw link hunting. Nine markdown files, one
                               per show. Finished 15 Sept.

..\..\Source\takes_links\      the links, cleaned. Two files per year:
                                 2022.txt        annotated, grouped by show
                                 2022_PASTE.txt  flat URLs, nothing else
                               PASTE the second one into Notebook. One box,
                               one paste, no per-show copying.
                               takes_coverage.csv counts what each show has.

..\..\Fantasy Analysts Takes.txt   an early 29-row link list from 14 Sept.
                               SUPERSEDED. Ignore it.

THE ORDER OF WORK
-----------------
1. Hunt the links.          DONE for nine shows. One more show to add.
2. Clean them per season.   DONE
3. Extract the calls.       THIS FOLDER. 2021 part done, 2022-2025 not started.
4. Score them against what actually happened.

THE STEPS, THE PROMPTS AND THE COPY BUTTONS ARE ON THE PAGE
-----------------------------------------------------------
Open  Source\TAKES_CORPUS.html  in Chrome. It shows only what is left, and
every block on it has a copy button, including the URLs for each year.
