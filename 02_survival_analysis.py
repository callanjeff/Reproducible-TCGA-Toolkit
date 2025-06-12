"""
Script: 02_survival_analysis.py

Description:
    Performs Kaplan–Meier survival analysis for TCGA cohorts by stratifying samples 
    based on gene expression. Survival metrics such as overall survival time and status 
    are merged with expression data, and groups are split for comparative analysis.

Usage:
    python3 02_survival_analysis.py [OPTIONS]
    python3 02_survival_analysis.py --gene PRRG2 --cohort LUAD

This script includes ✅ and ❌ print outputs to provide visual feedback on successful execution or errors.

Requirements:
    - pandas, numpy, lifelines, matplotlib
    - Python ≥ 3.8

Author:
    Jeffrey B. Callan
    MSc Bioinformatics Candidate, Brandeis University
    GitHub: https://github.com/jca11an
    Date: 2025-06-11
"""
#!/usr/bin/env python3


import argparse
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
import os

def main():
    parser = argparse.ArgumentParser(description="Kaplan-Meier survival analysis for TCGA gene expression.")
    parser.add_argument('--cohort', required=True, help="TCGA cohort name (e.g., KIRC)")
    parser.add_argument('--gene', required=True, help="Gene of interest (e.g., PRRG2)")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    data_dir = os.path.join(base_dir, "data")
    processed_dir = os.path.join(data_dir, "processed")
    metadata_dir = os.path.join(data_dir, "metadata")
    results_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(results_dir, exist_ok=True)

    expression_file = os.path.join(processed_dir, f"TCGA.{args.cohort}.sampleMap_HiSeqV2")
    survival_file = os.path.join(metadata_dir, "survival_tcga_cdr.tsv")

    if not os.path.exists(expression_file):
        raise FileNotFoundError(f"Expression file not found: {expression_file}")
    if not os.path.exists(survival_file):
        raise FileNotFoundError(f"Survival file not found: {survival_file}")

    # Load data
    exp = pd.read_csv(expression_file, sep="\t", index_col=0).T
    surv = pd.read_csv(survival_file, sep="\t")

    # Format survival data
    surv = surv.rename(columns={"sample": "Sample", "OS": "OS_event", "OS.time": "OS_time"})
    surv = surv[["Sample", "OS_time", "OS_event"]].dropna()
    surv["Sample"] = surv["Sample"].str.replace(r"-01$", "", regex=True)

    # Match and merge
    exp.index = exp.index.str.replace(r"-01A.*$", "", regex=True)
    merged = exp[[args.gene]].join(surv.set_index("Sample"))
    merged.dropna(inplace=True)

    # Create expression group
    merged["group"] = merged[args.gene] > merged[args.gene].median()

    # Kaplan-Meier plot
    kmf = KaplanMeierFitter()
    for group, label in zip([True, False], ["High", "Low"]):
        kmf.fit(
            durations=merged[merged.group == group]["OS_time"],
            event_observed=merged[merged.group == group]["OS_event"],
            label=f"{label} {args.gene}"
        )
        kmf.plot_survival_function()

    # Log-rank test
    results = logrank_test(
        merged[merged.group == True]["OS_time"],
        merged[merged.group == False]["OS_time"],
        event_observed_A=merged[merged.group == True]["OS_event"],
        event_observed_B=merged[merged.group == False]["OS_event"]
    )

    p_value = results.p_value
    print(f"🧪 Log-rank test p-value: {p_value:.4g}")

    # Save plot
    plt.title(f"Survival Curve: {args.gene} in {args.cohort}")
    plt.xlabel("Days")
    plt.ylabel("Survival Probability")
    output_path = os.path.join(results_dir, f"{args.cohort}_{args.gene}_survival.png")
    plt.savefig(output_path)
    plt.close()

    print(f"✅ Survival plot saved to: {output_path}")

if __name__ == "__main__":
    main()
