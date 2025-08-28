# Extractor Contract

## 目的
企業の採用ページURLから求人情報を抽出する

## 入力
- URL (str): 採用ページのURL
- 例: "https://progres02.jposting.net/pgmitsubishielectric/u/job.phtml"

## 出力
- 求人リスト (List[Dict])
```json
[
  {
    "title": "生産技術エンジニア（○○工場）",
    "url": "https://progres02.jposting.net/pgmitsubishielectric/u/job/job.phtml?job_id=12345"
  },
  {
    "title": "品質管理スタッフ（△△事業所）",
    "url": "https://progres02.jposting.net/pgmitsubishielectric/u/job/job.phtml?job_id=67890"
  }
]
```

## エラー時
- 例外を発生させ、メッセージを返す
- エラーケース:
  - URLにアクセスできない
  - HTMLの構造が想定と異なる
  - 求人が見つからない

## 実装方針
- JPOSTINGサイト専用の実装
- BeautifulSoupを使用してHTMLを解析
- 求人タイトルと詳細URLを抽出
