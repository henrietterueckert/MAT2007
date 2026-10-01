# Project code

import pandas as pd
import scipy
import matplotlib

# Reading the file, looking at classifications
df = pd.read_csv("GDSC2-dataset.csv")
rap = df[df["DRUG_NAME"] == "Rapamycin"]
print(len(rap))
print(rap["TCGA_DESC"].value_counts())

## There were 177 unclassified cancer types,  and 1 ther
# Remove cell lines without a usable cancer type label
rap = rap[~rap["TCGA_DESC"].isin(["UNCLASSIFIED", "OTHER"])]
# gives true for rows whose cancer type is in the list, and the ~ flips this

print(len(rap))
print(rap["TCGA_DESC"].value_counts())

# Separating into blood and solid cancers
blood_types = ["ALL", "LAML", "DLBC", "MM", "LCML", "CLL"]

rap = rap.copy()
rap["group"] = rap["TCGA_DESC"].isin(blood_types).map({True: "blood", False: "solid"})

print(rap["group"].value_counts())