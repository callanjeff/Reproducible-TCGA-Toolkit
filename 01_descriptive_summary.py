"""
Script: 01_descriptive_summary.py

Description:
    Generates a descriptive summary of a TCGA expression dataset for a specified cohort.
    The script loads a processed RNA-seq gene expression matrix, computes basic statistics 
    for each gene (e.g., mean, standard deviation, min, max), and saves the summary table 
    to the results directory for downstream review or filtering.

Usage:
    python3 01_descriptive_summary.py <TCGA_COHORT>
    Example: python3 01_descriptive_summary.py LUAD

Inputs:
    - <TCGA_COHORT>: TCGA cancer type abbreviation (e.g., LUAD, KIRC)
    - Expression file located at: data/processed/TCGA.<COHORT>.sampleMap_HiSeqV2 
    (or fallback to .tsv extension)

Outputs:
    - A tab-separated file containing descriptive statistics for each gene
    saved to: results/tables/<COHORT>_expression_summary.tsv

Statistics Reported:
    — Mean expression across samples
    — Standard deviation
    — Minimum and maximum expression values
    — Number of non-missing (non-NaN) values

Requirements:
    - pandas
    - Python ≥ 3.8

Author:
    Jeffrey B. Callan
    MSc Bioinformatics Candidate, Brandeis University
    GitHub: https://github.com/jca11an
    Date: 2025-06-11
"""

import sys
import os
import pandas as pd

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 01_descriptive_summary.py <COHORT>")
        sys.exit(1)

    cohort = sys.argv[1].upper()

    # Set directory structure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))

    data_path = os.path.join(project_dir, "data", "processed", f"TCGA.{cohort}.sampleMap_HiSeqV2")
    results_path = os.path.join(project_dir, "results", "tables")
    os.makedirs(results_path, exist_ok=True)

    # File extension fallback
    if not os.path.exists(data_path) and os.path.exists(data_path + ".tsv"):
        data_path += ".tsv"

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Expression file not found:\n{data_path}")

    # Load and transpose expression matrix (genes in columns, samples in rows)
    df = pd.read_csv(data_path, sep="\t", index_col=0).T

    # Compute descriptive statistics per gene
    summary_df = pd.DataFrame({
        "mean": df.mean(skipna=True),
        "std": df.std(skipna=True),
        "min": df.min(skipna=True),
        "max": df.max(skipna=True),
        "n_nonmissing": df.count()
    })

    # Save summary statistics
    output_file = os.path.join(results_path, f"{cohort}_expression_summary.tsv")
    summary_df.to_csv(output_file, sep="\t")

    print(f"✅ Descriptive summary for {cohort} saved to:\n{output_file}")

if __name__ == "__main__":
    main()
