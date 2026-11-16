# Findings

## Facebook Ads

The Facebook Ads dataset contains **246,745 rows and 41 columns**. It has **4,475 unique `page_id` values** and **246,745 unique `ad_id` values**, so every ad identifier is unique in this file. The largest page group contributes **55,503 records**, followed by page groups with **23,988** and **14,822** records.

The byline distribution is also concentrated. `HARRIS FOR PRESIDENT` is the most frequent byline with **49,788 records**. The most common publisher-platform combination is `['facebook', 'instagram']`, appearing in **214,434 records**.

Several advertising measures are strongly right-skewed. Estimated spend has a mean of approximately **1,061.29** but a median of only **49**. Estimated impressions have a mean of approximately **45,601.53** but a median of **3,499**. Estimated audience size averages approximately **556,462.86**, with a median of **300,000**. These gaps show that a relatively small number of high-spend or high-reach ads pull the means upward.

The ad content classifications also show that calls to action are common in paid advertising. `cta_msg_type_illuminating` has a mean of **0.5728**, which corresponds to about **57.3%** of records being flagged for a CTA. The fundraising CTA flag averages **0.2285** (about **22.8%**) and the voting CTA flag averages **0.1438** (about **14.4%**).

## Facebook Posts

The Facebook Posts dataset contains **19,009 rows and 56 columns**. It includes **21 unique `Facebook_Id` values** and **19,009 unique `post_id` values`, so the post identifier is unique for each row.

The largest Facebook account contributes **9,013 records**, which is nearly half of the dataset. Among rows with a page-category value, `PERSON` is the most frequent category with **9,453 records**. `Link` is the most common post type with **7,404 records**, followed by Photo and Native Video.

Facebook engagement is highly right-skewed. Total Interactions average approximately **4,190.44**, while the median is only **283**. Likes average **2,377.70** with a median of **139**; comments average **901.58** with a median of **48**; and shares average **320.54** with a median of **21**. A small number of very high-engagement posts therefore have a large effect on the means.

A data-quality issue is visible in this file: the column name `illuminating_scored_messageelection_integrity_Truth_illuminating` appears to combine two expected fields. I did not silently rename or split it because Task 3 is meant to reveal schema differences rather than hide them. This malformed field is therefore not treated as an exact common column in the cross-dataset comparison.

## Twitter/X Posts

The Twitter/X dataset contains **27,304 rows and 47 columns**. The `id` field is unique across all **27,304 records**, and the `url` field is also unique for every row.

The most common source is **Twitter Web App** with **14,930 records**, followed by Twitter for iPhone with **8,494** and Sprout Social with **2,933**. English dominates the language field, appearing in **27,281 of 27,304 records**. October 2024 is the most common month in the `month_year` field with **3,586 records**.

Engagement metrics are again strongly right-skewed. Likes average approximately **6,913.69**, compared with a median of **1,406**. Retweets average **1,322.06**, compared with a median of **333**. Replies average **1,063.79**, compared with a median of **131**. Views average approximately **507,084.73**, but the median is only **70,942**. This indicates that relatively few highly visible posts contribute disproportionately to the average engagement levels.

## Overall finding

Task 3 shows why a reusable system is valuable. The three datasets differ substantially in size, schema, identifier names, platform-specific metrics, and missingness, yet the same generalized Pure Python, Pandas, and Polars scripts processed all three without rewriting the core analysis. The verification step returned **PASS for all three datasets**, confirming that the independent implementations agreed on their core dataset-level statistics.
