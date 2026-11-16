# Reflection

## Moving from scripts to a reusable system

The most important change from Task 2 was removing assumptions that were specific to one CSV. Task 2 could safely assume the presence of fields such as `page_id` and `ad_id`. Task 3 required the same scripts to process Facebook Ads, Facebook Posts, and Twitter/X Posts, whose identifiers, engagement fields, dates, and schemas differ substantially.

I generalized the workflow by passing the file path at runtime, dynamically detecting column types, normalizing missing values, and choosing grouping keys only when appropriate fields exist. This allowed the same Pure Python, Pandas, and Polars implementations to run on all three datasets without editing the core analysis logic.

## What broke from the Task 2 design?

The biggest assumption that failed was fixed column naming. Ads use `page_id` and `ad_id`; Facebook Posts use fields such as `Facebook_Id` and `post_id`; Twitter/X uses `id` and different platform-specific fields. The datasets also differed in width and data quality: Ads had 41 columns, Facebook Posts had 56, and Twitter/X had 47.

A particularly useful example was the Facebook Posts field `illuminating_scored_messageelection_integrity_Truth_illuminating`, which appears to combine two expected column names. A hardcoded cross-platform script could easily mis-handle that issue. The generalized system instead compares exact available schemas and reports the mismatch.

## Cross-platform findings

The automated comparison found **27 exact common columns** across all three files. Most of these are binary content-classification variables, making them more appropriate for direct comparison than platform-specific engagement fields.

One of the clearest findings was the difference in CTA behavior. The CTA-message flag averaged about **57.3%** in Facebook Ads, compared with **13.3%** in Facebook Posts and **11.0%** on Twitter/X. Fundraising CTAs showed an even wider gap: **22.8%** in Ads, **1.8%** in Facebook Posts, and **0.8%** on Twitter/X. This supports the interpretation that paid advertising is much more directly action-oriented.

By contrast, the issue-message flag was highest on Twitter/X (**50.8%**), followed by Facebook Posts (**46.0%**) and Ads (**38.2%**). Attack-message classification was also highest on Twitter/X (**30.8%**). Advocacy itself was unusually consistent, appearing in roughly **55–56%** of valid records across all three sources.

These findings show that the three datasets tell both similar and different stories depending on the variable. The shared content-classification fields provide meaningful cross-platform comparisons, while platform-specific measures such as ad spend, Facebook reactions, and Twitter views should not be treated as if they were directly equivalent.

## Pure Python vs. Pandas vs. Polars after repeated use

Pure Python remains the best approach for understanding what grouping, type parsing, null handling, and aggregation actually require. It exposes each operation explicitly, but this also makes it the most verbose implementation.

Pandas remains the most convenient for exploratory analysis. `describe`, `groupby`, missing-value operations, and frequency analysis require relatively little code. The tradeoff is that Pandas can make type assumptions feel invisible unless the analyst inspects them carefully.

Polars is stricter and more expression-oriented. That required more deliberate coding initially, but after repeated use its explicit schema behavior became an advantage. For larger or repeated analytical pipelines, that predictability is useful.

For a junior analyst, I would teach enough Pure Python to understand the mechanics, then use Pandas for day-to-day exploratory work and introduce Polars when performance, strict schemas, or reusable pipelines become more important.

## How reusable is the system beyond election data?

Most of the system would work unchanged on another well-formed CSV. Row and column counts, missing-value analysis, dynamic type detection, numeric descriptive statistics, categorical frequency analysis, and dataset identification are domain-independent.

The part that still requires human judgment is grouped analysis and interpretation. A public-health dataset might need grouping by region or demographic category; a financial dataset might need grouping by account or transaction type. The system can compute statistics generically, but it cannot decide the research question on behalf of the analyst.

## AI coding tools and the generalization problem

AI coding tools were useful for generating starter structures, but generic first-pass code often assumes clean schemas, fixed column names, and straightforward numeric types. Task 3 showed why that is not enough. Real datasets contained platform-specific identifiers, missing values, different schemas, and even a malformed column name.

The most important practice was therefore not accepting generated code at face value, but validating it independently. Running Pure Python, Pandas, and Polars against the same three datasets and then checking agreement made the workflow much more trustworthy. The fact that the verification step returned **PASS for all three datasets** was more important than simply having code that executed.
