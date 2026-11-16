# AI-Generated Starter Code Review

Coding assistants can quickly generate starter versions of all three Task 3 approaches, but default suggestions usually optimize for brevity rather than cross-dataset correctness.

Common useful suggestions include `csv.DictReader` for standard-library parsing, `DataFrame.describe()`/`groupby()` in Pandas, and expression/group operations in Polars. These are appropriate starting points.

The main weaknesses are hidden assumptions. AI-generated examples often allow Pandas or Polars to infer types independently, which can produce different results when one CSV has mixed numeric/text values. They also tend to hardcode grouping columns after seeing one schema. A third issue is that identifier fields containing digits may be treated as numeric even though calculating their mean has no analytical meaning.

For this repository, AI assistance was treated as scaffolding. The important design choices were made explicit: the same missing-value markers and numeric parsing rules are applied across implementations, file paths are supplied at runtime, grouping can be auto-detected or overridden, and an independent verification script checks whether the three summaries agree.

The lesson is that coding AI can accelerate implementation, but agreement tests and human schema inspection are necessary before its output should be trusted for research analysis.
