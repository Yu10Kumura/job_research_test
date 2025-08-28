"""
テスト用のダミーランカー - OpenAI APIを使わずに動作確認
"""

from typing import Dict, List, Any
import random

def rank_jobs_with_llm_dummy(profile: Dict[str, str], jobs: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    テスト用ダミーランカー
    """
    print("🤖 [テストモード] ダミーAIで求人を分析中...")
    
    if not jobs:
        return {
            "recommendations": [],
            "message": "申し訳ございませんが、求人情報が見つかりませんでした。"
        }
    
    # ダミーのマッチング結果を生成
    recommendations = []
    
    # 最大3件までランダムに選択
    selected_jobs = random.sample(jobs, min(3, len(jobs)))
    
    dummy_reasons = [
        f"{profile.get('job_type', '職種')}の経験が活かせる職種です",
        f"{profile.get('industry', '業界')}での{profile.get('experience_years', 0)}年の経験に適合します", 
        "幅広い業務経験を持つあなたに最適なポジションです",
        "チームマネジメント経験が重宝される職種です",
        "コンサルティングスキルが活用できる業務内容です"
    ]
    
    for i, job in enumerate(selected_jobs):
        recommendations.append({
            "title": job['title'],
            "url": job['url'],
            "reason": dummy_reasons[i % len(dummy_reasons)]
        })
    
    return {
        "recommendations": recommendations,
        "message": "あなたに合う可能性のある職種は下記です。（テストモード）"
    }

if __name__ == "__main__":
    # テスト
    test_profile = {"industry": "人材業界", "job_type": "採用コンサルタント", "experience_years": 10}
    test_jobs = [
        {"title": "テスト求人1", "url": "http://example.com/1"},
        {"title": "テスト求人2", "url": "http://example.com/2"}
    ]
    
    result = rank_jobs_with_llm_dummy(test_profile, test_jobs)
    print("テスト結果:", result)
