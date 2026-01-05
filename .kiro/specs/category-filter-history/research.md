# Research & Design Decisions

## Summary
- **Feature**: `category-filter-history`
- **Discovery Scope**: Extension (既存コードベースへの機能追加)
- **Key Findings**:
  - Hugging Face APIレスポンスにarXiv論文IDが含まれる
  - arXiv APIで論文のカテゴリ情報を取得可能
  - history.jsonでシンプルな永続化が実現可能

## Research Log

### arXiv Category API
- **Context**: 論文のカテゴリ情報取得方法の調査
- **Sources Consulted**: arXiv API documentation
- **Findings**:
  - arXiv APIエンドポイント: `http://export.arxiv.org/api/query?id_list=PAPER_ID`
  - レスポンスにcategory情報が含まれる（例: `cs.AI`, `cs.CL`）
  - バッチリクエスト可能（カンマ区切りで複数ID）
- **Implications**: 各論文に対してarXiv APIを呼び出す必要あり（rate limit注意）

### Agent関連カテゴリ
- **Context**: デフォルトフィルタ対象の特定
- **Findings**:
  - `cs.AI` - Artificial Intelligence（メイン）
  - `cs.MA` - Multi-Agent Systems
  - `cs.CL` - Computation and Language（LLM Agent系）
  - `cs.LG` - Machine Learning（一般的だが含めると広すぎる可能性）

## Design Decisions

### Decision: arXiv API経由でカテゴリ取得
- **Context**: 論文カテゴリの取得方法
- **Selected Approach**: arXiv APIを使用してカテゴリ情報を取得
- **Rationale**: 正確なカテゴリ情報が取得可能
- **Trade-offs**: API呼び出し回数増加、rate limitへの配慮が必要

### Decision: history.jsonによる履歴管理
- **Context**: 送信済み論文の追跡方法
- **Selected Approach**: ローカルJSONファイルで管理、GitHub Actionsで自動コミット
- **Rationale**: シンプル、外部依存なし、バージョン管理可能

## Risks & Mitigations
- arXiv API rate limit — バッチリクエスト使用、適度な待機時間
- history.json競合 — GitHub Actions単一実行なので問題なし
- カテゴリ未取得 — フォールバックとして全論文を許可
