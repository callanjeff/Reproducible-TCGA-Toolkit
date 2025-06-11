# Reproducible-TCGA-Toolkit

A modular, reproducible toolkit for transcriptomic and multi-omics analysis of TCGA cohorts — designed for biomarker discovery, immune profiling, and survival analysis.

---

## Overview

The Reproducible-TCGA-Toolkit is a Python-based framework for conducting multi-step cancer genomics analyses using data from The Cancer Genome Atlas (TCGA). This toolkit supports the exploration of gene expression, survival associations, immune gene co-expression, and multi-omics comparisons, enabling data-driven biomarker discovery across multiple cancer types.

The codebase is structured around modular scripts that can be executed independently or in sequence, depending on the analytical goals of the user. Originally developed as part of a graduate-level bioinformatics research project, the toolkit has been generalized for broader use across gene targets, immune signatures, and TCGA datasets.

---

## Features

— RNA-seq expression analysis and sample-level filtering  
— Clinical metadata integration and cohort-level summaries  
— Kaplan–Meier survival analysis with binary or quantile-based groupings  
— Co-expression analysis with immune-related genes (e.g., CD8A, GZMB, PDCD1, IFNG)  
— Gene set enrichment analysis based on user-defined inputs  
— Multi-omics integration including CNV, RPPA, and methylation data  
— Tumor versus normal expression visualization and statistical comparison  
— Generation of high-quality plots suitable for scientific reporting

---

## Repository Structure

```
Reproducible-TCGA-Toolkit/
├── scripts/
│   ├── 00_analyze_expression.py
│   ├── 01_descriptive_summary.py
│   ├── 02_survival_analysis.py
│   ├── 03_coexpression_analysis.py
│   ├── 04_enrichment_analysis.py
│   ├── 05_multiomics_comparison.py
│   ├── 06_multiomics_visualization.py
│   ├── 07_generate_visuals.py
│   └── 08_plot_tumor_vs_normal.py
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── figures/
│   └── tables/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Reproducible-TCGA-Toolkit.git
   cd Reproducible-TCGA-Toolkit
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and place TCGA data files in the `data/raw/` directory. Suggested sources include:  
   — UCSC Xena (https://xenabrowser.net/datapages/)  
   — GDC Data Portal (https://portal.gdc.cancer.gov/)

4. Execute analysis scripts as needed. Each script is modular and can be run independently:
   ```bash
   python scripts/02_survival_analysis.py
   ```

Scripts assume appropriate input formats (e.g., gene expression matrices, survival tables, CNV files) as typically provided by TCGA or UCSC Xena repositories.

---

## Example Applications

— Identifying genes associated with poor or improved overall survival  
— Evaluating immunological context through gene co-expression  
— Characterizing tumor-specific expression compared to normal tissue  
— Integrating multiple molecular modalities for candidate biomarker validation  
— Preparing visual figures for scientific communication or publication

---

## Requirements

— Python ≥ 3.8  
— pandas, numpy  
— matplotlib, seaborn  
— lifelines  
— scipy, statsmodels  
— gseapy (for enrichment analysis, optional)  
— tqdm, scikit-learn (optional for extended analysis)

All dependencies can be installed via the provided `requirements.txt`.

---

## Author and Contact

This toolkit was developed by:

**Jeffrey B. Callan**  
MSc Candidate in Bioinformatics, Brandeis University  
GitHub: [@jca11an](https://github.com/jca11an)  

For inquiries, issues, or collaboration requests, please open a GitHub issue or contact the author directly.

---

## License

This project is released under the MIT License. Users are free to use, modify, and redistribute the toolkit with appropriate attribution.
