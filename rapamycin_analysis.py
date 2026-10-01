# Project code

import os
import sys

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

DATA_FILE = "GDSC2-dataset.csv"
BLOOD_TYPES = ["ALL", "LAML", "DLBC", "MM", "LCML", "CLL"]
EXCLUDED_TYPES = ["UNCLASSIFIED", "OTHER"]


# Reading the file
def load_data(path):  # Read the GDSC2 csv file
    if not os.path.exists(path):
        print(f"Cannot find '{path}'. Download it from Kaggle and put it in this folder.")  # stop if missing
        sys.exit(1)
    return pd.read_csv(path)


def get_groups(df, drug_name, blood_types=BLOOD_TYPES):  # Return the LN_IC50 values of blood and solid cell lines
    sub = df[df["DRUG_NAME"] == drug_name]  # picks one drug name
    sub = sub[~sub["TCGA_DESC"].isin(EXCLUDED_TYPES)]  # removes unclassified/other
    is_blood = sub["TCGA_DESC"].isin(blood_types)  # blood cancer rows
    return sub[is_blood]["LN_IC50"], sub[~is_blood]["LN_IC50"]  # blood cancers, solid tumours


# comparing the groups
def compare_groups(df, drug_name, blood_types=BLOOD_TYPES, min_lines=10):
    blood, solid = get_groups(df, drug_name, blood_types) # calling the previous function

    if len(blood) < min_lines or len(solid) < min_lines: # protections
        return None
    # Uncertainty of each mean
    sem_blood = blood.std() / np.sqrt(len(blood))
    sem_solid = solid.std() / np.sqrt(len(solid))
    #difference and its uncertainty
    diff = blood.mean() - solid.mean()
    diff_err = np.sqrt(sem_blood**2 + sem_solid**2)
    # t-test for significance
    _, p_value = stats.ttest_ind(blood, solid, equal_var=False)

    return {
        #dictionary
        "drug": drug_name,
        "n_blood": len(blood),
        "n_solid": len(solid),
        "mean_blood": blood.mean(),
        "sem_blood": sem_blood,
        "mean_solid": solid.mean(),
        "sem_solid": sem_solid,
        "diff": diff,
        "diff_err": diff_err,
        "sigma": abs(diff) / diff_err,
        "p_value": p_value,
    }

# analysis
df = load_data(DATA_FILE)
rap = df[df["DRUG_NAME"] == "Rapamycin"]
print(len(rap))
print(rap["TCGA_DESC"].value_counts())



# final analysis
def analyse_all_drugs(df, min_lines=20):
    rows = []
    for drug in df["DRUG_NAME"].unique():
        result = compare_groups(df, drug, min_lines=min_lines)
        if result is not None:
            rows.append(result)
    return pd.DataFrame(rows).sort_values("diff").reset_index(drop=True)


#Running the analysis
df = load_data(DATA_FILE)

rap = df[df["DRUG_NAME"] == "Rapamycin"]
print(len(rap))
print(rap["TCGA_DESC"].value_counts())

results = analyse_all_drugs(df)
print(len(results))
print(results[["drug", "n_blood", "n_solid", "diff", "diff_err"]].head(20))

# intermediate check
results.to_csv("all_drugs_blood_vs_solid.csv", index=False)