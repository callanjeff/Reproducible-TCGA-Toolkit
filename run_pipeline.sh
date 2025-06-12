#!/bin/bash

# -----------------------------------------
# TCGA Pipeline Runner (Universal)
# Usage: ./run_pipeline.sh <COHORT> <GENE>
# Example: ./run_pipeline.sh KIRC PRRG2
# Author: Jeffrey B. Callan
# Date: 2025-06-11
# -----------------------------------------

# --- Argument check ---
if [ "$#" -ne 2 ]; then
    echo "❌ Usage: ./run_pipeline.sh <COHORT> <GENE>"
    echo "   Example: ./run_pipeline.sh KIRC PRRG2"
    exit 1
fi

COHORT=$1
GENE=$2

echo "🔍 Running TCGA pipeline for gene: $GENE | cohort: $COHORT"
echo "------------------------------------------------------------"

# 01 - Descriptive summary (full cohort gene statistics)
python3 01_descriptive_summary.py $COHORT

# 02 - Kaplan–Meier survival analysis + log-rank test
python3 02_survival_analysis.py --gene $GENE --cohort $COHORT

# 03 - Co-expression analysis: Pearson r + p-values
python3 03_coexpression_analysis.py --gene $GENE --cohort $COHORT

# 04 - KEGG enrichment analysis on top 50 co-expressed genes
python3 04_enrichment_analysis.py --gene $GENE --cohort $COHORT

# 05 - Multi-omics comparison (CNV, methylation, expression)
python3 05_multiomics_comparison.py $COHORT

# 06 - Multi-omics visualization (barplots, heatmaps, etc.)
python3 06_multiomics_visualization.py $COHORT

# 07 - Full visualization suite (KM, distplot, coexpression heatmap, GSEA barplot)
python3 07_generate_visuals.py --cohort $COHORT

# 08 - Tumor vs. normal boxplot for PRRG2 expression
python3 08_plot_tumor_vs_normal.py $COHORT $GENE

echo "✅ Pipeline complete for $GENE in $COHORT"
