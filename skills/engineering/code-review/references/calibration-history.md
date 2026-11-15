# Calibration history

One row per month per calibration run. [Calibration](calibration.md) adds rows. Compare miss rates
only between rows with the same method. The baseline rows came from a manual classification before
the script existed, so the first script run sets the comparable baseline.

| Month   | Calibrated | Method                                         | Pull requests | Comments | Misses | Miss rate |
| ------- | ---------- | ---------------------------------------------- | ------------- | -------- | ------ | --------- |
| 2026-09 | 19/10/2026 | Baseline: PRs created, all repositories        | 6             | 6        | 2      | 0.33      |
| 2026-10 | 19/10/2026 | Baseline: PRs created, all repositories        | 110           | 206      | 150    | 1.36      |
| 2026-10 | 19/10/2026 | Script: merged PRs, bot-commented repositories | 33            | 56       | 50     | 1.52      |
| 2026-10 | 15/11/2026 | Script: merged PRs, bot-commented repositories | 12            | 3        | 3      | 0.25      |
| 2026-11 | 15/11/2026 | Script: merged PRs, bot-commented repositories | 75            | 23       | 14     | 0.19      |
