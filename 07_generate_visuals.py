"""
Script: 07_generate_visuals.py

Description:
    Creates reusable, publication-quality plots for expression analysis, survival curves, 
    co-expression scatter plots, and multi-omics comparisons. Designed to standardize and 
    simplify figure creation for reporting and manuscripts.

Usage:
    python3 07_generate_visuals.py [OPTIONS]
    Example: python3 07_generate_visuals.py PRRG2 LUAD

This script includes ✅ and ❌ print outputs to provide visual feedback on successful execution or errors.

Requirements:
    - pandas, matplotlib, seaborn
    - Python ≥ 3.8

Author:
    Jeffrey B. Callan
    MSc Bioinformatics Candidate, Brandeis University
    GitHub: https://github.com/jca11an
    Date: 2025-06-11
"""

#!/usr/bin/env python3

import os
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px  # type: ignore
from lifelines import KaplanMeierFitter

# -------------------------
# Parse command-line input
# -------------------------
parser = argparse.ArgumentParser(description="Generate PRRG2 visualizations for a TCGA cohort.")
parser.add_argument('--cohort', type=str, required=True, help='TCGA cohort abbreviation (e.g., KIRC, CESC, LUAD)')
args = parser.parse_args()
cohort = args.cohort.upper()

# -------------------------
# Set project directories
# -------------------------
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_dir = os.path.join(root, "data", "processed")
metadata_dir = os.path.join(root, "data", "metadata")
figures_dir = os.path.join(root, "results", "figures")
tables_dir = os.path.join(root, "results", "tables")
os.makedirs(figures_dir, exist_ok=True)

# -------------------------
# Load expression matrix
# -------------------------
base_expr_file = os.path.join(data_dir, f"TCGA.{cohort}.sampleMap_HiSeqV2")
if os.path.exists(base_expr_file):
    expr_file = base_expr_file
elif os.path.exists(base_expr_file + ".tsv"):
    expr_file = base_expr_file + ".tsv"
elif os.path.exists(base_expr_file + ".txt"):
    expr_file = base_expr_file + ".txt"
else:
    raise FileNotFoundError(f"❌ Expression file not found for {cohort} at: {base_expr_file}[.tsv/.txt]")

print(f"✅ Expression file used: {expr_file}")
full_expr_df = pd.read_csv(expr_file, sep="\t", index_col=0)
expr_df = full_expr_df.loc[["PRRG2"]].T
expr_df.index = expr_df.index.str[:12]
expr_df.columns = ["PRRG2"]

# -------------------------
# Load clinical metadata
# -------------------------
clinical_file = os.path.join(metadata_dir, f"TCGA.{cohort}.sampleMap_{cohort}_clinicalMatrix")
if not os.path.exists(clinical_file):
    raise FileNotFoundError(f"❌ Clinical file not found: {clinical_file}")
clinical_df = pd.read_csv(clinical_file, sep="\t", index_col=0)
clinical_df.index = clinical_df.index.str[:12]

# -------------------------
# Load survival metadata
# -------------------------
survival_df = pd.read_csv(os.path.join(metadata_dir, "survival_tcga_cdr.tsv"), sep="\t")
survival_df.set_index("_PATIENT", inplace=True)
merged_clinical = clinical_df.join(survival_df, how="left")

# -------------------------
# Load co-expression results
# -------------------------
coexp_path = os.path.join(tables_dir, f"{cohort}_PRRG2_top50_coexpression.csv")
if not os.path.exists(coexp_path):
    raise FileNotFoundError(f"❌ Coexpression file not found: {coexp_path}")
coexp_df = pd.read_csv(coexp_path, names=["gene", "correlation"], header=0)

# -------------------------
# Load KEGG enrichment results
# -------------------------
gsea_path = os.path.join(tables_dir, f"{cohort}_PRRG2_kegg_enrichment.csv")
if not os.path.exists(gsea_path):
    raise FileNotFoundError(f"❌ KEGG enrichment file not found: {gsea_path}")
gsea_df = pd.read_csv(gsea_path)

# -------------------------
# Visualization setup
# -------------------------
sns.set(style='whitegrid', font_scale=1.2)

# 1. PRRG2 Expression Distribution
plt.figure(figsize=(8, 6))
sns.histplot(expr_df["PRRG2"], bins=30, kde=True, color='steelblue')
plt.title(f"Distribution of PRRG2 Expression in {cohort}")
plt.xlabel("log2(RSEM + 1)")
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, f"{cohort.lower()}_prrg2_expression_distribution.png"))
plt.close()

# 2. PRRG2 Expression vs OS Status
if "OS" in merged_clinical.columns:
    merged = expr_df.join(merged_clinical["OS"]).dropna()
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="OS", y="PRRG2", data=merged, hue="OS", palette="Set2", legend=False)
    sns.stripplot(x="OS", y="PRRG2", data=merged, color="black", alpha=0.3)
    plt.title(f"PRRG2 Expression vs Overall Survival ({cohort})")
    plt.savefig(os.path.join(figures_dir, f"{cohort.lower()}_prrg2_vs_os.png"))
    plt.close()

# 3. Kaplan-Meier Curve by PRRG2 Expression
if {"OS", "OS.time"}.issubset(merged_clinical.columns):
    km_data = expr_df.join(merged_clinical[["OS", "OS.time"]]).dropna()
    km_data["event"] = km_data["OS"]
    km_data["time"] = km_data["OS.time"]
    median_expr = km_data["PRRG2"].median()
    km_data["group"] = (km_data["PRRG2"] >= median_expr).map({True: "High", False: "Low"})

    kmf = KaplanMeierFitter()
    plt.figure(figsize=(8, 6))
    for group in ["High", "Low"]:
        subset = km_data[km_data["group"] == group]
        kmf.fit(subset["time"], event_observed=subset["event"], label=group)
        kmf.plot_survival_function()

    plt.title(f"Kaplan-Meier Curve by PRRG2 Expression ({cohort})")
    plt.xlabel("Days")
    plt.ylabel("Survival Probability")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, f"{cohort.lower()}_km_prrg2_expression.png"))
    plt.close()

# 4. Co-expression Heatmap
top50 = coexp_df.sort_values("correlation", ascending=False).head(50)
plt.figure(figsize=(12, 6))
sns.heatmap(
    top50.set_index("gene")["correlation"].to_frame().T,
    cmap="coolwarm", annot=True, cbar_kws={'label': 'Pearson r'}
)
plt.title(f"Top 50 Genes Co-expressed with PRRG2 ({cohort})")
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, f"{cohort.lower()}_coexpression_heatmap_top50.png"))
plt.close()

# 5. KEGG Enrichment Bar Plot
if not gsea_df.empty:
    top_gsea = gsea_df.sort_values("Combined Score", ascending=False).head(10).copy()
    top_gsea = top_gsea.rename(columns={
        "Combined Score": "NES",
        "Term": "pathway",
        "P-value": "pval"
    })

    fig = px.bar(
        top_gsea,
        x="NES",
        y="pathway",
        color="pval",
        orientation="h",
        color_continuous_scale="Plasma_r",
        title=f"Top Enriched KEGG Pathways Correlated with PRRG2 ({cohort})"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    fig.write_image(os.path.join(figures_dir, f"{cohort.lower()}_gsea_top_pathways.png"))

print(f"✅ All visualizations for {cohort} saved to: {figures_dir}")

