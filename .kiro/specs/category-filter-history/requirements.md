# Requirements Document - Category Filtering and History Tracking

## Introduction
本ドキュメントは、arXivカテゴリによる論文フィルタリング機能と、過去出力論文の重複排除機能の要件を定義します。

## Requirements

### Requirement 1: arXivカテゴリフィルタリング機能
**Objective:** As a researcher/engineer, I want to filter papers by arXiv category, so that I can focus on specific research areas (e.g., Agent-related papers).

#### Acceptance Criteria
1. When fetching papers, the Paper Notificator shall extract arXiv ID from each paper's link
2. The Paper Notificator shall fetch arXiv category information for each paper using the arXiv API
3. When `--categories` flag is provided, the Paper Notificator shall filter papers matching the specified categories
4. The default categories shall be `cs.AI, cs.MA, cs.CL` (Agent-related)
5. If a paper matches any of the specified categories, the Paper Notificator shall include it in the results

### Requirement 2: 重複排除機能
**Objective:** As a user, I want to avoid seeing duplicate papers, so that I only receive new papers each week.

#### Acceptance Criteria
1. The Paper Notificator shall maintain a `history.json` file to track sent paper IDs
2. When preparing papers for output, the Paper Notificator shall exclude papers already in `history.json`
3. After successfully posting to Slack, the Paper Notificator shall append new paper IDs to `history.json`
4. The Paper Notificator shall remove entries older than 30 days from `history.json` to prevent bloat
5. If `history.json` does not exist, the Paper Notificator shall create it with an empty list

### Requirement 3: GitHub Actions自動履歴更新
**Objective:** As a developer, I want GitHub Actions to automatically commit history.json updates, so that the history persists across runs.

#### Acceptance Criteria
1. The GitHub Actions workflow shall commit `history.json` changes after each successful run
2. The commit message shall include `[skip ci]` to prevent infinite loop
3. The workflow shall use `github-actions[bot]` as the commit author
