# Phase 3：実装フェーズ

PoC・本格導入で開発する業務自動化スクリプトの置き場。

## ディレクトリ方針

```
phase3_implementation/
├── tax_office/           # 税理士事務所向け
│   ├── <業務スラッグ>/
│   │   ├── README.md     # 業務概要・運用手順・成果指標
│   │   ├── main.py       # 実行スクリプト（CLI または最小UI）
│   │   ├── prompts/      # LLM用プロンプト
│   │   ├── samples/      # 仮データ（実データはコミット禁止）
│   │   └── manual.md     # 非エンジニア向け操作マニュアル
│   └── ...
└── law_office/           # 弁護士事務所向け
    └── ...
```

## 実装規約

- **入力データに実情報を含めない。** `samples/` 配下は仮データのみ。実データは `input/`（gitignore済）で扱う。
- **エラーメッセージは日本語。** スタッフが原因を判別できる粒度で出す。
- **AI生成物には注記を付与。** 出力ファイルの先頭または末尾に `shared/disclaimers.md` の注記を組み込む。
- **依存は最小限。** 標準ライブラリ＋ `anthropic` SDK で書ける範囲を優先。複雑な連携は n8n / Make 側で組む。
- **セキュリティ。** APIキーは環境変数（`.env`）で管理し、リポジトリにコミットしない。

## 業務スラッグの命名例

- 税理士: `monthly-trial-balance` / `client-bulk-mail` / `tax-qa-draft` / `subsidy-app-draft`
- 弁護士: `contract-review` / `engagement-letter` / `case-law-summary` / `client-progress-report`
