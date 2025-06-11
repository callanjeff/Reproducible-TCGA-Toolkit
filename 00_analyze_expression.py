"""
Script: 00_analyze_expression.py

Description:
    Extracts gene-specific expression data from a TCGA RNA-seq matrix 
    for a given gene and cancer cohort. The script loads a processed 
    expression file (typically from UCSC Xena), transposes it, and 
    exports the expression values for the specified gene across all 
    patient samples.

Usage:
    python3 00_analyze_expression.py <GENE_SYMBOL> <TCGA_COHORT>
    Example: python3 00_analyze_expression.py PRRG2 LUAD

Inputs:
    - <GENE_SYMBOL>: Name of the gene (e.g., PRRG2, CD8A)
    - <TCGA_COHORT>: TCGA cancer type abbreviation (e.g., LUAD, KIRC)
    - Expression file located at: data/processed/TCGA.<COHORT>.sampleMap_HiSeqV2 
      (or fallback to .tsv extension)

Outputs:
    - A tab-separated file containing the expression values for the specified gene
      across all samples, saved to: results/tables/<COHORT>_<GENE>_expression.tsv

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
    if len(sys.argv) != 3:
        print("Usage: python3 00_analyze_expression.py <GENE> <COHORT>")
        sys.exit(1)

    gene = sys.argv[1]
    cohort = sys.argv[2].upper()

    # Determine script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))

    # Define data and output paths
    data_path = os.path.join(project_dir, "data", "processed", f"TCGA.{cohort}.sampleMap_HiSeqV2")
    results_path = os.path.join(project_dir, "results", "tables")
    os.makedirs(results_path, exist_ok=True)

    # Attempt fallback if file extension is missing
    if not os.path.exists(data_path) and os.path.exists(data_path + ".tsv"):
        data_path += ".tsv"

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Expression file not found:\n{data_path}")

    # Load and transpose expression matrix (genes in columns, samples in rows)
    df = pd.read_csv(data_path, sep="\t", index_col=0).T

    # Extract gene expression vector
    if gene not in df.columns:
        raise KeyError(f"Gene {gene} not found in expression data columns.")

    gene_vector = df[gene]
    output_file = os.path.join(results_path, f"{cohort}_{gene}_expression.tsv")
    gene_vector.to_csv(output_file, sep="\t")

    print(f"Expression data for {gene} in {cohort} saved to:\n{output_file}")

if __name__ == "__main__":
    main()
