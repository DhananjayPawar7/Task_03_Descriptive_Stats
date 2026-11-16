"""Task 03 generalized descriptive statistics for any CSV using Polars."""
from __future__ import annotations
import argparse, json, math, re
from collections import Counter
from pathlib import Path
import polars as pl
from common_utils import MISSING, auto_groups

def clean_number(v):
    if v is None or str(v).strip().lower() in MISSING:return None
    s=str(v).strip().replace(",","").replace("$","").replace("%","")
    s=re.sub(r"^\((.*)\)$",r"-\1",s)
    try:return float(s)
    except ValueError:return None

def summarize_values(vals):
    non=[str(v).strip() for v in vals if v is not None and str(v).strip().lower() not in MISSING]
    out={"count":len(non),"missing":len(vals)-len(non)}; parsed=[clean_number(v) for v in non]
    ratio=(sum(x is not None for x in parsed)/len(non)) if non else 0
    if non and ratio>=0.90:
        nums=[x for x in parsed if x is not None]; n=len(nums); mean=sum(nums)/n
        std=0.0 if n==1 else math.sqrt(sum((x-mean)**2 for x in nums)/(n-1))
        sn=sorted(nums); med=sn[n//2] if n%2 else (sn[n//2-1]+sn[n//2])/2
        out.update({"type":"numeric","numeric_count":n,"mean":mean,"min":min(nums),"max":max(nums),"std":std,"median":med})
    else:
        c=Counter(non); mode,freq=c.most_common(1)[0] if c else (None,0)
        out.update({"type":"categorical","unique":len(c),"mode":mode,"mode_frequency":freq,"top5":c.most_common(5)})
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("data_path",type=Path); ap.add_argument("--output-dir",type=Path,default=Path("outputs")); ap.add_argument("--group",action="append",default=[])
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    df=pl.read_csv(args.data_path,infer_schema=False,ignore_errors=True,encoding="utf8-lossy")
    summary={"row_count":df.height,"column_count":df.width,"columns":{c:summarize_values(df.get_column(c).to_list()) for c in df.columns}}
    (args.output_dir/"polars_dataset_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    # Required Polars exploratory methods
    with (args.output_dir/"polars_describe.txt").open("w",encoding="utf-8") as f:
        f.write(f"Shape: {df.shape}\nSchema: {df.schema}\n\nDescribe:\n{df.describe()}\n\n")
        f.write("Null counts:\n"+str(df.null_count())+"\n")
    groups=[g.split(",") for g in args.group] if args.group else auto_groups(df.columns)
    print(f"File: {args.data_path}\nRows: {df.height:,} | Columns: {df.width:,}\nDetected groups: {groups if groups else 'none'}")
    for keys in groups:
        if any(k not in df.columns for k in keys): print(f"Skipping {keys}: missing column(s)"); continue
        counts=df.group_by(keys).len().sort("len",descending=True).rename({"len":"row_count"})
        label="__".join(keys); counts.write_csv(args.output_dir/f"polars_group_{label}_counts.csv")
        print(f"\nGrouped by {keys}: {counts.height:,} groups\n{counts.head(10)}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__=="__main__": main()
