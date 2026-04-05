# 📚 arxiv-notificator

[![Daily Paper Notification](https://github.com/sosuke-hiraoka/arxiv-notificator/actions/workflows/daily.yml/badge.svg)](https://github.com/sosuke-hiraoka/arxiv-notificator/actions/workflows/daily.yml)

> Hugging Face Daily Papers から人気の論文を取得し、毎朝 Slack に自動配信するボット。

---

## ✨ 主な機能

| 機能 | 説明 |
|------|------|
| **論文取得** | Hugging Face Daily Papers API からアップボート数の多い論文をランキング形式で取得 |
| **カテゴリフィルタリング** | arXiv カテゴリ（デフォルト: `cs.AI`, `cs.MA`, `cs.CL`）で論文を絞り込み |
| **重複排除** | `history.json` で送信済み論文を管理し、同じ論文の再通知を防止 |
| **Slack 通知** | Incoming Webhook 経由で整形されたダイジェストメッセージを Slack に投稿 |
| **定期自動実行** | GitHub Actions により毎日 JST 10:00 に自動実行 |

---

## 🏗️ アーキテクチャ

```
main.py                     ← エントリーポイント / CLI
├── huggingface_client.py   ← Hugging Face Daily Papers API クライアント
├── arxiv_category_client.py← arXiv API カテゴリ取得クライアント
├── slack_client.py         ← Slack Webhook 通知クライアント
└── history_manager.py      ← 送信履歴管理 (history.json)
```

---

## 🚀 セットアップ

### 前提条件

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) （推奨パッケージマネージャー）

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/sosuke-hiraoka/arxiv-notificator.git
cd arxiv-notificator

# 依存関係をインストール（uv 使用）
uv sync
```

### 環境変数

| 変数名 | 説明 |
|--------|------|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook の URL（[取得方法](https://api.slack.com/messaging/webhooks)） |

- **GitHub Actions**: リポジトリの **Settings → Secrets and variables → Actions** に `SLACK_WEBHOOK_URL` を登録すれば自動で注入されます。
- **ローカル実行**: 環境変数を直接設定するか、`.env` ファイルをプロジェクトルートに作成してください。

```bash
# ローカル実行時のみ（.env は .gitignore 推奨）
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX
```

---

## 📖 使い方

### 基本実行

```bash
# Slack に通知を送信（トップ 5 件）
uv run python main.py

# ドライラン（Slack に送信せず stdout に出力）
uv run python main.py --dry-run
```

### オプション

| フラグ | デフォルト | 説明 |
|--------|-----------|------|
| `--dry-run` | `false` | Slack に送信せず標準出力に表示 |
| `--top-n N` | `5` | 取得する論文数 |
| `--days N` | `7` | 過去 N 日以内の論文を対象 |
| `--categories CATS` | `cs.AI,cs.MA,cs.CL` | フィルタリング対象の arXiv カテゴリ（カンマ区切り） |
| `--no-category-filter` | – | カテゴリフィルタリングを無効化 |
| `--no-history` | – | 重複排除を無効化 |

### 使用例

```bash
# 過去 3 日の NLP 関連論文を 10 件取得
uv run python main.py --top-n 10 --days 3 --categories cs.CL

# カテゴリフィルタなしで全分野を対象
uv run python main.py --no-category-filter

# ドライランで重複排除なし
uv run python main.py --dry-run --no-history
```

---

## ⚙️ GitHub Actions（自動実行）

`.github/workflows/daily.yml` で毎日 **JST 10:00**（UTC 01:00）に自動実行されます。

### 処理の流れ

1. リポジトリをチェックアウト
2. `uv` をセットアップ
3. `main.py` を実行して Slack に通知
4. 更新された `history.json` を自動コミット・プッシュ

### 必要な Secrets

| Secret 名 | 説明 |
|-----------|------|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook の URL |

> リポジトリの **Settings → Secrets and variables → Actions** から設定してください。

手動実行は GitHub の **Actions → Daily Paper Notification → Run workflow** からも可能です。

---

## 🧪 テスト

```bash
uv run pytest
```

テストは `tests/` 以下に配置されています。

| テストファイル | 対象 |
|--------------|------|
| `test_huggingface_client.py` | Hugging Face API クライアント |
| `test_arxiv_category_client.py` | arXiv カテゴリクライアント |
| `test_slack_client.py` | Slack 通知クライアント |
| `test_history_manager.py` | 送信履歴管理 |

---

## 📁 プロジェクト構成

```
arxiv-notificator/
├── .github/workflows/
│   └── daily.yml               # GitHub Actions 定期実行ワークフロー
├── tests/                      # テストスイート
├── main.py                     # エントリーポイント
├── huggingface_client.py       # Hugging Face API クライアント
├── arxiv_category_client.py    # arXiv カテゴリ取得
├── slack_client.py             # Slack Webhook クライアント
├── history_manager.py          # 送信履歴管理
├── history.json                # 送信済み論文の記録
├── pyproject.toml              # プロジェクト設定・依存関係
└── requirements.txt            # 依存パッケージ一覧
```

---

## 🛠️ 技術スタック

- **言語**: Python 3.9+
- **パッケージ管理**: [uv](https://docs.astral.sh/uv/)
- **外部 API**: [Hugging Face Daily Papers](https://huggingface.co/papers), [arXiv API](https://arxiv.org/help/api/)
- **通知**: Slack Incoming Webhook
- **CI/CD**: GitHub Actions
- **テスト**: pytest

---

## 📄 ライセンス

MIT
