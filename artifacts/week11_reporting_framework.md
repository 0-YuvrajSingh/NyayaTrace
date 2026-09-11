# Week 11 Final Temporal Retrieval Reporting Framework

## Temporal eligibility and integrity counts

| Population | Eligible | Later-year ineligible | Same-year ambiguous | Total |
|---|---:|---:|---:|---:|
| Preserved post-ranking baseline candidates | 764 | 1712 | 267 | 2743 |
| Final pre-ranking candidates | 3000 | 0 | 0 | 3000 |
| Final displayed citations | 150 | 0 | 0 | 150 |

The final configuration applies the strict earlier-year rule to the candidate relation before BM25 ranking and `LIMIT 100`. Consequently all 3,000 logged candidates and all 150 displayed citations are eligible; same-year and later-year documents cannot consume the returned top-100 depth. The preserved post-ranking baseline contains 764 eligible, 1,712 later-year, and 267 same-year candidates.

The two temporal exposure-rate metrics previously included here were removed on the project mentor's guidance. Direct eligibility and violation counts remain the temporal-integrity report.

## Operational definitions

| Term | Implemented project definition |
|---|---|
| Temporal existence | An eCourts item has a parseable exact `decision_date`; candidates missing this metadata are excluded. ILDC query dates are available only at year granularity. |
| Temporal effectiveness | The strict filter constrains the BM25 candidate relation before ranking, preventing later/same-year material from consuming top-k capacity; all 3,000 final candidates are eligible. |
| Temporal applicability | For an ILDC query with year Y, an eCourts precedent is eligible only when `precedent_decision_year < Y`. Same-year and later-year items are excluded before BM25 ranking; missing dates are excluded. |
| Provenance validity | Each displayed evidence item must reproduce a corpus chunk's stable source ID, citation, decision date, court, PDF/page/character locator, exact passage text, and retrieval-run membership. |
| Authority consistency | A final displayed authority matches the independently verified answer-key authority by stable source ID, normalized citation, or normalized title plus exact decision date. |
| Displayed temporal integrity | Every displayed citation must be strictly earlier than the query year; all 150 final displayed citations satisfy this rule. |
