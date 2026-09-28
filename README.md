# **Cancer type sensitivities to Rapamycin (mTOR inhibitor)**
## Research Question
Are blood cancers or solid tumours more sensitive to Rapamycin treatment (mTOR inhibitor)? Using drug sensitivity data from the GDSC2 (Genomics of Drug Sensitivity in Cancer) data set.

## Datasets
 **Original Source file:** 'GDSC2-DATASET.csv' 
Contains drug sensitivity data, including IC50 values, for various drugs tested against cancer cell lines. The dataset file is not in this repository due to large size (>25 mb) Download GDSC2-dataset.csv from Kaggle: https://www.kaggle.com/datasets/samiraalipour/genomics-of-drug-sensitivity-in-cancer-gdsc 

After downloading, place `GDSC2-DATASET.csv` in the same folder as the code

**Other Kaggle files:**
- `Compounds-annotation.csv`
- `GDSC_DATASET.csv`
- `Cell-lines.xlsx`

These are **not used** by this analysis, so you do not need them to reproduce the results

## Cleaning
**Does the dataset need cleaning?**

Not **manual** cleaning
The script performs all preprocessing automatically:
1. Keeps only rows where `DRUG_NAME == "Rapamycin"`.
2. Removes rows with `TCGA_DESC == "UNCLASSIFIED"` or a missing cancer type.
3. For the per-cancer-type summary and boxplot only, keeps cancer types with
   at least 5 cell lines. The blood vs solid tumour test uses all remaining
   Rapamycin measurements.

Cancer types are grouped as **blood cancer** (DLBC, MM, LCML, ALL, LAML) or
**solid tumour** (all other TCGA codes).


