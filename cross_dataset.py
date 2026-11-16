"""Compare schemas and common-column statistics across multiple CSV datasets."""
from __future__ import annotations
import argparse, csv, json, math, re
from collections import Counter
from pathlib import Path
from statistics import median

MISSING={"","na","n/a","null","none","nan","missing","-"}

def clean(v):
    if v is None or str(v).strip().lower() in MISSING:return None
    s=str(v).strip().replace(",","").replace("$","").replace("%",""); s=re.sub(r"^\((.*)\)$",r"-\1",s)
    try:return float(s)
    except ValueError:return None

def read(path):
    with path.open("r",encoding="utf-8-sig",newline="",errors="replace") as f:
        r=csv.DictReader(f); rows=list(r); return rows,list(r.fieldnames or [])

def stat(values):
    non=[str(v).strip() for v in values if v is not None and str(v).strip().lower() not in MISSING]
    parsed=[clean(v) for v in non]; ratio=sum(x is not None for x in parsed)/len(non) if non else 0
    if non and ratio>=.90:
        nums=[x for x in parsed if x is not None]; n=len(nums); m=sum(nums)/n
        sd=0 if n==1 else math.sqrt(sum((x-m)**2 for x in nums)/(n-1))
        return {"type":"numeric","count":n,"mean":m,"median":median(nums),"min":min(nums),"max":max(nums),"std":sd}
    c=Counter(non); mode,f=c.most_common(1)[0] if c else (None,0)
    return {"type":"categorical","count":len(non),"unique":len(c),"mode":mode,"mode_frequency":f}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("paths",nargs="+",type=Path); ap.add_argument("--labels",nargs="*"); ap.add_argument("--output-dir",type=Path,default=Path("outputs/cross_dataset")); args=ap.parse_args()
    if args.labels and len(args.labels)!=len(args.paths):raise SystemExit("--labels count must match paths count")
    labels=args.labels or [p.stem for p in args.paths]; args.output_dir.mkdir(parents=True,exist_ok=True)
    data={}; schemas={}
    for label,path in zip(labels,args.paths):
        rows,cols=read(path); data[label]=rows; schemas[label]=cols
    common=sorted(set.intersection(*(set(c) for c in schemas.values()))) if schemas else []
    allcols=set.union(*(set(c) for c in schemas.values())) if schemas else set()
    report={"datasets":{},"common_columns":common,"common_column_stats":{}}
    for label in labels:
        report["datasets"][label]={"row_count":len(data[label]),"column_count":len(schemas[label]),"columns":schemas[label],"unique_columns":sorted(set(schemas[label])-set.union(*(set(schemas[o]) for o in labels if o!=label))) if len(labels)>1 else schemas[label]}
    for col in common:
        report["common_column_stats"][col]={label:stat([r.get(col,"") for r in data[label]]) for label in labels}
    (args.output_dir/"cross_dataset_summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    md=["# Automated Cross-Dataset Comparison","", "## Dataset Shapes","", "| Dataset | Rows | Columns |", "|---|---:|---:|"]
    for label in labels: md.append(f"| {label} | {len(data[label]):,} | {len(schemas[label]):,} |")
    md += ["","## Common Columns",""] + ([", ".join(f"`{c}`" for c in common)] if common else ["No exact column names are shared across all supplied files."])
    md += ["","## Schema Differences",""]
    for label in labels:
        unique=report["datasets"][label]["unique_columns"]; md.append(f"### {label}\n\nUnique columns: "+(", ".join(f"`{c}`" for c in unique) if unique else "None"))
    md += ["","## Common-Column Statistics",""]
    for col in common:
        md.append(f"### `{col}`")
        for label in labels:
            s=report["common_column_stats"][col][label]
            if s["type"]=="numeric":md.append(f"- **{label}:** n={s['count']:,}, mean={s['mean']:.4f}, median={s['median']:.4f}, min={s['min']:.4f}, max={s['max']:.4f}")
            else:md.append(f"- **{label}:** n={s['count']:,}, unique={s['unique']:,}, mode={s['mode']} ({s['mode_frequency']:,})")
        md.append("")
    (args.output_dir/"CROSS_DATASET_AUTO.md").write_text("\n".join(md),encoding="utf-8")
    print(f"Compared {len(labels)} datasets. Common columns: {len(common)}")
    print(f"Outputs written to {args.output_dir}")
if __name__=="__main__":main()
