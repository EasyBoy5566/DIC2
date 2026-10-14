# DIC2 — Multiple Linear Regression Explorer

Live site: https://easyboy5566.github.io/DIC2/

## Assignment checklist

- Two completed problems selectable from a dropdown.
- **Submission topic / default: Problem 1 — 50 Startups profit prediction.**
- Problem 2 — Auto MPG prediction directly reuses the documented [CRISP-DM regression workflow](workflows/regression.md).
- Load public CSV URLs or upload a local CSV; choose a numeric target and predictors.
- Compare Best Subset, Forward Selection, RFE, Lasso ranking and Elastic Net ranking.
- View selected features, CV RMSE, test RMSE, R² and interactive charts.

## Try it

1. Choose a problem and click **Load Selected Problem Example**.
2. Click **Run Analysis**. Problem 1 uses 50 rows and five encoded inputs; Problem 2 uses 392 complete rows and three inputs.
3. For other datasets, enter a CSV URL and click **Load Dataset from URL**, or upload a CSV, then select target and predictors.

Public URLs must allow CORS. Both bundled examples work without external downloads. JavaScript libraries are vendored with their license headers retained.

## Methodology and limits

Missing selected values are excluded. Categorical mappings use training rows; unseen test categories use reference coding. Seeded train/test split defaults to seed 42 and 20% test data. The summary is selected by training CV RMSE, not test performance.

Lasso and Elastic Net rank regularized coefficients and refit subsets with OLS. CV is a model-selection score, not an unbiased nested-CV estimate. Exhaustive search supports at most 10 encoded inputs and explicitly rejects larger selections. User datasets must satisfy the numeric-target and size constraints.

This implements the stated assignment requirements, not every extra feature in the screenshot (such as coefficient significance tests and a live prediction panel).

## Validation

Run Python Playwright: python tests/browser_check.py (requires installed Chromium).

Checks both topics, five-method result counts, finite metrics, CSV URL loading, local CSV upload, malformed CSV rejection, an exact linear dataset, switching topics, browser errors and mobile overflow.

Observed default test RMSE: startup 9304.12; Auto MPG 4.74. These are computed results, not copied screenshot values.

## Deployment

.github/workflows/pages.yml publishes index.html, data/, vendor/ and workflows/ on pushes to main. GitHub Pages uses GitHub Actions.

Sources and full methodology: [regression workflow](workflows/regression.md).
