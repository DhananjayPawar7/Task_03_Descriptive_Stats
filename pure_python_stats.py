"""Task 03 generalized descriptive statistics using Python standard library only."""
from __future__ import annotations
import argparse, csv, json, math, re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

MISSING = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}
PRIMARY_GROUP_CANDIDATES = ["page_id","account_id","user_id","author_id","page_name","account_name","username","screen_name","handle"]
RECORD_ID_CANDIDATES = ["ad_id","post_id","tweet_id","status_id","message_id","id"]

def is_missing(v):
    return v is None or str(v).strip().lower() in MISSING

def clean_number(v):
    if is_missing(v): return None
    s=str(v).strip().replace(",","").replace("$","").replace("%","")
    s=re.sub(r"^\((.*)\)$", r"-\1", s)
    try: return float(s)
    except ValueError: return None

def sample_std(values):
    if not values: return None
    if len(values)==1: return 0.0
    m=sum(values)/len(values)
    return math.sqrt(sum((x-m)**2 for x in values)/(len(values)-1))

def infer_numeric(values, threshold=0.90):
    non=[v for v in values if not is_missing(v)]
    if not non: return False
    parsed=sum(clean_number(v) is not None for v in non)
    return parsed/len(non) >= threshold

def summarize_column(values):
    non=[str(v).strip() for v in values if not is_missing(v)]
    out={"count":len(non),"missing":len(values)-len(non)}
    if infer_numeric(values):
        nums=[clean_number(v) for v in non]
        nums=[x for x in nums if x is not None]
        out.update({"type":"numeric","numeric_count":len(nums),"mean":sum(nums)/len(nums) if nums else None,
                    "min":min(nums) if nums else None,"max":max(nums) if nums else None,
                    "std":sample_std(nums),"median":median(nums) if nums else None})
    else:
        c=Counter(non); mode,freq=c.most_common(1)[0] if c else (None,0)
        out.update({"type":"categorical","unique":len(c),"mode":mode,"mode_frequency":freq,"top5":c.most_common(5)})
    return out

def load_csv(path):
    with path.open("r",encoding="utf-8-sig",newline="",errors="replace") as f:
        reader=csv.DictReader(f); rows=list(reader); cols=list(reader.fieldnames or [])
    return rows,cols

def summarize_dataset(rows,cols):
    return {"row_count":len(rows),"column_count":len(cols),"columns":{c:summarize_column([r.get(c,"") for r in rows]) for c in cols}}

def auto_groups(cols):
    s=set(cols); groups=[]
    primary=next((c for c in PRIMARY_GROUP_CANDIDATES if c in s),None)
    record=next((c for c in RECORD_ID_CANDIDATES if c in s),None)
    if primary: groups.append([primary])
    if primary and record and record!=primary: groups.append([primary,record])
    elif record and not primary: groups.append([record])
    return groups

def grouped_counts(rows, keys):
    counts=Counter(tuple(str(r.get(k,"")) for k in keys) for r in rows)
    return counts

def write_group_counts(counts, keys, path):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(keys+["row_count"])
        for key,n in counts.most_common(): w.writerow(list(key)+[n])

def write_top_group_stats(rows, keys, cols, counts, path, top_n=50):
    selected={k for k,_ in counts.most_common(top_n)}
    buckets=defaultdict(list)
    for r in rows:
        key=tuple(str(r.get(k,"")) for k in keys)
        if key in selected: buckets[key].append(r)
    with path.open("w",encoding="utf-8") as f:
        for key,_ in counts.most_common(top_n):
            record={"group":dict(zip(keys,key)),"row_count":len(buckets[key]),"summary":summarize_dataset(buckets[key],cols)}
            f.write(json.dumps(record,ensure_ascii=False)+"\n")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data_path",type=Path)
    ap.add_argument("--output-dir",type=Path,default=Path("outputs"))
    ap.add_argument("--group",action="append",default=[],help="Comma-separated group keys; may be repeated. If omitted, keys are auto-detected.")
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    rows,cols=load_csv(args.data_path)
    summary=summarize_dataset(rows,cols)
    (args.output_dir/"pure_python_dataset_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    groups=[g.split(",") for g in args.group] if args.group else auto_groups(cols)
    print(f"File: {args.data_path}\nRows: {len(rows):,} | Columns: {len(cols):,}")
    print("Detected groups:", groups if groups else "none")
    for keys in groups:
        if any(k not in cols for k in keys):
            print(f"Skipping {keys}: missing column(s)"); continue
        counts=grouped_counts(rows,keys); label="__".join(keys)
        write_group_counts(counts,keys,args.output_dir/f"pure_python_group_{label}_counts.csv")
        write_top_group_stats(rows,keys,cols,counts,args.output_dir/f"pure_python_group_{label}_top50.jsonl")
        print(f"\nGrouped by {keys}: {len(counts):,} groups")
        for key,n in counts.most_common(10): print(f"  {key}: {n:,}")
    print(f"\nOutputs written to {args.output_dir}")
if __name__=="__main__": main()
