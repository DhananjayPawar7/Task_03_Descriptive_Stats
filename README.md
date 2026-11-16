# Task 03 — Descriptive Statistics as a Reusable Multi-Dataset System

## Project description

Task 03 generalizes the descriptive-statistics work from Tasks 1 and 2 into a reusable system. The same three implementations — **Pure Python, Pandas, and Polars** — accept a CSV path at runtime, infer column types dynamically, handle missing and mixed values, perform schema-aware grouped analysis, and produce comparable summaries without rewriting the core scripts for each dataset.

The system was successfully run against the three required 2024 election datasets:

1. Facebook Political Ads
2. Facebook Posts
3. Twitter/X Posts

All three implementations produced matching core dataset-level results for all three files. The verification step returned **PASS three times**.

## Dataset results

| Dataset | Rows | Columns |
|---|---:|---:|
| Facebook Ads | 246,745 | 41 |
| Facebook Posts | 19,009 | 56 |
| Twitter/X Posts | 27,304 | 47 |

The cross-dataset analysis found **27 exact common columns**, primarily binary content-classification features. See `CROSS_DATASET.md` for the detailed comparison.

## Dataset setup

Download the **2024 Election Social Media Data** files from the Google Drive source supplied with the assignment. Do **not** commit the datasets to GitHub.

Create a local folder named `data` and place/rename the three files as:

```text
data/facebook_political_ads.csv
data/facebook_posts.csv
data/twitter_posts.csv
```

## Environment setup (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Run the complete task

```bash
python3 run_task3.py data/facebook_political_ads.csv data/facebook_posts.csv data/twitter_posts.csv
```

This one command:

1. runs Pure Python, Pandas, and Polars on Facebook Ads;
2. verifies agreement;
3. repeats the process for Facebook Posts;
4. repeats the process for Twitter/X Posts;
5. generates the cross-dataset comparison.

## Run scripts individually

Example for Facebook Ads:

```bash
python3 pure_python_stats.py data/facebook_political_ads.csv --output-dir outputs/facebook_ads
python3 pandas_stats.py data/facebook_political_ads.csv --output-dir outputs/facebook_ads
python3 polars_stats.py data/facebook_political_ads.csv --output-dir outputs/facebook_ads
python3 verify_results.py outputs/facebook_ads
```

The same scripts accept the Facebook Posts or Twitter/X CSV path without modification.

## Cross-dataset analysis

The comparison can also be run directly:

```bash
python3 cross_dataset.py \
  data/facebook_political_ads.csv \
  data/facebook_posts.csv \
  data/twitter_posts.csv \
  --labels "Facebook Ads" "Facebook Posts" "Twitter/X Posts" \
  --output-dir outputs/cross_dataset
```

## Main findings

### Facebook Ads

The ads dataset contains **246,745 rows**. Estimated spend is strongly right-skewed: the mean is about **1,061.29** while the median is only **49**. Estimated impressions show the same pattern, with a mean around **45,601.53** and a median of **3,499**. CTA-related content is common: about **57.3%** of valid records are flagged as CTA messages.

### Facebook Posts

The Facebook Posts dataset contains **19,009 rows**. Total Interactions average approximately **4,190.44**, but the median is only **283**, showing substantial right-skew. `Link` is the most common post type, and the largest account contributes **9,013 records**.

### Twitter/X Posts

The Twitter/X dataset contains **27,304 rows**. Likes average approximately **6,913.69** versus a median of **1,406**, and views average approximately **507,084.73** versus a median of **70,942**. Twitter Web App is the most common source.

### Cross-platform comparison

The strongest contrast is CTA behavior. Approximately **57.3%** of Ads are classified as CTA messages, compared with **13.3%** of Facebook Posts and **11.0%** of Twitter/X Posts. Fundraising CTA classification is **22.8%** in Ads but only **1.8%** in Facebook Posts and **0.8%** on Twitter/X.

Issue-message classification moves in the opposite direction: about **38.2%** for Ads, **46.0%** for Facebook Posts, and **50.8%** for Twitter/X. Advocacy-message classification is highly consistent across all three, at roughly **55–56%**.

See `FINDINGS.md` and `CROSS_DATASET.md` for the full narrative.

## Data-quality observations

The datasets are not perfectly schema-aligned. Facebook Posts contains a field named `illuminating_scored_messageelection_integrity_Truth_illuminating`, which appears to be a concatenated/malformed column name. The system does not silently rename it; exact schema comparison therefore treats it as a Facebook-Posts-specific field.

Some Twitter/X classification fields contain fewer valid observations than the total row count. Cross-dataset comparisons use the valid count for each field rather than assuming complete coverage.

## Repository map

- `pure_python_stats.py` — generalized standard-library analysis
- `pandas_stats.py` — equivalent Pandas analysis
- `polars_stats.py` — equivalent Polars analysis
- `verify_results.py` — verifies agreement across approaches
- `cross_dataset.py` — compares schemas and shared-column statistics
- `run_task3.py` — one-command orchestration
- `common_utils.py` — shared parsing/type/grouping rules
- `FINDINGS.md` — findings for each dataset
- `CROSS_DATASET.md` — cross-platform comparison
- `REFLECTION.md` — design and tooling reflection
- `AI_CODE_REVIEW.md` — evaluation of AI-generated starter code
- `requirements.txt` — dependencies
- `.gitignore` — excludes datasets, outputs, and local environments

## Reproducibility

A researcher can clone the repository, download the three datasets separately, place them in `data/`, install dependencies, and run `run_task3.py` without modifying the analysis scripts. The local run used for this submission produced **PASS** for the Pure Python/Pandas/Polars agreement check on all three datasets.
