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


# analysis
df = load_data(DATA_FILE)
rap = df[df["DRUG_NAME"] == "Rapamycin"]
print(len(rap))
print(rap["TCGA_DESC"].value_counts())