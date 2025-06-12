"""
Script: 05_multiomics_comparison.py

Description:
    Compares expression data with additional omics layers (e.g., CNV, RPPA, methylation) 
    for integrative biomarker analysis. Enables layered molecular interpretation across 
    platforms.

Usage:
    python3 05_multiomics_comparison.py [OPTIONS]
    Example: python3 05_multiomics_comparison.py PRRG2 LUAD

This script includes ✅ and ❌ print outputs to provide visual feedback on successful execution or errors.

Requirements:
    - pandas, numpy
    - Python ≥ 3.8

Author:
    Jeffrey B. Callan
    MSc Bioinformatics Candidate, Brandeis University
    GitHub: https://github.com/jca11an
    Date: 2025-06-11
"""

#!/usr/bin/env python3

import sys
import pandas as pd
import os

# Parse cohort argument
if len(sys.argv) < 2:
    print("❌ Usage: python3 05_multiomics_comparison.py <COHORT>")
    sys.exit(1)

cohort = sys.argv[1]
gene_of_interest = "PRRG2"

# Resolve base directory from script location
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))

# Construct file paths
data_dir = os.path.join(base_dir, "data", "processed")
meta_dir = os.path.join(base_dir, "data", "metadata")
results_dir = os.path.join(base_dir, "results", "tables")

expr_file = os.path.join(data_dir, f"TCGA.{cohort}.sampleMap_HiSeqV2")
cnv_file = os.path.join(data_dir, f"TCGA.{cohort}.sampleMap_Gistic2_CopyNumber_Gistic2_all_thresholded.by_genes")
meth_file = os.path.join(data_dir, f"TCGA.{cohort}.sampleMap_HumanMethylation450")
probe_map_file = os.path.join(data_dir, "probeMap_hugo_gencode_good_hg19_V24lift37_probemap")

# Load expression data
expr = pd.read_csv(expr_file, sep='\t', index_col=0).T
expr = expr[[gene_of_interest]].rename(columns={gene_of_interest: "expression"})

# Load CNV data
cnv = pd.read_csv(cnv_file, sep='\t', index_col=0).T
cnv = cnv[[gene_of_interest]].rename(columns={gene_of_interest: "cnv"})

# Load methylation and probe map
meth = pd.read_csv(meth_file, sep='\t', index_col=0).T
probe_map = pd.read_csv(probe_map_file, sep='\t', header=None, names=["probe", "gene"])

# Extract PRRG2 probes and average
prrg2_probes = probe_map[probe_map["gene"] == gene_of_interest]["probe"].values
meth_filtered = meth[prrg2_probes]
meth["methylation"] = meth_filtered.mean(axis=1)
meth = meth[["methylation"]]

# Merge all data
merged = expr.join(cnv, how="inner").join(meth, how="inner")

# Save output
out_file = os.path.join(results_dir, f"{cohort}_multiomics_PRRG2.tsv")
merged.to_csv(out_file, sep='\t')

print(f"✅ Merged multi-omics table for {gene_of_interest} in {cohort} saved to:\n{out_file}")
