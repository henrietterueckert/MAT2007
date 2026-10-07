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
|`Cell-lines.xlsx`|This repository (not read by the script, but used to justify the blood vs solid grouping, see below)|


## Cleaning
**Does the dataset need cleaning?**

Not **manual** cleaning
The script performs all preprocessing automatically:
1. Selects the rows for one drug (`DRUG_NAME`), starting with Rapamycin.
2. Removes rows with `TCGA_DESC` equal to `UNCLASSIFIED` or `OTHER`, or with a missing cancer type.
3. Averages repeated measurements so each cell line (`COSMIC_ID`) counts once (see note below).
4. Compares mean LN_IC50 (blood - solid), with the standard error of the difference and a Welch t-test.
5. Repeats steps 1-4 for every drug with at least 20 cell lines in each group (286 drugs).

Cancer types are grouped as **blood cancer** (DLBC, MM, LCML, ALL, LAML, CLL) or
**solid tumour** (all other TCGA codes).

### What the TCGA codes are
`TCGA_DESC` is GDSC's "Cancer Type (matching TCGA label)". The Cancer Genome Atlas (TCGA) was a large NCI/NHGRI programme that profiled over 11,000 patient tumours across 33 cancer types and gave each type a short code (e.g. BRCA = breast invasive carcinoma, LAML = acute myeloid leukaemia). GDSC uses these codes to label each cell line with the patient cancer type it best matches (Iorio et al., 2016). Cell lines that do not match any TCGA type are labelled `UNCLASSIFIED`.

### How the blood vs solid grouping was decided
The grouping follows GDSC's own cell line annotation in `Cell-lines.xlsx` (GDSC's Cell_Lines_Details file):
- **Decode sheet:** the GDSC definitions of the TCGA labels. ALL (acute lymphoblastic leukaemia), CLL (chronic lymphocytic leukaemia), DLBC (diffuse large B-cell lymphoma), LAML (acute myeloid leukaemia), LCML (chronic myelogenous leukaemia) and MM (multiple myeloma) are the only haematological cancers; all other labels are solid tumours (carcinomas, gliomas, melanoma, neuroblastoma, etc.).
- **COSMIC tissue classification sheet:** every cell line with one of these six labels has the COSMIC site `haematopoietic_and_lymphoid_tissue`, and no cell line with any other label does.
- **GDSC Tissue descriptor 1:** these six labels fall only under `leukemia`, `lymphoma` or `myeloma`.

Lymphoma (DLBC) and myeloma (MM) are included as blood cancers because they are haematological malignancies (cancers of the blood-forming and lymphoid tissues), even though they are not leukaemias.

### Limitation: blood cancer lines without a TCGA label
`Cell-lines.xlsx` lists 53 haematopoietic/lymphoid cell lines with **no** TCGA label (e.g. Burkitt lymphoma, Hodgkin lymphoma, B-cell leukaemia, hairy cell leukaemia, anaplastic large cell lymphoma). About 50 of these have Rapamycin data in GDSC2 but are labelled `UNCLASSIFIED` and therefore excluded. The blood cancer group in this analysis therefore covers only TCGA-labelled blood cancer lines, not all blood cancer lines in GDSC2.

**Note on cell line counts:** some drugs were screened twice in GDSC2 under different `DRUG_ID`s, so the same cell line would otherwise appear twice and make the results look more significant than they are. Averaging per cell line prevents this. Cell lines with no cancer type are also dropped at this step, which is why the analysis uses 655 solid tumour lines for Rapamycin rather than the 661 counted before cleaning.

## How to run
Requires Python 3 with `pandas`, `numpy`, `scipy` and `matplotlib`:

```
pip install pandas numpy scipy matplotlib
```

With `GDSC2-dataset.csv` in the same folder, run:

```
python rapamycin_analysis.py
```

The script prints the Rapamycin result and the comparison with all drugs, and creates:
- `all_drugs_blood_vs_solid.csv`: results for every drug
- `figure1_boxplot.png`: Rapamycin LN_IC50 for blood cancers vs solid tumours
- `figure2_all_drugs.png`: blood - solid difference for all drugs, with Rapamycin marked

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

## References
- Iorio, F. et al. (2016). A Landscape of Pharmacogenomic Interactions in Cancer. *Cell*, 166(3), 740–754. https://doi.org/10.1016/j.cell.2016.06.017
- The Cancer Genome Atlas Research Network et al. (2013). The Cancer Genome Atlas Pan-Cancer analysis project. *Nature Genetics*, 45, 1113–1120. https://doi.org/10.1038/ng.2764
- Genomics of Drug Sensitivity in Cancer (GDSC): TCGA label definitions, https://www.cancerrxgene.org/faq