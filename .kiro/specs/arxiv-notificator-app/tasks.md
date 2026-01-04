# Implementation Plan

## Task 1: プロジェクト基盤セットアップ
- [x] 1.1 依存関係とプロジェクト構造の整備
  - requirements.txtにrequests, python-dotenvを定義
  - 既存の不要ファイル（旧arxiv関連）を整理
  - _Requirements: 4.3_

## Task 2: Hugging Face論文取得クライアント
- [x] 2.1 (P) Hugging Face APIからの論文データ取得機能
  - Daily Papers APIへのリクエスト送信
  - JSONレスポンスからタイトル、リンク、Upvote数、概要を抽出
  - 過去7日間の論文をフィルタリング
  - Upvote数でソートしてTop N件を返却
  - API通信エラー時の例外処理
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

## Task 3: Slack通知クライアント
- [x] 3.1 (P) Slack Webhookへのメッセージ投稿機能
  - Webhook URLを使用したPOSTリクエスト送信
  - 通信エラー時の例外処理とログ出力
  - _Requirements: 2.2, 2.4_

- [x] 3.2 (P) 論文ダイジェストメッセージのフォーマット
  - 論文リストから見やすいSlackメッセージを生成
  - タイトル、リンク、Upvote数、概要を含める
  - _Requirements: 2.1, 2.3_

## Task 4: メインオーケストレーション
- [x] 4.1 全体フローの制御とCLIエントリーポイント
  - 環境変数（SLACK_WEBHOOK_URL）の読み込みとバリデーション
  - HuggingFaceClientで論文取得
  - SlackClientでダイジェスト作成と投稿
  - --dry-runフラグ処理（標準出力への出力）
  - _Requirements: 3.1, 3.2, 5.1, 5.2_

## Task 5: GitHub Actions定期実行
- [x] 5.1 GitHub Actionsワークフローの作成
  - daily.ymlワークフローファイル作成
  - JST 10:00（UTC 01:00）のcronスケジュール設定
  - Python環境セットアップと依存インストール
  - Secrets経由でのWebhook URL注入
  - _Requirements: 4.1, 4.2, 4.3_

## Task 6: テストとバリデーション
- [x] 6.1 HuggingFaceClientのユニットテスト
  - APIレスポンスのモックによる取得ロジック検証
  - フィルタリングとソートのテスト
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 6.2 SlackClientのユニットテスト
  - ダイジェスト生成ロジックの検証
  - _Requirements: 2.1, 2.3_

- [x]* 6.3 ドライラン統合テスト
  - main.py --dry-runの標準出力確認
  - _Requirements: 5.1, 5.2_
