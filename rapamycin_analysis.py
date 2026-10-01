# Project code

import pandas as pd
import scipy
import matplotlib

# Reading the file
df = pd.read_csv("GDSC2-dataset.csv")
rap = df[df["DRUG_NAME"] == "Rapamycin"]
print(len(rap))
print(rap["TCGA_DESC"].value_counts())

