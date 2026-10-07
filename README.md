# **Cancer type sensitivities to Rapamycin (mTOR inhibitor)**
## Research Question
Are blood cancers or solid tumours more sensitive to Rapamycin treatment (mTOR inhibitor)? Using drug sensitivity data from the GDSC2 (Genomics of Drug Sensitivity in Cancer) data set.

## Datasets
 **Original Source file:** `GDSC2-dataset.csv`
 
Contains drug sensitivity data, including IC50 values, for various drugs tested against cancer cell lines. The dataset file is not in this repository due to large size (>25 mb) Download GDSC2-dataset.csv from Kaggle: https://www.kaggle.com/datasets/samiraalipour/genomics-of-drug-sensitivity-in-cancer-gdsc 

After downloading, place `GDSC2-dataset.csv` in the same folder as the code

**Other Kaggle files:**

The follwing files are **not used** by this analysis, so you do not need them to reproduce the results. 

|Files        |Where to find |
|--------------|--------------|
|`Compounds-annotation.csv`|This repository|
|`GDSC_DATASET.csv`|Kaggle: https://www.kaggle.com/datasets/samiraalipour/genomics-of-drug-sensitivity-in-cancer-gdsc |
|`Cell-lines.xlsx`|This repository|


## Cleaning
**Does the dataset need cleaning?**

Not **manual** cleaning
The script performs all preprocessing automatically:
1. Keeps only rows where `DRUG_NAME == "Rapamycin"`.
2. Removes rows with `TCGA_DESC == "UNCLASSIFIED"` or a missing cancer type.
4. Compare mean LN_IC50 (blood - solid) with uncertainty 
5. Repeat for all drugs with at least 20 cell lines per group (286 drugs)

Cancer types are grouped as **blood cancer** (DLBC, MM, LCML, ALL, LAML) or
**solid tumour** (all other TCGA codes).

## Rapamycin cell lines by cancer type
|  TCGA_DESC    | Cell lines | Group in analysis |
|--------------|-----------:|-------------------|
| UNCLASSIFIED | 177        | excluded          |
| LUAD         | 62         | solid             |
| SCLC         | 57         | solid             |
| SKCM         | 54         | solid             |
| BRCA         | 50         | solid             |
| COREAD       | 43         | solid             |
| HNSC         | 39         | solid             |
| GBM          | 34         | solid             |
| ESCA         | 34         | solid             |
| OV           | 34         | solid             |
| KIRC         | 32         | solid             |
| DLBC         | 31         | blood             |
| NB           | 30         | solid             |
| PAAD         | 29         | solid             |
| ALL          | 26         | blood             |
| LAML         | 25         | blood             |
| STAD         | 23         | solid             |
| MESO         | 21         | solid             |
| BLCA         | 18         | solid             |
| MM           | 17         | blood             |
| LGG          | 17         | solid             |
| THCA         | 15         | solid             |
| LIHC         | 15         | solid             |
| CESC         | 14         | solid             |
| LUSC         | 14         | solid             |
| LCML         | 10         | blood             |
| UCEC         | 9          | solid             |
| PRAD         | 6          | solid             |
| MB           | 4          | solid             |
| CLL          | 2          | blood             |
| ACC          | 1          | solid             |
| OTHER        | 1          | excluded          |


