# 06_multiomics_visualization.py
# Author: Jeff Callan
# Purpose: Generate multi-omics correlation plots for PRRG2 across TCGA cohorts

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
from scipy.stats import pearsonr

# Argument parsing
parser = argparse.ArgumentParser(description="Generate multi-omics visualizations for PRRG2")
parser.add_argument("cohort", help="TCGA cohort name (e.g., CESC or KIRC)")
args = parser.parse_args()

# Define paths
project_root = os.path.expanduser(f"~/Bioinformatics/TCGA_{args.cohort}_PRRG2_Project")
input_csv = os.path.join(project_root, "results", "tables", f"{args.cohort}_multiomics_PRRG2.tsv")
output_dir = os.path.join(project_root, "results", "figures")
os.makedirs(output_dir, exist_ok=True)

# Load multi-omics data (TSV) and clean column names
df = pd.read_csv(input_csv, sep="\t", index_col=0)
df.columns = df.columns.str.strip()

# Bin CNV values for boxplot
df['cnv_bin'] = pd.cut(df['cnv'], bins=[-2, -0.5, 0.5, 2], labels=['Deletion', 'Neutral', 'Amplification'])

# Compute Pearson correlations (drop NaNs)
cnv_data = df[['expression', 'cnv']].dropna()
r_expr_cnv, p_expr_cnv = pearsonr(cnv_data['expression'], cnv_data['cnv'])

meth_data = df[['expression', 'methylation']].dropna()
if len(meth_data) >= 2:
    r_expr_meth, p_expr_meth = pearsonr(meth_data['expression'], meth_data['methylation'])
else:
    r_expr_meth, p_expr_meth = float('nan'), float('nan')
    print(f"⚠️ Not enough valid data points for methylation correlation in {args.cohort}")


# Set visual style
sns.set(style="whitegrid")

# Plot 1: Expression vs CNV
plt.figure(figsize=(6, 4))
sns.scatterplot(data=cnv_data, x='cnv', y='expression')
plt.title("PRRG2 Expression vs. CNV")
plt.xlabel("Copy Number Variation (Segment Mean)")
plt.ylabel("PRRG2 Expression (log2 RSEM)")
plt.annotate(f"r = {r_expr_cnv:.3f}\np = {p_expr_cnv:.3f}", 
             xy=(0.05, 0.85), xycoords='axes fraction', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white'))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"{args.cohort}_expression_vs_cnv.png"))
plt.close()

# Plot 2: Expression vs Methylation
plt.figure(figsize=(6, 4))
sns.scatterplot(data=meth_data, x='methylation', y='expression')
plt.title("PRRG2 Expression vs. Methylation")
plt.xlabel("Methylation Beta Value")
plt.ylabel("PRRG2 Expression (log2 RSEM)")
plt.annotate(f"r = {r_expr_meth:.3f}\np = {p_expr_meth:.3f}", 
             xy=(0.05, 0.85), xycoords='axes fraction', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='gray', facecolor='white'))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"{args.cohort}_expression_vs_methylation.png"))
plt.close()

# Plot 3: Boxplot - Expression by CNV Category
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='cnv_bin', y='expression', hue='cnv_bin', palette='muted', legend=False)

plt.title("PRRG2 Expression by CNV Category")
plt.xlabel("CNV Category")
plt.ylabel("PRRG2 Expression (log2 RSEM)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"{args.cohort}_expression_by_cnv_category.png"))
plt.close()

# Save correlation stats to CSV
corr_df = pd.DataFrame({
    'Comparison': ['Expression vs CNV', 'Expression vs Methylation'],
    'Pearson_r': [r_expr_cnv, r_expr_meth],
    'p_value': [p_expr_cnv, p_expr_meth]
})
corr_df.to_csv(os.path.join(output_dir, f"{args.cohort}_PRRG2_correlation_stats.csv"), index=False)

print(f"✅ Figures and correlation results for {args.cohort} saved to: {output_dir}")
