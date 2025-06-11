#!/bin/bash

# Usage: ./run_pipeline.sh PRRG2 LUAD

GENE=$1
COHORT=$2

if [[ -z "$GENE" || -z "$COHORT" ]]; then
    echo "❌ Usage: ./run_pipeline.sh <GENE_SYMBOL> <TCGA_COHORT>"
    exit 1
fi

echo "🔄 Starting Reproducible-TCGA-Toolkit pipeline for gene: $GENE | cohort: $COHORT"
echo "------------------------------------------------------------"

# Step 00 - Expression Extraction
python3 scripts/00_analyze_expression.py "$GENE" "$COHORT" || exit 1

# Step 01 - Expression Summary
python3 scripts/01_descriptive_summary.py "$COHORT" || exit 1

# Step 02 - Survival Analysis
python3 scripts/02_survival_analysis.py "$GENE" "$COHORT" || exit 1

# Step 03 - Co-expression Analysis
python3 scripts/03_coexpression_analysis.py "$GENE" "$COHORT" || exit 1

# Step 04 - Enrichment Analysis
python3 scripts/04_enrichment_analysis.py "${GENE}_coexpressed_genes.txt" || exit 1

# Step 05 - Multi-omics Comparison
python3 scripts/05_multiomics_comparison.py "$GENE" "$COHORT" || exit 1

# Step 06 - Multi-omics Visualization
python3 scripts/06_multiomics_visualization.py "$GENE" "$COHORT" || exit 1

# Step 07 - Generate Publication Figures
python3 scripts/07_generate_visuals.py "$GENE" "$COHORT" || exit 1

# Step 08 - Tumor vs Normal Plotting
python3 scripts/08_plot_tumor_vs_normal.py "$GENE" "$COHORT" || exit 1

echo "✅ Pipeline completed successfully for $GENE in $COHORT"
