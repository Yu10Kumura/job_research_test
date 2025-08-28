"""
テストデータセット - 三菱電機の実際の求人パターンに基づく
より現実的なレコメンドテストのため、実際の求人トレンドを反映
"""

# 電力・エネルギー系エンジニアリング求人（三菱電機の主力事業）
POWER_ENGINEERING_JOBS = [
    {
        "title": "【東京/WEB面接可】直流送電技術のリードエンジニア・R&D【エネルギーシステム事業本部】",
        "url": "https://example.com/job1",
        "description": "直流送電技術の研究開発、電力システム設計、プロジェクト推進業務。電気・電子系学位、電力システム設計経験3年以上、直流送電技術知見、英語力が必要。"
    },
    {
        "title": "【神戸/WEB面接可】システムエンジニア：鉄道会社向け電力管理システム【神戸製作所】",
        "url": "https://example.com/job2",
        "description": "鉄道会社向け電力管理システムの設計・開発。システム開発経験5年以上、鉄道システム経験、プロジェクト管理、Linux/Unix知識が求められる。"
    },
    {
        "title": "【神戸/WEB面接可】原子力発電所向け制御システムの設計【電力システム製作所】",
        "url": "https://example.com/job3", 
        "description": "原子力発電所向け計装・制御システムの設計業務。制御システム設計経験、原子力関連知識、安全設計、品質管理経験必須。"
    },
    {
        "title": "【横浜/WEB面接可】電力ICTシステムのソフトウェア開発【電力システム製作所】",
        "url": "https://example.com/job4",
        "description": "送配電事業者向けの業務/DXシステム開発。C++/Java、電力システム知識、データベース設計経験が必要。"
    },
    {
        "title": "【神戸/WEB面接可】変電所監視制御システムの開発【系統変電システム製作所】",
        "url": "https://example.com/job5",
        "description": "変電所監視制御システムの設計・開発業務。電力システム、SCADA、リアルタイムシステム開発経験。"
    }
]

# 防衛・宇宙事業系求人（高度技術・セキュリティ要件）
DEFENSE_SPACE_JOBS = [
    {
        "title": "【神奈川/WEB面接可】防衛事業におけるレーダシステムのシステム設計【鎌倉製作所】",
        "url": "https://example.com/defense1",
        "description": "防衛事業向けレーダシステムの設計・開発。レーダシステム経験、電波工学、システム設計、セキュリティクリアランス対応可能な方。"
    },
    {
        "title": "【神奈川/WEB面接可】人工衛星のシステム設計/打ち上げ後の運用【鎌倉製作所】",
        "url": "https://example.com/defense2",
        "description": "人工衛星のシステム設計および運用業務。宇宙機システム経験、軌道力学、通信技術、品質管理経験。"
    },
    {
        "title": "【神奈川/WEB面接可】航空機（次期戦闘機）搭載用センサのシステム設計【鎌倉製作所】",
        "url": "https://example.com/defense3",
        "description": "次期戦闘機向けセンサシステムの設計・開発。航空電子機器経験、センサ技術、組込みシステム、国際協力経験。"
    },
    {
        "title": "【神奈川/WEB面接可】防衛装備品における光学センサ機器のH/W開発【鎌倉製作所】",
        "url": "https://example.com/defense4",
        "description": "防衛装備品向け光学センサ機器のハードウェア開発・設計。光学技術、電子回路設計、画像処理技術。"
    },
    {
        "title": "【神奈川/WEB面接可】大規模情報処理システム開発【鎌倉製作所】",
        "url": "https://example.com/defense5",
        "description": "大規模情報処理システムのシステムエンジニアリング業務。分散システム、高信頼性設計、リアルタイム処理。"
    }
]

# 製造・生産技術系求人（ものづくりの現場）
MANUFACTURING_JOBS = [
    {
        "title": "【静岡】空調用圧縮機の設計開発業務【静岡製作所】",
        "url": "https://example.com/mfg1",
        "description": "空調用圧縮機の設計・開発業務。機械設計経験3年以上、熱力学、流体力学、CAD操作スキル必要。"
    },
    {
        "title": "【日立】大型発電機の組立技術スタッフ【電力システム製作所】",
        "url": "https://example.com/mfg2",
        "description": "大型発電機の組立・調整工法改善・開発。機械組立経験、大型機械取扱、工程管理、品質管理経験。"
    },
    {
        "title": "【姫路/WEB面接可】電動パワーステアリング用モータ設計【姫路事業所】",
        "url": "https://example.com/mfg3",
        "description": "電動パワーステアリング用モータの設計・開発。モータ設計経験、自動車部品知識、電磁界解析、制御技術。"
    },
    {
        "title": "【和歌山】業務用空調機の開発評価と量産導入準備【冷熱システム製作所】",
        "url": "https://example.com/mfg4",
        "description": "業務用空調機の開発評価および量産導入準備業務。評価技術、品質管理、量産技術、プロジェクト管理。"
    },
    {
        "title": "【尼崎】次世代戦闘機事業におけるシステム開発【電子通信システム製作所】",
        "url": "https://example.com/mfg5",
        "description": "次世代戦闘機事業におけるシステム開発。航空電子システム、組込みソフトウェア、リアルタイムOS。"
    }
]

# ビジネス系求人（営業・企画・管理）
BUSINESS_JOBS = [
    {
        "title": "【東京/WEB面接可】海外営業：海外電力会社向け発電システム関連の営業【電力システム製作所】",
        "url": "https://example.com/biz1", 
        "description": "海外電力会社向け発電システムの営業活動。海外営業経験5年以上、英語力（ビジネスレベル）、電力業界知識、プロジェクト管理経験。"
    },
    {
        "title": "【東京/WEB面接可】事業企画・戦略立案、マーケティング戦略・販売企画【エネルギーシステム事業本部】",
        "url": "https://example.com/biz2",
        "description": "エネルギー事業の戦略立案・マーケティング企画。事業企画経験、戦略コンサル、マーケティング、データ分析スキル。"
    },
    {
        "title": "人事採用担当（新卒採用の施策企画・運営）【グローバル人財部・採用グループ】",
        "url": "https://example.com/biz3",
        "description": "新卒採用の施策企画・運営業務。人事採用経験3年以上、新卒採用企画、大学連携、データ分析経験。"
    },
    {
        "title": "【東京/WEB面接可】コーポレート経理部門における国際税務プロフェッショナル要員【本社経理部】", 
        "url": "https://example.com/biz4",
        "description": "国際税務業務の専門家として税務戦略立案・実行。税理士資格、国際税務経験、英語力、M&A税務経験。"
    },
    {
        "title": "【東京/WEB面接可】防衛製品の海外向け営業活動【防衛宇宙システム事業本部】",
        "url": "https://example.com/biz5",
        "description": "防衛製品の海外展開営業。防衛業界経験、海外営業、英語力、セキュリティクリアランス対応可能。"
    },
    {
        "title": "採用コンサルタント・リクルーター（中途採用担当）【人財開発センター】",
        "url": "https://example.com/biz6",
        "description": "技術系中途採用のコンサルティング営業。採用コンサル経験、人材紹介業務、技術職理解、面接スキル、営業経験。"
    },
    {
        "title": "人事労務・組織開発スペシャリスト【労務・働き方改革推進部】",
        "url": "https://example.com/biz7",
        "description": "労務管理および組織開発業務。社会保険労務士、人事制度設計、労務管理、組織開発、働き方改革推進。"
    },
    {
        "title": "【グローバル】採用戦略・ブランディング企画【タレントアクイジション部】",
        "url": "https://example.com/biz8",
        "description": "グローバル採用戦略の立案・実行。採用マーケティング、ブランディング、SNS活用、データ分析、英語力。"
    }
]

# IT・デジタル系求人（DX推進・AI活用）
IT_DIGITAL_JOBS = [
    {
        "title": "【東京/WEB面接可】三菱電機グループのAI活用による業務改革推進【本社(AI・クラウドソリューション部)】",
        "url": "https://example.com/it1",
        "description": "AI活用による業務改革の推進・ビジネスアナリスト業務。AI・機械学習、Python、データサイエンス、業務改革経験。"
    },
    {
        "title": "【東京/WEB面接可】三菱電機グループクラウド基盤の企画・構築・運用【本社(AI・クラウドソリューション部)】",
        "url": "https://example.com/it2", 
        "description": "クラウドエンジニア・ソリューションアーキテクト業務。AWS/Azure、インフラ設計、DevOps、セキュリティ知識。"
    },
    {
        "title": "【東京/WEB面接可】製品セキュリティエンジニア（PSIRT）【本社】",
        "url": "https://example.com/it3",
        "description": "製品セキュリティ対応・PSIRTチーム業務。セキュリティ経験、脆弱性対応、インシデント対応、英語力。"
    },
    {
        "title": "【東京/WEB面接可】生成AI活用プラットフォーム開発エンジニア【AI戦略プロジェクトグループ】",
        "url": "https://example.com/it4",
        "description": "生成AI活用プラットフォームの開発。Python、機械学習、LLM、クラウド開発、API設計経験。"
    },
    {
        "title": "【東京/WEB面接可】社内業務DXを実現するためのSAP S/4 HANA技術者【本社・標準アプリケーション第一部】", 
        "url": "https://example.com/it5",
        "description": "SAP S/4 HANAによる基幹業務システム構築。SAP技術、ERP、データベース設計、業務分析経験。"
    }
]

def get_test_jobs_by_profile(industry: str, job_type: str):
    """
    プロフィールに応じてテスト用求人データを返す
    三菱電機の実際の職種分布に基づいてマッチング
    """
    industry_lower = industry.lower()
    job_type_lower = job_type.lower()
    
    # 防衛・宇宙系（高度技術）
    if any(keyword in industry_lower for keyword in ['防衛', '宇宙', '航空', 'defense', 'space']) or \
       any(keyword in job_type_lower for keyword in ['防衛', '宇宙', '航空', 'レーダ', 'ミサイル', '衛星']):
        return DEFENSE_SPACE_JOBS
    
    # 電力・エネルギー系エンジニア
    elif any(keyword in industry_lower for keyword in ['電力', '電気', 'エネルギー', 'power', 'energy']) or \
         any(keyword in job_type_lower for keyword in ['電力', '電気', '発電', '変電', '制御', '計装']):
        return POWER_ENGINEERING_JOBS
    
    # IT・デジタル系
    elif any(keyword in industry_lower for keyword in ['it', 'システム', 'デジタル', 'dx', 'ai']) or \
         any(keyword in job_type_lower for keyword in ['システム', 'it', 'ai', 'クラウド', 'dx', 'セキュリティ']):
        return IT_DIGITAL_JOBS
    
    # 製造・生産技術系
    elif any(keyword in industry_lower for keyword in ['製造', '生産', 'manufacturing']) or \
         any(keyword in job_type_lower for keyword in ['製造', '生産', '組立', '加工', '品質']):
        return MANUFACTURING_JOBS
    
    # ビジネス系（営業・企画・管理）
    elif any(keyword in job_type_lower for keyword in ['営業', '企画', '人事', '経理', '法務', 'マーケティング', '採用', 'コンサル', 'hr', '労務', 'リクルート', 'recruitment', 'consulting']):
        return BUSINESS_JOBS
    
    # デフォルトは電力エンジニア系（三菱電機の主力）
    else:
        return POWER_ENGINEERING_JOBS

# テスト用プロフィールセット（三菱電機の主要職種に対応）
TEST_PROFILES = [
    {
        "name": "電力システムエンジニア",
        "industry": "電力・エネルギー業界", 
        "job_type": "電力システム設計",
        "experience_years": "8"
    },
    {
        "name": "防衛システムエンジニア",
        "industry": "防衛・宇宙業界",
        "job_type": "レーダシステム開発", 
        "experience_years": "10"
    },
    {
        "name": "製造技術者",
        "industry": "製造業",
        "job_type": "生産技術",
        "experience_years": "6" 
    },
    {
        "name": "AIエンジニア",
        "industry": "IT業界",
        "job_type": "AI・機械学習",
        "experience_years": "5"
    },
    {
        "name": "海外営業",
        "industry": "電機業界",
        "job_type": "海外営業",
        "experience_years": "7"
    },
    {
        "name": "人事担当者",
        "industry": "製造業",
        "job_type": "人事・採用",
        "experience_years": "5"
    }
]
