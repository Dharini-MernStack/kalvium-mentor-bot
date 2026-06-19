"""
One-time script: Convert pasted LLD TSV data into xlsx files in data/ folder.
Run once: python build_lld_data.py
"""
import pandas as pd
import os, glob

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TSV_DIR = os.path.join(DATA_DIR, "tsv_inbox")

os.makedirs(TSV_DIR, exist_ok=True)

print("Place .tsv files in data/tsv_inbox/ and run this script.")
print(f"TSV inbox: {TSV_DIR}")

# Process any .tsv files in inbox
for tsv_file in glob.glob(os.path.join(TSV_DIR, "*.tsv")):
    name = os.path.splitext(os.path.basename(tsv_file))[0]
    out_path = os.path.join(DATA_DIR, f"{name}_lld.xlsx")
    
    df = pd.read_csv(tsv_file, sep="\t")
    # Drop fully empty rows
    df = df.dropna(how="all").reset_index(drop=True)
    # Drop rows where all important columns are empty
    key_cols = [c for c in df.columns if c.lower() in ["module name", "lu title", "lu name", "lu sequence #", "lu sequence"]]
    if key_cols:
        df = df.dropna(subset=key_cols, how="all").reset_index(drop=True)
    
    df.to_excel(out_path, index=False)
    print(f"✅ {name} → {out_path} ({len(df)} rows)")
