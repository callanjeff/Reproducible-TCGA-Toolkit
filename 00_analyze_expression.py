#!/usr/bin/env python3

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

#!/usr/bin/env python3

import sys
import os
import pandas as pd

def main():
    # ✅ Check argument count
    if len(sys.argv) != 3:
        print("❌ Usage: python3 analyze_expression.py <GENE> <COHORT>")
        sys.exit(1)

    # ✅ Parse command-line arguments
    gene = sys.argv[1]
    cohort = sys.argv[2].upper()

    # ✅ Resolve absolute script and project paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    data_path = os.path.join(project_dir, "data", "processed", f"TCGA.{cohort}.sampleMap_HiSeqV2")
    results_path = os.path.join(project_dir, "results", "tables")
    os.makedirs(results_path, exist_ok=True)

    # 🔁 Fallback to .tsv extension if needed
    if not os.path.exists(data_path) and os.path.exists(data_path + ".tsv"):
        data_path += ".tsv"

    # ❌ Fail if expression file still not found
    if not os.path.exists(data_path):
        print(f"❌ Expression file not found:\n{data_path}")
        sys.exit(1)

    print("✅ Expression file located.")

    # ✅ Load expression matrix
    try:
        df = pd.read_csv(data_path, sep="\t", index_col=0)
        print("✅ Expression matrix loaded.")
    except Exception as e:
        print(f"❌ Failed to load expression matrix:\n{e}")
        sys.exit(1)

    # ❌ Check if requested gene exists
    if gene not in df.index:
        print(f"❌ Gene '{gene}' not found in expression matrix.")
        sys.exit(1)

    # ✅ Extract gene expression vector
    expression_vector = df.loc[gene]
    output_file = os.path.join(results_path, f"{cohort}_{gene}_expression.tsv")
    try:
        expression_vector.to_csv(output_file, sep="\t", header=False)
        print(f"✅ Expression vector for {gene} saved to:\n{output_file}")
    except Exception as e:
        print(f"❌ Failed to save expression vector:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
