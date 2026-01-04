# Research & Design Decisions

## Summary
- **Feature**: `arxiv-notificator-app` (Hugging Face Daily Papers版)
- **Discovery Scope**: New Feature (データソース変更)
- **Key Findings**:
  - Hugging Face非公式API `https://huggingface.co/api/daily_papers` が利用可能
  - BeautifulSoupによるスクレイピング不要、JSON APIで取得可能
  - GitHub Actionsでcron実行可能（JST 10:00 = UTC 01:00）

## Research Log

### Hugging Face Daily Papers API
- **Context**: 論文データ取得方法の調査
- **Sources Consulted**: Web search, community projects (AK391/daily-papers-hn)
- **Findings**:
  - 非公式API: `https://huggingface.co/api/daily_papers`
  - JSON形式でレスポンス、最大100件取得可能
  - 各論文にupvote数、abstract、arXivリンクが含まれる
  - Rate limit情報は不明だが、公開エンドポイント
- **Implications**: requestsライブラリのみで実装可能、BeautifulSoup不要

### GitHub Actions Scheduling
- **Context**: 定期実行環境の設計
- **Sources Consulted**: GitHub Actions documentation
- **Findings**:
  - cron構文: `0 1 * * *` (UTC 01:00 = JST 10:00)
  - 環境変数はSecretsで管理
  - Python setup action と pip install で依存管理
- **Implications**: requirements.txtで依存宣言、workflowで自動インストール

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| API Client | 非公式APIを使用 | シンプル、安定 | APIが変更される可能性 | 推奨 |
| Web Scraping | BeautifulSoupで解析 | 公式ページ準拠 | 構造変更に弱い | 代替案 |

## Design Decisions

### Decision: 非公式API利用
- **Context**: Hugging Face Daily Papersからのデータ取得方法
- **Alternatives Considered**:
  1. BeautifulSoupによるWebスクレイピング
  2. 非公式API (`/api/daily_papers`) の利用
- **Selected Approach**: 非公式APIを使用
- **Rationale**: JSON形式で取得でき、パース処理がシンプル
- **Trade-offs**: APIが変更された場合は対応が必要
- **Follow-up**: APIレスポンス構造の変更を監視

### Decision: requirements.txt管理
- **Context**: ユーザー指定の依存管理方式
- **Selected Approach**: .venv + requirements.txt
- **Rationale**: GitHub Actions標準的なPythonセットアップと整合

## Risks & Mitigations
- API変更 — レスポンス構造の検証ロジック追加
- Rate limit — 1日1回実行で問題なし
- Secrets漏洩 — GitHub Secretsで安全に管理

## References
- [Hugging Face Daily Papers](https://huggingface.co/papers) — 公式ページ
- [AK391/daily-papers-hn](https://github.com/AK391/daily-papers-hn) — API利用の参考実装
- [GitHub Actions cron syntax](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
