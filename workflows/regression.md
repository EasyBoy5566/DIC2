# Reusable regression workflow — CRISP-DM

## 1. Business understanding
- Problem 1: predict startup Profit from R&D Spend, Administration, Marketing Spend and State.
- Problem 2: predict vehicle mpg from displacement, horsepower and weight using the same implementation.
- Submission topic: Problem 1 (default). Both problems are available in the dropdown.

## 2. Data understanding
Load the selected example, a public CSV URL, or a local CSV file. Inspect row/column counts, select a numeric target and predictors. Public URLs must permit browser CORS access; local upload is the fallback.

## 3. Data preparation
Reject malformed CSV; exclude rows with missing selected values or nonnumeric targets. Require at least 10 complete rows. Seeded train/test split; learn drop-first categorical encoding from training rows. Unseen test categories use the reference coding. Reject more than 10 encoded features explicitly because exhaustive subset search is exponential.

## 4. Modeling
Apply the same `runAnalysis()` implementation to both problems. Compare Best Subset, Forward Selection, RFE, Lasso ranking and Elastic Net ranking across feature counts. The latter two tune regularization on training folds, rank standardized coefficients, and refit selected features with OLS. They are feature-selection workflows, not final penalized predictions.

## 5. Evaluation
Select the displayed model by training CV RMSE. Report held-out test RMSE and R² and chart all methods. Training CV is used for selection, not claimed as unbiased nested-CV performance. Repeatedly adjusting choices after viewing test results can still overfit the test set. Results need not reproduce the reference screenshot's numbers because splits and selection implementations differ.

## 6. Deployment
Publish the static application with `.github/workflows/pages.yml`. No server or uploaded-data storage is required. The included example datasets make both topics reproducible without remote dataset availability.

## Sources
- Startup data: https://github.com/Avik-Jain/100-Days-Of-ML-Code/blob/master/datasets/50_Startups.csv
- Auto MPG data: https://github.com/mwaskom/seaborn-data/blob/master/mpg.csv (Auto MPG example dataset).
- Assignment reference: https://huanchen1107.github.io/AIoT-DIC2-MultipleLR/
