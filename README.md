# DIC2 — Multiple Linear Regression Explorer

This project satisfies the assignment requirements:

- Two problems available from a dropdown menu.
- Problem 1: 50 Startups profit prediction.
- Problem 2: Generic Multiple Linear Regression skill/workflow for arbitrary CSV datasets.
- Dataset can be loaded from a public CSV URL or uploaded locally.
- CRISP-DM workflow is shown in the interface.
- Five feature-selection methods are compared:
  - Best Subset
  - Forward Selection
  - Backward Elimination
  - Recursive Feature Elimination (RFE)
  - Lasso (L1)
- RMSE and R-squared are reported for each number of selected features.
- Interactive charts are produced with Chart.js.

## Default Dataset

https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv

For the 50 Startups dataset, `State` is encoded with drop-first dummy coding.  
Original predictors = 4 (`R&D Spend`, `Administration`, `Marketing Spend`, `State`)  
Encoded model inputs = 5 (3 numeric + 2 state dummy variables).

## GitHub Pages

This project is static. Put `index.html` in the repository root and enable:

Settings → Pages → Deploy from a branch → `main` → `/ (root)`

Or use the included GitHub Actions workflow.
