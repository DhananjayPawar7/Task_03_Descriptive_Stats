"""Verify that Pure Python, Pandas, and Polars dataset summaries agree."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

def close(a,b,tol=1e-8):
    if a is None or b is None:return a is b
    return math.isclose(float(a),float(b),rel_tol=tol,abs_tol=tol)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("output_dir",type=Path); args=ap.parse_args()
    names=["pure_python","pandas","polars"]
    docs={n:json.loads((args.output_dir/f"{n}_dataset_summary.json").read_text(encoding="utf-8")) for n in names}
    base=docs["pure_python"]; errors=[]
    for n in ["pandas","polars"]:
        d=docs[n]
        for key in ["row_count","column_count"]:
            if d[key]!=base[key]:errors.append(f"{n}: {key} {d[key]} != {base[key]}")
        if set(d["columns"])!=set(base["columns"]): errors.append(f"{n}: column sets differ"); continue
        for col,b in base["columns"].items():
            x=d["columns"][col]
            for k in ["type","count","missing"]:
                if x.get(k)!=b.get(k):errors.append(f"{n}:{col}:{k} {x.get(k)} != {b.get(k)}")
            if b.get("type")=="numeric":
                for k in ["numeric_count","mean","min","max","std","median"]:
                    if k=="numeric_count":
                        if x.get(k)!=b.get(k):errors.append(f"{n}:{col}:{k} mismatch")
                    elif not close(x.get(k),b.get(k),1e-7):errors.append(f"{n}:{col}:{k} {x.get(k)} != {b.get(k)}")
            else:
                for k in ["unique","mode_frequency"]:
                    if x.get(k)!=b.get(k):errors.append(f"{n}:{col}:{k} mismatch")
                if x.get("mode")!=b.get("mode"):errors.append(f"{n}:{col}:mode mismatch")
    if errors:
        print("FAIL: summaries do not fully agree")
        for e in errors[:100]:print("-",e)
        raise SystemExit(1)
    print("PASS: core dataset-level statistics agree across Pure Python, Pandas, and Polars.")
if __name__=="__main__":main()
