# 用語集・リファレンス

> **ドキュメントバージョン**: 1.0
> **最終更新日**: 2025-12-11
> **前提ドキュメント**: [トラブルシューティング](./06_troubleshooting.md)

---

## 目次

1. [プロジェクト固有の用語](#1-プロジェクト固有の用語)
2. [略語一覧](#2-略語一覧)
3. [技術用語](#3-技術用語)
4. [Power Query M言語リファレンス](#4-power-query-m言語リファレンス)
5. [データスキーマ一覧](#5-データスキーマ一覧)
6. [関連ドキュメントリンク](#6-関連ドキュメントリンク)
7. [外部リソース](#7-外部リソース)

---

## 1. プロジェクト固有の用語

### 1.1 ビジネス用語

| 用語 | 英語表記 | 定義 |
|------|----------|------|
| 保管場所 | Storage Location | 製品が保管されるエリア（エリアA、エリアBなど） |
| 保管環境 | Storage Environment | 保管場所の温度・湿度などの環境条件 |
| 履歴表 | History Table | センサーの保管場所移動履歴を記録したテーブル |
| 計測ログ | Measurement Log | センサーが記録した温湿度データ |
| センサナンバー | Sensor Number | センサーを識別する内部番号 |
| センサーシリアル | Sensor Serial | センサーの製造番号（デバイスID） |
| LOT | Lot Number | 製品のロット番号 |

### 1.2 工程区分

| 区分 | コード | 説明 | 対象エリア |
|------|--------|------|------------|
| 常温 | RT | Room Temperature | エリアA, B, C, D, E |
| 逆浸透 | RO | Reverse Osmosis | エリアX |
| 限外ろ過 | UF | Ultrafiltration | エリアY, Z |

### 1.3 データ層

| 層 | 英語 | 説明 |
|----|------|------|
| Staging層 | Staging Layer | 生データの取り込みと基本的な正規化を行う層 |
| Curated層 | Curated Layer | ビジネスロジックを適用し、分析に適した形式に変換する層 |
| セマンティックモデル | Semantic Model | 分析用に最適化されたデータモデル |

---

## 2. 略語一覧

| 略語 | 正式名称 | 説明 |
|------|----------|------|
| PPU | Premium Per User | Power BIのユーザー単位Premiumライセンス |
| DF | Dataflow | Power BIのデータフロー |
| Stg | Staging | Staging層を示すプレフィックス |
| Cur | Curated | Curated層を示すプレフィックス |
| JST | Japan Standard Time | 日本標準時（UTC+9） |
| CSV | Comma-Separated Values | カンマ区切りテキストファイル |
| AH | Absolute Humidity | 絶対湿度（g/m³） |
| RH | Relative Humidity | 相対湿度（%） |
| PK | Primary Key | 主キー |
| FK | Foreign Key | 外部キー |
| UK | Unique Key | 一意キー |

---

## 3. 技術用語

### 3.1 データベース・ETL用語

| 用語 | 説明 |
|------|------|
| ETL | Extract（抽出）、Transform（変換）、Load（読み込み）の略。データ統合プロセス |
| データフロー | Power BIでのセルフサービスETLツール |
| エンティティ | データフロー内の個々のテーブル |
| 区間JOIN | 時間範囲に基づいてデータを結合する処理 |
| FillDown | 空のセルを上の行の値で埋める処理 |
| クエリ折りたたみ | クエリをデータソースのネイティブクエリに変換する最適化 |

### 3.2 時間・日時用語

| 用語 | 説明 |
|------|------|
| ISO 8601 | 日時の国際標準表記（例: 2025-10-23T18:10:00+09:00） |
| タイムゾーン | 時間帯（本プロジェクトではJSTを使用） |
| 半開区間 | 開始を含み終了を含まない区間（[start, end)） |
| datetimezone | タイムゾーン情報を含む日時型 |

### 3.3 環境計測用語

| 用語 | 説明 | 単位 |
|------|------|------|
| 温度 | Temperature | ℃（摂氏） |
| 相対湿度 | Relative Humidity | %（パーセント） |
| 絶対湿度 | Absolute Humidity | g/m³ |
| 飽和水蒸気圧 | Saturation Vapor Pressure | hPa |

---

## 4. Power Query M言語リファレンス

### 4.1 本プロジェクトで使用する主な関数

#### テーブル操作

| 関数 | 説明 | 使用例 |
|------|------|--------|
| `Table.SelectRows` | 条件に一致する行を選択 | `Table.SelectRows(Source, each [Column] > 0)` |
| `Table.SelectColumns` | 指定列のみを選択 | `Table.SelectColumns(Source, {"Col1", "Col2"})` |
| `Table.TransformColumnTypes` | 列のデータ型を変換 | `Table.TransformColumnTypes(Source, {{"Col", type number}})` |
| `Table.RenameColumns` | 列名を変更 | `Table.RenameColumns(Source, {{"OldName", "NewName"}})` |
| `Table.AddColumn` | 新しい列を追加 | `Table.AddColumn(Source, "NewCol", each [Col1] + [Col2])` |
| `Table.Sort` | テーブルをソート | `Table.Sort(Source, {{"Col", Order.Ascending}})` |
| `Table.FillDown` | 空のセルを上の値で埋める | `Table.FillDown(Source, {"Col1", "Col2"})` |
| `Table.Group` | グループ化 | `Table.Group(Source, {"GroupCol"}, {{"Grouped", each _}})` |
| `Table.NestedJoin` | テーブルを結合 | `Table.NestedJoin(Table1, "Key1", Table2, "Key2", "Joined")` |
| `Table.Combine` | 複数テーブルを結合 | `Table.Combine({Table1, Table2})` |
| `Table.Distinct` | 重複を排除 | `Table.Distinct(Source, {"Key"})` |

#### 日時操作

| 関数 | 説明 | 使用例 |
|------|------|--------|
| `DateTimeZone.FromText` | 文字列からdatetimezoneを生成 | `DateTimeZone.FromText("2025-10-23T18:10:00+09:00")` |
| `DateTime.FromText` | 文字列からdatetimeを生成 | `DateTime.FromText("2025/10/23 18:10", [Format="yyyy/M/d H:mm"])` |
| `DateTime.ToText` | datetimeを文字列に変換 | `DateTime.ToText(dt, "yyyy-MM-dd")` |

#### 数値操作

| 関数 | 説明 | 使用例 |
|------|------|--------|
| `Number.Exp` | 指数関数（e^x） | `Number.Exp(1)` |
| `Number.Abs` | 絶対値 | `Number.Abs(-5)` |
| `Number.Round` | 四捨五入 | `Number.Round(3.14159, 2)` |

### 4.2 エラーハンドリング

```powerquery
// try...otherwise構文
SafeValue = try Expression otherwise DefaultValue,

// try式の結果
Result = try Expression,
// Result[HasError] : エラーが発生したかどうか（true/false）
// Result[Value] : 成功時の値
// Result[Error] : エラー時のエラー情報
```

---

## 5. データスキーマ一覧

### 5.1 入力データ（CSVファイル）

#### センサーマスタ.csv

| 列名 | データ型 | 説明 | 制約 |
|------|----------|------|------|
| センサナンバー | text | センサー識別番号 | 必須 |
| センサーシリアル | text | センサーシリアル番号 | 必須、一意 |

#### 履歴表.csv

| 列名 | データ型 | 説明 | 制約 |
|------|----------|------|------|
| センサナンバー | text | センサー識別番号 | 必須 |
| LOT | text | ロット番号 | 必須 |
| 保管場所 | text | 保管エリア名 | 必須 |
| 日時 | text | 移動日時 | 必須、形式: yyyy/M/d H:mm |

#### 計測ログ_*.csv

| 列名 | データ型 | 説明 | 制約 |
|------|----------|------|------|
| created_at | text | 計測日時 | 必須、ISO 8601形式 |
| field1(Temperature ºC ) | text | 温度（℃） | 必須 |
| field2(Humidity) | text | 相対湿度（%） | 必須 |
| serial | text | センサーシリアル | 必須 |

### 5.2 Staging層エンティティ

#### Stg_センサーマスタ

| 列名 | データ型 | 説明 |
|------|----------|------|
| センサナンバー | Int64.Type | センサー識別番号 |
| センサーシリアル | text | センサーシリアル番号 |

#### Stg_履歴表

| 列名 | データ型 | 説明 |
|------|----------|------|
| センサナンバー | Int64.Type | センサー識別番号 |
| LOT | text | ロット番号 |
| 保管場所 | text | 保管エリア名 |
| 日時 | datetimezone | 移動日時（JST） |

#### Stg_計測ログ

| 列名 | データ型 | 説明 |
|------|----------|------|
| created_at | datetimezone | 計測日時（JST） |
| Temperature | number | 温度（℃） |
| Humidity | number | 相対湿度（%） |
| serial | text | センサーシリアル |

#### Stg_有効期間

| 列名 | データ型 | 説明 |
|------|----------|------|
| 有効期間ID | Int64.Type | 期間識別子 |
| 開始日時 | datetimezone | 有効期間開始 |
| 終了日時 | datetimezone | 有効期間終了 |
| 説明 | text | 期間の説明 |

### 5.3 Curated層エンティティ

#### Cur_計測ログ_共通 / Cur_計測ログ_RT/RO/UF

| 列名 | データ型 | 説明 |
|------|----------|------|
| created_at | datetimezone | 計測日時 |
| センサナンバー | Int64.Type | センサー識別番号 |
| LOT | text | ロット番号 |
| 保管場所 | text | 保管エリア |
| Temperature | number | 温度（℃） |
| Humidity | number | 相対湿度（%） |
| AbsoluteHumidity | number | 絶対湿度（g/m³） |
| 工程区分 | text | RT/RO/UF（ファクトテーブルのみ） |

---

## 6. 関連ドキュメントリンク

### 6.1 プロジェクトドキュメント

| ドキュメント | 説明 | リンク |
|--------------|------|--------|
| 全体概要 | プロジェクトの目的・スコープ | [00_overview.md](./00_overview.md) |
| 環境構築手順 | 環境構築の手順 | [01_environment_setup.md](./01_environment_setup.md) |
| Staging層実装手順 | Staging層の実装詳細 | [02_staging_layer.md](./02_staging_layer.md) |
| Curated層実装手順 | Curated層の実装詳細 | [03_curated_layer.md](./03_curated_layer.md) |
| 区間JOIN処理詳細 | FillDownによる区間JOIN | [04_interval_join_logic.md](./04_interval_join_logic.md) |
| テスト手順 | テストの実施方法 | [05_testing_procedure.md](./05_testing_procedure.md) |
| トラブルシューティング | 問題対処法 | [06_troubleshooting.md](./06_troubleshooting.md) |

### 6.2 データファイル

| ファイル | 説明 | パス |
|----------|------|------|
| センサーマスタ | センサー基本情報 | `data/センサーマスタ.csv` |
| 履歴表 | 保管場所履歴 | `data/履歴表.csv` |
| 計測ログ（サンプル） | センサー計測データ | `data/計測ログ_*.csv` |

---

## 7. 外部リソース

### 7.1 Microsoft公式ドキュメント

| リソース | URL |
|----------|-----|
| Power BI ドキュメント | https://docs.microsoft.com/power-bi/ |
| Power Query M言語リファレンス | https://docs.microsoft.com/powerquery-m/ |
| データフローのベストプラクティス | https://docs.microsoft.com/power-bi/transform-model/dataflows/dataflows-best-practices |

### 7.2 技術参考資料

| リソース | 説明 |
|----------|------|
| ISO 8601 | 日時表記の国際標準 |
| 絶対湿度計算式 | Magnus-Tetens近似式 |

### 7.3 サポート連絡先

| 問い合わせ種別 | 連絡先 |
|----------------|--------|
| 技術的な問題 | プロジェクト技術リーダー |
| 権限・ライセンス | IT部門 |
| データに関する問い合わせ | データ管理チーム |

---

**前のステップ**: [トラブルシューティング](./06_troubleshooting.md)
**ドキュメント先頭へ**: [全体概要](./00_overview.md)
