# Requirements Document

## Introduction
本ドキュメントは、Hugging Face Daily Papersから人気論文を取得してSlackに投稿するシステムの要件を定義します。

## Requirements

### Requirement 1: 論文データ取得機能
**Objective:** As a 研究者/エンジニア, I want Hugging Face Daily Papersから人気論文を自動取得したい, so that 最新のAI/ML研究動向を効率的に把握できる

#### Acceptance Criteria
1. When the system executes, the Paper Notificator shall fetch papers from Hugging Face Daily Papers (https://huggingface.co/papers)
2. When fetching papers, the Paper Notificator shall retrieve title, link, upvote count, and abstract for each paper
3. The Paper Notificator shall filter papers based on upvote count from the past week
4. The Paper Notificator shall select the top 5 papers with the highest upvote count
5. If the Hugging Face website returns an error or is unavailable, the Paper Notificator shall log the error and exit gracefully

### Requirement 2: Slack通知機能
**Objective:** As a 研究者/エンジニア, I want 取得した人気論文をSlackに自動投稿したい, so that チームメンバーと最新の論文情報を共有できる

#### Acceptance Criteria
1. When papers are fetched successfully, the Paper Notificator shall format a digest message for Slack
2. When digest is formatted, the Paper Notificator shall post the message to Slack via Webhook
3. The Paper Notificator shall include paper title, link, upvote count, and abstract in the digest
4. If Slack Webhook returns an error, the Paper Notificator shall log the error and report failure

### Requirement 3: 設定管理
**Objective:** As a 開発者, I want 環境変数で設定を管理したい, so that セキュアかつ柔軟にシステムを運用できる

#### Acceptance Criteria
1. The Paper Notificator shall read `SLACK_WEBHOOK_URL` from environment variables
2. If required environment variables are missing, the Paper Notificator shall exit with an error message

### Requirement 4: GitHub Actions実行
**Objective:** As a 開発者, I want GitHub Actionsで定期実行したい, so that サーバー管理なしで自動化できる

#### Acceptance Criteria
1. The Paper Notificator shall be executable via GitHub Actions workflow
2. The GitHub Actions workflow shall trigger daily at JST 10:00 (UTC 01:00)
3. The workflow shall use .venv virtual environment with requirements.txt for dependency management

### Requirement 5: ドライラン機能
**Objective:** As a 開発者, I want 実際にSlackに投稿せずに動作確認したい, so that テストやデバッグが容易になる

#### Acceptance Criteria
1. When `--dry-run` flag is provided, the Paper Notificator shall print the digest to stdout instead of posting to Slack
2. While in dry-run mode, the Paper Notificator shall skip Slack API calls
