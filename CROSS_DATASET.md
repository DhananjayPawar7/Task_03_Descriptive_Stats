# Cross-Dataset Comparison

## Dataset shapes

| Dataset | Rows | Columns |
|---|---:|---:|
| Facebook Ads | 246,745 | 41 |
| Facebook Posts | 19,009 | 56 |
| Twitter/X Posts | 27,304 | 47 |

The three datasets have very different schemas and scales. Facebook Ads is by far the largest by row count, Facebook Posts has the widest schema, and Twitter/X falls between them on both dimensions.

## Shared schema

The automated comparison found **27 exact column names common to all three datasets**. These common fields are primarily binary classification variables describing message type, CTA subtype, issue topic, incivility, scams, fraud, and related content characteristics.

The shared fields are:

`advocacy_msg_type_illuminating`, `attack_msg_type_illuminating`, `covid_topic_illuminating`, `cta_msg_type_illuminating`, `economy_topic_illuminating`, `education_topic_illuminating`, `engagement_cta_subtype_illuminating`, `environment_topic_illuminating`, `foreign_policy_topic_illuminating`, `fraud_illuminating`, `freefair_illuminating`, `fundraising_cta_subtype_illuminating`, `governance_topic_illuminating`, `health_topic_illuminating`, `image_msg_type_illuminating`, `immigration_topic_illuminating`, `incivility_illuminating`, `issue_msg_type_illuminating`, `lgbtq_issues_topic_illuminating`, `military_topic_illuminating`, `race_and_ethnicity_topic_illuminating`, `safety_topic_illuminating`, `scam_illuminating`, `social_and_cultural_topic_illuminating`, `technology_and_privacy_topic_illuminating`, `voting_cta_subtype_illuminating`, and `womens_issue_topic_illuminating`.

## Platform-specific schema

Facebook Ads contains advertising-specific fields such as `estimated_spend`, `estimated_impressions`, `estimated_audience_size`, `currency`, `delivery_by_region`, `page_id`, and `ad_id`.

Facebook Posts contains platform engagement and post-format fields such as `Likes`, `Comments`, `Shares`, `Total Interactions`, reaction counts, `Type`, `Post Views`, and `post_id`.

Twitter/X contains fields such as `retweetCount`, `replyCount`, `likeCount`, `quoteCount`, `viewCount`, `bookmarkCount`, `source`, `lang`, `isReply`, `isQuote`, and `id`.

This confirms that direct comparisons should focus on the **shared classification variables**, not on unrelated platform-specific metrics such as ad spend versus tweet likes.

## Notable shared-column differences

Because most shared classification fields are coded 0/1, the mean can be interpreted as the proportion of valid records flagged for that characteristic.

| Shared feature | Facebook Ads | Facebook Posts | Twitter/X Posts |
|---|---:|---:|---:|
| Advocacy message | 54.9% | 54.9% | 56.4% |
| CTA message | 57.3% | 13.3% | 11.0% |
| Fundraising CTA | 22.8% | 1.8% | 0.8% |
| Voting CTA | 14.4% | 2.3% | 1.7% |
| Issue message | 38.2% | 46.0% | 50.8% |
| Attack message | 27.2% | 21.7% | 30.8% |
| Economy topic | 12.2% | 9.0% | 16.0% |
| Health topic | 10.9% | 4.9% | 5.6% |
| Incivility | 18.8% | 12.8% | 17.9% |
| Scam flag | 7.2% | 2.0% | 1.2% |
| Women's-issue topic | 8.1% | 2.5% | 2.3% |

### 1. Advocacy is remarkably consistent

The advocacy-message flag is nearly identical across the three sources: about **54.9%** for Ads, **54.9%** for Facebook Posts, and **56.4%** for Twitter/X. This is one of the strongest examples of the three platforms telling a similar story despite their different formats.

### 2. Paid ads are much more CTA-oriented

The largest cross-platform gap appears in the CTA flag. About **57.3%** of Facebook Ads are classified as CTA messages, compared with only **13.3%** of Facebook Posts and **11.0%** of Twitter/X Posts.

The pattern is even stronger for fundraising: approximately **22.8%** of ads are flagged as fundraising CTAs, compared with **1.8%** of Facebook Posts and **0.8%** of Twitter/X Posts. Voting CTAs show the same direction: **14.4%** in Ads versus **2.3%** in Facebook Posts and **1.7%** on Twitter/X.

This suggests that the paid-ad dataset is much more action-oriented than the organic social-post datasets.

### 3. Twitter/X contains more issue and attack classifications

The issue-message flag rises from about **38.2%** in Ads to **46.0%** in Facebook Posts and **50.8%** on Twitter/X. The attack-message flag is also highest on Twitter/X at approximately **30.8%**, compared with **27.2%** for Ads and **21.7%** for Facebook Posts.

Economy-topic classification is also highest on Twitter/X at about **16.0%**, compared with **12.2%** for Ads and **9.0%** for Facebook Posts.

### 4. Some themes are more prominent in ads

Health appears in about **10.9%** of Ads, compared with **4.9%** of Facebook Posts and **5.6%** of Twitter/X Posts. The scam flag appears in about **7.2%** of Ads, versus **2.0%** and **1.2%** in the two organic-post datasets. Women's-issue classification also appears more often in Ads (**8.1%**) than Facebook Posts (**2.5%**) or Twitter/X (**2.3%**).

## Missingness and schema caution

Not every shared field has the same valid count in every dataset. Several Twitter/X classification fields have **26,034 valid values** rather than the full 27,304 rows, so comparisons are based on available values for each field rather than assuming complete coverage.

The Facebook Posts schema also contains a malformed/concatenated field name, `illuminating_scored_messageelection_integrity_Truth_illuminating`. Because the cross-dataset tool uses exact field names, that field is correctly treated as platform-specific instead of being silently forced into an assumed match.

## Conclusion

The cross-dataset comparison shows both consistency and platform-specific behavior. Advocacy is common at almost the same rate across all three datasets, but paid advertising is substantially more CTA- and fundraising-oriented, while Twitter/X has higher shares of issue and attack classifications. These differences demonstrate why Task 3 needed a schema-aware system: comparable fields can be analyzed together, while platform-specific measures must remain separate rather than being forced into misleading comparisons.
