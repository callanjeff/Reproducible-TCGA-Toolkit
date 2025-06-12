#!/usr/bin/env python3

"""
Script: 03_coexpression_analysis.py

Description:
    Computes co-expression between a target gene and all other genes in a TCGA expression matrix,
    reporting both Pearson correlation coefficients and p-values. Useful for identifying immune 
    signaling relationships or microenvironmental associations.

Usage:
    python3 03_coexpression_analysis.py --gene PRRG2 --cohort LUAD

This script includes ✅ and ❌ print outputs to provide visual feedback on successful execution or errors.

Requirements:
    - pandas, scipy.stats
    - Python ≥ 3.8

Author:
    Jeffrey B. Callan
    MSc Bioinformatics Candidate, Brandeis University
    GitHub: https://github.com/jca11an
    Date: 2025-06-11
"""

import argparse
import pandas as pd
import os
from scipy.stats import pearsonr

def main():
    parser = argparse.ArgumentParser(description="Co-expression analysis using Pearson correlation.")
    parser.add_argument('--cohort', required=True, help="TCGA cohort (e.g., KIRC)")
    parser.add_argument('--gene', required=True, help="Gene symbol (e.g., PRRG2)")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    data_file = os.path.join(base_dir, "data", "processed", f"TCGA.{args.cohort}.sampleMap_HiSeqV2")
    results_dir = os.path.join(base_dir, "results", "tables")
    os.makedirs(results_dir, exist_ok=True)

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"❌ Expression file not found: {data_file}")

    # Load and clean data
    df = pd.read_csv(data_file, sep="\t", index_col=0)
    df = df.dropna(axis=1, how='any')  # Drop samples with missing expression

    if args.gene not in df.index:
        raise ValueError(f"❌ {args.gene} not found in expression matrix.")

    target_vector = df.loc[args.gene]

    # Compute Pearson correlation and p-values
    def compute_stats(row):
        r, p = pearsonr(row, target_vector)
        return pd.Series({'correlation': r, 'p_value': p})

    results = df.apply(compute_stats, axis=1)
    results = results.drop(index=args.gene)  # Exclude self-correlation

    # Sort by correlation
    results_sorted = results.sort_values(by="correlation", ascending=False)

    # Save results
    output_top50 = os.path.join(results_dir, f"{args.cohort}_{args.gene}_top50_coexpression.csv")
    output_full = os.path.join(results_dir, f"{args.cohort}_{args.gene}_coexpression_full.csv")

    results_sorted.head(50).to_csv(output_top50)
    results_sorted.to_csv(output_full)

    print(f"✅ Top 50 co-expressed genes (with p-values) saved to: {output_top50}")
    print(f"📄 Full correlation results saved to: {output_full}")

if __name__ == "__main__":
    main()
