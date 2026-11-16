"""Task 03 generalized descriptive statistics for any CSV using Pandas."""
from __future__ import annotations
import argparse, json, re
from collections import Counter
from pathlib import Path
import pandas as pd
from common_utils import MISSING, auto_groups

def clean_number(v):
    if v is None or str(v).strip().lower() in MISSING: return None
    s=str(v).strip().replace(",","").replace("$","").replace("%","")
    s=re.sub(r"^\((.*)\)$",r"-\1",s)
    try:return float(s)
    except ValueError:return None

def summarize_series(s: pd.Series):
    vals=s.tolist(); non=[str(v).strip() for v in vals if v is not None and str(v).strip().lower() not in MISSING]
    out={"count":len(non),"missing":len(vals)-len(non)}
    parsed=[clean_number(v) for v in non]; ratio=(sum(x is not None for x in parsed)/len(non)) if non else 0
    if non and ratio>=0.90:
        nums=pd.Series([x for x in parsed if x is not None],dtype="float64")
        out.update({"type":"numeric","numeric_count":int(nums.count()),"mean":float(nums.mean()),"min":float(nums.min()),"max":float(nums.max()),"std":float(nums.std(ddof=1)) if len(nums)>1 else 0.0,"median":float(nums.median())})
    else:
        c=Counter(non); mode,freq=c.most_common(1)[0] if c else (None,0)
        out.update({"type":"categorical","unique":len(c),"mode":mode,"mode_frequency":freq,"top5":c.most_common(5)})
    return out

def summarize_dataset(df):
    return {"row_count":int(df.shape[0]),"column_count":int(df.shape[1]),"columns":{c:summarize_series(df[c]) for c in df.columns}}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("data_path",type=Path); ap.add_argument("--output-dir",type=Path,default=Path("outputs")); ap.add_argument("--group",action="append",default=[])
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.data_path,dtype=str,keep_default_na=False,encoding="utf-8-sig",on_bad_lines="warn")
    summary=summarize_dataset(df); (args.output_dir/"pandas_dataset_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    # Required Pandas exploratory methods
    with (args.output_dir/"pandas_describe.txt").open("w",encoding="utf-8") as f:
        f.write(f"Shape: {df.shape}\n\nDtypes:\n{df.dtypes.to_string()}\n\n")
        try:f.write("Describe (all columns):\n"+df.describe(include="all").to_string()+"\n\n")
        except Exception as e:f.write(f"describe failed: {e}\n")
        missing=df.apply(lambda s:s.astype(str).str.strip().str.lower().isin(MISSING)).sum()
        f.write("Missing counts and percentages:\n"+pd.DataFrame({"missing_count":missing,"missing_percent":missing/len(df)*100}).to_string()+"\n")
    groups=[g.split(",") for g in args.group] if args.group else auto_groups(list(df.columns))
    print(f"File: {args.data_path}\nRows: {len(df):,} | Columns: {len(df.columns):,}\nDetected groups: {groups if groups else 'none'}")
    for keys in groups:
        if any(k not in df.columns for k in keys): print(f"Skipping {keys}: missing column(s)"); continue
        counts=df.groupby(keys,dropna=False).size().reset_index(name="row_count").sort_values("row_count",ascending=False)
        label="__".join(keys); counts.to_csv(args.output_dir/f"pandas_group_{label}_counts.csv",index=False)
        print(f"\nGrouped by {keys}: {len(counts):,} groups\n{counts.head(10).to_string(index=False)}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__=="__main__": main()
