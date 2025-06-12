"""
Script: 04_enrichment_analysis.py

Description:
    Performs functional enrichment analysis (e.g., GO, KEGG) on a user-provided gene 
    list using gseapy or similar enrichment libraries. Designed for downstream 
    interpretation of differentially expressed or co-expressed gene sets.

Usage:
    python3 04_enrichment_analysis.py [OPTIONS]
    Example: python3 04_enrichment_analysis.py gene_list.txt

This script includes ✅ and ❌ print outputs to provide visual feedback on successful execution or errors.

Requirements:
    - pandas, gseapy
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
import os
from gseapy import enrichr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', required=True)
    parser.add_argument('--gene', required=True)
    args = parser.parse_args()

    # Get base directory (2 levels up from script location)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Construct paths relative to project layout
    coexp_path = os.path.join(base_dir, "results", "tables", f"{args.cohort}_{args.gene}_top50_coexpression.csv")
    out_path = os.path.join(base_dir, "results", "tables", f"{args.cohort}_{args.gene}_kegg_enrichment.csv")

    if not os.path.exists(coexp_path):
        raise FileNotFoundError(f"❌ File not found: {coexp_path}")

    ranked_genes = pd.read_csv(coexp_path, index_col=0).head(100).index.tolist()

    enr = enrichr(gene_list=ranked_genes,
                  gene_sets='KEGG_2021_Human',
                  organism='Human')

    res = enr.results
    res.to_csv(out_path, index=False)
    print(f"✅ Enrichment results saved to:\n{out_path}")

if __name__ == "__main__":
    main()
