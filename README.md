# aiforpro — 士業事務所 AI導入コンサル ワークスペース

税理士・弁護士事務所への成果報酬型AI導入コンサルを高速で回すための、テンプレート・ROI試算ツール・実装スクリプト置き場。

プロジェクトの背景・ビジネスモデル・ターゲット定義は **[CLAUDE.md](./CLAUDE.md)** を参照。

## ディレクトリ構成

```
.
├── CLAUDE.md                       # プロジェクト方針（Claude Code 起動時に必読）
├── phase1_proposal/                # 提案・営業フェーズの成果物
│   ├── hearing_sheets/             # 業務棚卸しヒアリングシート（税理士／弁護士）
│   ├── roi/                        # ROI試算モデル（Python + CSV）
│   └── differentiation_table.md    # 競合差別化比較表
├── phase2_analysis/                # 業務分析フェーズの成果物
│   └── automation_scoring_template.csv
├── phase3_implementation/          # 実装スクリプト（業種別）
│   ├── tax_office/                 # 税理士向け
│   └── law_office/                 # 弁護士向け
├── phase4_reporting/               # 成果測定・KPIレポート
│   └── kpi_dashboard_template.html
└── shared/                         # 全Phase共通
    └── disclaimers.md              # AI生成物への注記文言
```

## 進め方（Claude Codeセッション開始時）

1. `CLAUDE.md` の「優先タスクの進め方」に従い、本日のPhaseとタスクを確認する
2. 必要なインプット（ヒアリングメモ等）の有無を確認する
3. 成果物の形式（Markdown / HTML / Excel / Python）を合意する
4. 各Phaseディレクトリ配下にあるテンプレートをベースに作業する

## ROI試算ツールの使い方

```bash
# 入力CSVを編集してから実行
python phase1_proposal/roi/roi_calculator.py phase1_proposal/roi/roi_input_template.csv
```

## 法的注記

AIによる生成物は必ず士業有資格者の確認を経てクライアントに提供すること。
詳細は [shared/disclaimers.md](./shared/disclaimers.md) を参照。
