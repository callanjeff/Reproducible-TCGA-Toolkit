import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import os
import sys

# === USAGE ===
if len(sys.argv) != 3:
    print("Usage: python3 09_plot_prrg2_tumor_vs_normal.py <COHORT> <GENE_SYMBOL>")
    sys.exit(1)

cohort = sys.argv[1].upper()  # e.g., KIRC
gene = sys.argv[2].upper()    # e.g., PRRG2

# === RESOLVE PATH TO EXPRESSION FILE ===
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
expr_path = os.path.join(project_root, "data", "processed", f"TCGA.{cohort}.sampleMap_HiSeqV2")

# Check for optional .tsv extension
if not os.path.exists(expr_path) and os.path.exists(expr_path + ".tsv"):
    expr_path += ".tsv"

# Validate path
if not os.path.exists(expr_path):
    print(f"❌ Expression file not found at expected path:\n{expr_path}")
    sys.exit(1)

print(f"📂 Loading expression matrix from: {expr_path}")

# === LOAD EXPRESSION MATRIX ===
df = pd.read_csv(expr_path, sep="\t", index_col=0).T  # Samples as rows

# === LABEL SAMPLE TYPES FROM BARCODE ===
def label_sample(sample_id):
    code = sample_id.split("-")[3][:2]
    return "Tumor" if code == "01" else "Normal" if code == "11" else "Other"

df["SampleType"] = df.index.map(label_sample)
df = df[df["SampleType"].isin(["Tumor", "Normal"])]  # Keep only Tumor and Normal

# === GENE VALIDATION ===
if gene not in df.columns:
    print(f"❌ Gene '{gene}' not found in expression matrix.")
    sys.exit(1)

df["Expression"] = df[gene]

# === PLOTTING ===
sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="SampleType", y="Expression", palette="Set2")
sns.stripplot(data=df, x="SampleType", y="Expression", color='black', alpha=0.4, jitter=True)

# === STATISTICS ===
tumor_vals = df[df["SampleType"] == "Tumor"]["Expression"]
normal_vals = df[df["SampleType"] == "Normal"]["Expression"]
t_stat, p_val = ttest_ind(tumor_vals, normal_vals, equal_var=False)

# === Annotate plot ===
plt.title(f"{gene} in {cohort}: Tumor vs. Normal\np = {p_val:.2e}")
plt.ylabel("Expression (log2 RSEM + 1)")
plt.xlabel("")
plt.tight_layout()

# === OUTPUT DIRECTORY AND SAVE ===
output_dir = os.path.join(project_root, "results", "figures")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"{gene}_{cohort}_tumor_vs_normal.png")
plt.savefig(output_path, dpi=300)
print(f"✅ Plot saved: {output_path}")

