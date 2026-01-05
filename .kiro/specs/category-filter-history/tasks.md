# Implementation Plan - Category Filtering and History Tracking

## Task 1: HistoryManager 実装
- [x] 1.1 (P) 履歴管理クラスの実装
  - history.json の読み込み・書き込み
  - 送信済み論文IDのチェック機能
  - 新規論文IDの追加機能
  - 30日以上古いエントリの自動削除
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

## Task 2: ArxivCategoryClient 実装
- [x] 2.1 (P) arXivカテゴリ取得クライアントの実装
  - arXiv APIへのリクエスト送信
  - XMLレスポンスからカテゴリ情報を抽出
  - バッチリクエスト対応（複数ID同時取得）
  - エラー時のフォールバック処理
  - _Requirements: 1.1, 1.2_

## Task 3: HuggingFaceClient 拡張
- [x] 3.1 arXiv ID抽出メソッドの追加
  - 論文リンクからarXiv IDを正規表現で抽出
  - _Requirements: 1.1_

## Task 4: main.py オーケストレーション更新
- [x] 4.1 新機能の統合
  - `--categories` CLI引数の追加（デフォルト: cs.AI,cs.MA,cs.CL）
  - カテゴリフィルタリングロジックの統合
  - 重複排除ロジックの統合
  - 実行後の履歴更新処理
  - _Requirements: 1.3, 1.4, 1.5, 2.2, 2.3_

## Task 5: GitHub Actions 更新
- [x] 5.1 history.json 自動コミットステップ追加
  - git config 設定
  - history.json のコミットとプッシュ
  - [skip ci] による無限ループ防止
  - _Requirements: 3.1, 3.2, 3.3_

## Task 6: テスト
- [x] 6.1 (P) HistoryManager ユニットテスト
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 6.2 (P) ArxivCategoryClient ユニットテスト
  - _Requirements: 1.1, 1.2_
