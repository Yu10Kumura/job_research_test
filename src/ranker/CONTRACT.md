# Ranker Contract

## 目的
ユーザープロフィールと求人リストをマッチングし、おすすめ求人をランキング形式で提案

## 入力
### プロフィール (Dict)
```json
{
  "industry": "自動車業界",
  "job_type": "生産技術", 
  "experience_years": 5
}
```

### 求人リスト (List[Dict])
```json
[
  {
    "title": "生産技術エンジニア（○○工場）",
    "url": "https://progres02.jposting.net/pgmitsubishielectric/u/job/job.phtml?job_id=12345"
  }
]
```

## 出力
### 成功時
```json
{
  "recommendations": [
    {
      "title": "生産技術エンジニア（○○工場）",
      "url": "https://progres02.jposting.net/pgmitsubishielectric/u/job/job.phtml?job_id=12345",
      "reason": "自動車業界での生産技術経験5年を活かせる職種です"
    }
  ],
  "message": "あなたに合う可能性のある職種は下記です。"
}
```

### マッチなし時
```json
{
  "recommendations": [],
  "message": "申し訳ございませんが、現在あなたのプロフィールに合う求人は見つかりませんでした。"
}
```

## 制約
- 最大5件まで推薦
- 無理にレコメンドしない（合わない場合は空配列）
- GPT-4o-miniを使用してマッチング判定

## エラー時
- 例外を発生させ、メッセージを返す
