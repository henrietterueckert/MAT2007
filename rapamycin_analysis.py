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

# so is rapamycin exceptional? 
target = compare_groups(df, "Rapamycin")

rank = results.index[results["drug"] == "Rapamycin"][0] + 1
median_diff = results["diff"].median()
q25, q75 = results["diff"].quantile([0.25, 0.75])
share_blood_more_sensitive = (results["diff"] < 0).mean()

print(f"Rapamycin: difference = {target['diff']:.2f} +/- {target['diff_err']:.2f} ({target['sigma']:.1f} sigma)")
print(f"All drugs: median difference = {median_diff:.2f}, middle 50% between {q25:.2f} and {q75:.2f}")
print(f"Blood more sensitive for {share_blood_more_sensitive:.1%} of drugs")
print(f"Rapamycin rank: {rank} of {len(results)}")

# plotting

def plot_all_drugs(results, drug_name, filename):
    target_diff = results.loc[results["drug"] == drug_name, "diff"].iloc[0]
    median_diff = results["diff"].median()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(results["diff"], bins=30, color="lightgray", edgecolor="black")
    ax.axvline(median_diff, color="blue", linestyle="--", label=f"Median of all drugs ({median_diff:.2f})")
    ax.axvline(target_diff, color="red", label=f"{drug_name} ({target_diff:.2f})")
    ax.set_xlabel("Mean LN_IC50 difference (blood - solid)")
    ax.set_ylabel("Number of drugs")
    ax.set_title("Blood-solid sensitivity difference across all drugs")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)