"""One-command runner for Task 03: all three methods + verification + cross-dataset report."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def run(cmd):
    print("\n$", " ".join(map(str,cmd)), flush=True); subprocess.run(cmd,check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("facebook_ads",type=Path); ap.add_argument("facebook_posts",type=Path); ap.add_argument("twitter_posts",type=Path); ap.add_argument("--output-root",type=Path,default=Path("outputs")); args=ap.parse_args()
    datasets=[("facebook_ads",args.facebook_ads),("facebook_posts",args.facebook_posts),("twitter_posts",args.twitter_posts)]
    py=sys.executable
    for label,path in datasets:
        out=args.output_root/label; out.mkdir(parents=True,exist_ok=True)
        for script in ["pure_python_stats.py","pandas_stats.py","polars_stats.py"]: run([py,script,str(path),"--output-dir",str(out)])
        run([py,"verify_results.py",str(out)])
    run([py,"cross_dataset.py",str(args.facebook_ads),str(args.facebook_posts),str(args.twitter_posts),"--labels","Facebook Ads","Facebook Posts","Twitter/X Posts","--output-dir",str(args.output_root/"cross_dataset")])
    print("\nTASK 3 RUN COMPLETE")
if __name__=="__main__":main()
