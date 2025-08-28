"""
LLM求人マッチャー - GPT-4o-miniを使用
ユーザープロフィールと求人リストをマッチング
"""

import os
import json
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

class LLMJobRanker:
    def __init__(self):
        # Streamlit Cloudの場合はst.secretsから、ローカルの場合はconfig.envから読み込み
        api_key = None
        
        # まずStreamlit secretsを試行
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY")
        except:
            pass
            
        # Streamlit secretsで取得できなかった場合、環境変数を試行
        if not api_key:
            try:
                load_dotenv('config.env')
                api_key = os.getenv('OPENAI_API_KEY')
            except:
                # 直接環境変数から取得を試行
                api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。Streamlit CloudのSecretsまたはconfig.envファイルを確認してください。")
        
        self.client = OpenAI(api_key=api_key)
        print("🤖 GPT-4o-mini求人ランカーを初期化しました")
        
        self.client = OpenAI(api_key=api_key)
        print("🤖 GPT-4o-mini求人ランカーを初期化しました")
    
    def rank_jobs(self, profile: Dict[str, str], jobs: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        求人をユーザープロフィールに基づいてランキング
        """
        try:
            if not jobs:
                return {
                    "recommendations": [],
                    "message": "申し訳ございませんが、求人情報が見つかりませんでした。"
                }
            
            print(f"🤖 GPT-4o-miniで{len(jobs)}件の求人を分析中...")
            
            # プロンプト作成
            prompt = self._create_ranking_prompt(profile, jobs)
            
            # OpenAI API呼び出し
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "あなたは経験豊富な採用コンサルタントです。クライアントの転職成功を最優先に、専門的で価値のある提案を行ってください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            # レスポンス解析
            result_text = response.choices[0].message.content.strip()
            print(f"🔍 LLMの生レスポンス:")
            print("=" * 60)
            print(result_text)
            print("=" * 60)
            
            recommendations = self._parse_recommendations(result_text, jobs)
            
            # 結果の構築
            if recommendations:
                return {
                    "recommendations": recommendations,
                    "message": f"{len(recommendations)}件の最適な求人をご提案いたします。"
                }
            else:
                return {
                    "recommendations": [],
                    "message": "申し訳ございませんが、現在のプロフィールに適合する求人が見つかりませんでした。より詳細な経験やスキル、ご希望をお聞かせください。"
                }
        
        except Exception as e:
            print(f"❌ LLMランキングエラー: {e}")
            return {
                "recommendations": [],
                "message": f"申し訳ございません、分析中にエラーが発生しました: {str(e)}"
            }
    
    def _create_ranking_prompt(self, profile: Dict[str, str], jobs: List[Dict[str, str]]) -> str:
        """
        プロフィールと求人リストから分析プロンプトを作成
        """
        industry = profile.get('industry', '未指定')
        job_type = profile.get('job_type', '未指定')
        work_experience = profile.get('work_experience', '未指定')
        
        # 求人情報をリスト化
        jobs_text = ""
        for i, job in enumerate(jobs, 1):
            jobs_text += f"{i}. {job['title']}\n"
        
        prompt = f"""
あなたは経験豊富な採用コンサルタントです。以下のクライアントプロフィールと求人リストを専門的な視点で分析し、戦略的な転職提案を行ってください。

【クライアントプロフィール】
業界: {industry}
職種: {job_type}  
これまでのご経験: {work_experience}

【求人リスト】
{jobs_text}

【分析指示】
以下の観点から各求人を評価し、クライアントにとって価値のあるキャリア提案を行ってください：

1. **経験活用性**: 記載された具体的な経験をどの程度活かせるか
2. **キャリアパス現実性**: 現在の経験レベルから現実的に到達可能か
3. **スキル転換可能性**: 既存スキルを新分野でどう活用できるか
4. **業界適合性**: 業界知識・経験の活用可能性
5. **成長機会**: 中長期的な成長機会とリスク評価

【出力形式】
以下の形式で最大5件まで提案してください（現実的なキャリアパスを重視してください）：

1番目: [求人番号]
適合度: [高/中/低]
提案理由: [クライアントの具体的な経験をどう活かせるか、現実的なキャリアステップとしてどう位置づけられるかを2-3文で説明]
注意点: [転職時の課題や習得すべきスキルがあれば1文で]

【重要な判断基準】
- 記載された具体的な経験内容を最重視してください
- ブルーカラー→ホワイトカラーのような大幅な職種転換は慎重に判断してください
- 現実的なキャリアステップを提案してください（例: 製造現場→製造技術、営業→営業企画など）
- 経験を活かした横展開や、段階的なステップアップを重視してください
- 真に現実的な提案がない場合のみ「適合する求人がありません」と回答してください
"""
        return prompt
    
    def _parse_recommendations(self, result_text: str, jobs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        LLMの回答を解析してレコメンデーション形式に変換
        """
        recommendations = []
        
        try:
            # 「適合する求人がありません」のチェック  
            if "適合する求人がありません" in result_text or "適合しない" in result_text:
                return []
            
            lines = result_text.split('\n')
            current_job_num = None
            current_reason = ""
            current_fitness = ""
            current_notes = ""
            
            for line in lines:
                line = line.strip()
                
                # 順位パターンを探す (例: "1番目: 3", "2番目: 1")
                ranking_match = None
                import re
                
                patterns = [
                    r'(\d+)番目[：:]\s*\[(\d+)\]',  # "1番目: [150]"形式
                    r'(\d+)番目[：:]\s*\[?求人番号\s*(\d+)\]?',  # "1番目: [求人番号 1]"形式
                    r'(\d+)番目[：:]\s*(\d+)',  # "1番目: 3"形式
                    r'(\d+)\.\s*\[(\d+)\]',  # "1. [150]"形式
                    r'(\d+)\.\s*(\d+)',  # "1. 3"形式
                    r'第(\d+)位[：:]\s*\[(\d+)\]',  # "第1位: [150]"形式
                    r'第(\d+)位[：:]\s*(\d+)',  # "第1位: 3"形式
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        ranking_match = match
                        break
                
                if ranking_match:
                    # 前の求人の処理を完了
                    if current_job_num is not None and current_reason:
                        combined_reason = f"{current_reason}"
                        if current_fitness:
                            combined_reason = f"【適合度: {current_fitness}】{combined_reason}"
                        if current_notes:
                            combined_reason += f" ※{current_notes}"
                        self._add_recommendation(recommendations, current_job_num, combined_reason, jobs)
                    
                    # 新しい求人番号を取得
                    current_job_num = int(ranking_match.group(2))
                    current_reason = ""
                    current_fitness = ""
                    current_notes = ""
                
                # 各フィールドの行を探す
                elif line.startswith('適合度:') or line.startswith('適合度：'):
                    current_fitness = line.replace('適合度:', '').replace('適合度：', '').strip()
                elif line.startswith('提案理由:') or line.startswith('提案理由：'):
                    current_reason = line.replace('提案理由:', '').replace('提案理由：', '').strip()
                elif line.startswith('理由:') or line.startswith('理由：'):
                    current_reason = line.replace('理由:', '').replace('理由：', '').strip()
                elif line.startswith('注意点:') or line.startswith('注意点：'):
                    current_notes = line.replace('注意点:', '').replace('注意点：', '').strip()
                elif current_job_num is not None and line and not line.startswith(tuple('0123456789第適提理注')):
                    # 理由の続きの可能性
                    if current_reason:
                        current_reason += " " + line
                    else:
                        current_reason = line
            
            # 最後の求人を追加
            if current_job_num is not None and current_reason:
                combined_reason = f"{current_reason}"
                if current_fitness:
                    combined_reason = f"【適合度: {current_fitness}】{combined_reason}"
                if current_notes:
                    combined_reason += f" ※{current_notes}"
                self._add_recommendation(recommendations, current_job_num, combined_reason, jobs)
            
            # 最大5件まで
            return recommendations[:5]
            
        except Exception as e:
            print(f"⚠️ レスポンス解析エラー: {e}")
            print(f"生レスポンス: {result_text}")
            return []
    
    def _add_recommendation(self, recommendations: List, job_num: int, reason: str, jobs: List[Dict[str, str]]):
        """
        レコメンデーションリストに追加
        """
        try:
            if 1 <= job_num <= len(jobs):
                job = jobs[job_num - 1]
                
                # 適合度「中」の場合は特別な表示に変更
                modified_reason = reason
                if "【適合度: 中】" in reason:
                    modified_reason = reason.replace("【適合度: 中】", "【適合度: 中・参考】")
                    modified_reason += "（参考程度にご検討ください。正確ではない可能性があります）"
                
                recommendations.append({
                    "title": job["title"],
                    "url": job.get("url", ""),
                    "reason": modified_reason
                })
                print(f"✅ 求人{job_num}: {job['title']} を追加")
            else:
                print(f"⚠️ 無効な求人番号: {job_num} (範囲: 1-{len(jobs)})")
        except Exception as e:
            print(f"⚠️ レコメンデーション追加エラー: {e}")
    
    def validate_api_key(self) -> bool:
        """
        APIキーの有効性をチェック
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"❌ API Key validation failed: {e}")
            return False
