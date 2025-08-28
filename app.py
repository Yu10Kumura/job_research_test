"""
三菱電機 求人レコメンドシステム - Streamlit版
"""

import streamlit as st
import sys
import os
from typing import Dict, List

# パスを追加してインポートを確実にする
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 必要なモジュールをインポート
try:
    from src.extractors.simple_html_extractor import SimpleJobExtractor
    from src.ranker.llm_ranker import LLMJobRanker
except ImportError as e:
    st.error(f"モジュールのインポートエラー: {e}")
    st.write("デバッグ情報:")
    st.write(f"Current directory: {current_dir}")
    st.write(f"Python path: {sys.path}")
    st.write(f"Files in current directory: {os.listdir(current_dir)}")
    if os.path.exists(os.path.join(current_dir, 'src')):
        st.write(f"Files in src directory: {os.listdir(os.path.join(current_dir, 'src'))}")
    st.stop()

# ページ設定
st.set_page_config(
    page_title="三菱電機 求人レコメンドシステム",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'jobs_loaded' not in st.session_state:
    st.session_state.jobs_loaded = False
if 'all_jobs' not in st.session_state:
    st.session_state.all_jobs = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

def load_jobs():
    """求人データを読み込み"""
    if not st.session_state.jobs_loaded:
        with st.spinner("🌐 三菱電機採用サイトから全求人を取得中..."):
            try:
                job_extractor = SimpleJobExtractor()
                url = 'https://progres02.jposting.net/pgmitsubishielectric/u/job.phtml'
                jobs = job_extractor.extract_all_jobs(url)
                
                if jobs:
                    st.session_state.all_jobs = jobs
                    st.session_state.jobs_loaded = True
                    
                    # カテゴリ別集計
                    categories = job_extractor.get_job_categories(jobs)
                    st.success(f"✅ {len(jobs)}件の求人があります")
                    
                    # サイドバーには統計情報は表示しない（シンプルに）
                    pass
                else:
                    st.error("❌ 求人情報が取得できませんでした。")
                    st.stop()
                    
            except Exception as e:
                st.error(f"❌ エラーが発生しました: {e}")
                st.stop()

def get_recommendations(profile: Dict[str, str]):
    """AIレコメンデーションを取得"""
    try:
        llm_ranker = LLMJobRanker()
        with st.spinner("🤖 AIがあなたに最適な求人を分析中..."):
            result = llm_ranker.rank_jobs(profile, st.session_state.all_jobs)
            return result
    except Exception as e:
        st.error(f"❌ AI分析でエラーが発生しました: {e}")
        return {"recommendations": [], "message": "エラーが発生しました"}

def display_recommendations(recommendations: List[Dict[str, str]]):
    """レコメンデーション結果を表示"""
    if not recommendations:
        st.warning("条件に合う求人が見つかりませんでした。別の条件でお試しください。")
        return
    
    # 適合度別に分類
    high_recs = [r for r in recommendations if '【適合度: 高】' in r['reason']]
    mid_recs = [r for r in recommendations if '【適合度: 中・参考】' in r['reason']]
    
    # 概要表示
    st.markdown(f"### 📊 マッチング結果")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("総提案数", len(recommendations))
    with col2:
        st.metric("推奨度: 高", len(high_recs))
    with col3:
        st.metric("参考程度", len(mid_recs))
    
    # 適合度「高」の求人を表示
    if high_recs:
        st.markdown("### 🎯 推奨求人")
        for i, rec in enumerate(high_recs, 1):
            with st.expander(f"{i}. {rec['title']}", expanded=True):
                # 理由から「【適合度: 高】」を除去して表示
                reason_clean = rec['reason'].replace('【適合度: 高】', '').strip()
                st.markdown(f"**理由:** {reason_clean}")
                st.markdown(f"**詳細:** [求人詳細を見る]({rec['url']})")
    
    # 適合度「中」の求人を表示
    if mid_recs:
        st.markdown("---")
        st.markdown("### 📝 参考求人")
        st.info("💡 以下は参考程度にご検討ください（正確ではない可能性があります）")
        
        for i, rec in enumerate(mid_recs, len(high_recs) + 1):
            with st.expander(f"{i}. {rec['title']}"):
                # 理由から不要なテキストを除去
                reason_clean = rec['reason'].replace('【適合度: 中・参考】', '').replace('（参考程度にご検討ください。正確ではない可能性があります）', '').strip()
                st.markdown(f"**理由:** {reason_clean}")
                st.markdown(f"**詳細:** [求人詳細を見る]({rec['url']})")

def main():
    """メインアプリケーション"""
    
    # ヘッダー
    st.title("🚀 三菱電機 求人レコメンドシステム")
    st.markdown("AI powered job matching system using GPT-4o-mini")
    st.markdown("---")
    
    # サイドバー
    with st.sidebar:
        st.markdown("### � システム説明")
        st.markdown("このシステムは三菱電機の採用ページから求人を抽出し、AIがあなたに最適な求人を提案します。")
        
        # 求人データ読み込み
        if st.button("🔄 求人データを更新してやり直す", type="secondary"):
            st.session_state.jobs_loaded = False
            st.session_state.all_jobs = []
            st.rerun()
    
    # 求人データ読み込み
    load_jobs()
    
    if not st.session_state.jobs_loaded:
        st.warning("求人データの読み込み中...")
        return
    
    # 入力フォーム
    st.markdown("### 📝 あなたの経験を入力してください。")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.text_input(
                "業界",
                placeholder="例: 自動車業界, IT業界, 製造業, 電力業界",
                help="あなたの経験がある業界を入力してください"
            )
            
        with col2:
            job_type = st.text_input(
                "職種",
                placeholder="例: 生産技術, システム開発, 営業, 設計, 品質管理",
                help="現在または希望する職種を入力してください"
            )
        
        work_experience = st.text_area(
            "これまでのご経験について（100文字以内）",
            placeholder="例: 自動車部品の組み立てライン作業とリーダー業務（5年間）",
            max_chars=100,
            help="これまでの仕事経験を具体的に記載してください",
            height=100
        )
        
        submitted = st.form_submit_button("🔍 マッチする可能性のある求人をAIで探してみる", type="primary")
    
    # フォーム送信後の処理
    if submitted:
        if not industry or not job_type or not work_experience:
            st.error("⚠️ すべての項目を入力してください")
            return
        
        # プロフィール確認
        st.markdown("### 📋 入力内容の確認")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**業界:** {industry}")
        with col2:
            st.info(f"**職種:** {job_type}")
        with col3:
            st.info(f"**経験:** {work_experience[:30]}...")
        
        # AIレコメンデーション実行
        profile = {
            "industry": industry,
            "job_type": job_type,
            "work_experience": work_experience
        }
        
        result = get_recommendations(profile)
        
        if result and result.get('recommendations'):
            st.session_state.recommendations = result['recommendations']
            display_recommendations(result['recommendations'])
        else:
            st.warning("条件に合う求人が見つかりませんでした。")
    
    # フッター
    st.markdown("---")
    st.markdown("### 💡 ヒント")
    st.markdown("""
    - **業界**: 具体的な業界名を入力すると、より精度の高いマッチングが可能です
    - **職種**: 現在の職種または希望する職種を明確に記載してください  
    - **経験**: 具体的な業務内容と期間を記載すると、適切な求人を提案できます
    """)

if __name__ == "__main__":
    main()
