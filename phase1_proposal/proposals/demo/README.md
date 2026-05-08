# Demo：完成版 提案スライド（Marp）

架空のペルソナを使って、実数値まで埋め切った Phase 1 提案スライドの実例。
本番提案では、固有名詞・数値を御所のヒアリング結果に差し替えて使用する。

## ファイル構成

| ファイル | 内容 |
|---|---|
| `tax_office_slides.md` | 税理士事務所（神田税理士事務所・仮）向け 15スライド |
| `law_office_slides.md` | 弁護士事務所（丸の内総合法律事務所・仮）向け 15スライド |
| `roi_input_tax.csv` | 税理士向けスライドの ROI 試算入力 |
| `roi_input_law.csv` | 弁護士向けスライドの ROI 試算入力 |
| `roi_output_tax.md` | 税理士向け ROI 試算レポート（提案書付録の根拠） |
| `roi_output_law.md` | 弁護士向け ROI 試算レポート（提案書付録の根拠） |

## 架空ペルソナの設定

### 神田税理士事務所（仮）
- 所長：田中太郎 先生
- スタッフ8名（税理士2／科目合格者2／補助4）
- 顧問先150社／平均月顧問料5万円
- 主要痛点：月次試算表チェック・税務相談メール初稿
- ヒアリング日：2026/04/20、提案日：2026/05/15

### 丸の内総合法律事務所（仮）
- 代表：鈴木一郎 先生
- パートナー2／アソシエイト3／パラリーガル3
- 取扱：企業法務中心（顧問先30社）
- 主要痛点：契約書レビュー初稿・判例調査サマリ
- ヒアリング日：2026/04/22、提案日：2026/05/16

## 試算結果サマリ（架空ケース）

| 指標 | 税理士（神田事務所） | 弁護士（丸の内総合） |
|---|---:|---:|
| 月間削減時間合計 | 65.1 時間 | 47.8 時間 |
| 年間削減コスト | ¥3,524,400 | ¥4,538,400 |
| 年間純便益 | ¥1,824,400 | ¥2,518,400 |
| 成果報酬合計（初年度・40%） | ¥1,409,760 | ¥1,815,360 |

## スライドの出力方法（Marp）

### 1. 環境
Node.js が入っていれば追加インストール不要。`npx` 経由で Marp CLI を使う。

### 2. PDF / PPTX / HTML 出力

```bash
# HTML（ブラウザで確認用）
npx --yes @marp-team/marp-cli@latest phase1_proposal/proposals/demo/tax_office_slides.md --html

# PDF（クライアント送付用）
npx --yes @marp-team/marp-cli@latest phase1_proposal/proposals/demo/tax_office_slides.md --pdf

# PowerPoint（編集を引き継ぐ場合）
npx --yes @marp-team/marp-cli@latest phase1_proposal/proposals/demo/tax_office_slides.md --pptx
```

弁護士向けは `tax_office_slides.md` を `law_office_slides.md` に置換。

### 3. 一括出力（両方のスライドをPDF化）

```bash
for f in tax_office_slides.md law_office_slides.md; do
  npx --yes @marp-team/marp-cli@latest \
    "phase1_proposal/proposals/demo/$f" --pdf
done
```

出力ファイル（`*.html` / `*.pdf` / `*.pptx`）は `.gitignore` 済み。元の `.md` のみリポジトリ管理。

## ROI数値の再生成方法

CSV を編集してから、ROI計算スクリプトを実行する：

```bash
# 税理士
python3 phase1_proposal/roi/roi_calculator.py \
  phase1_proposal/proposals/demo/roi_input_tax.csv \
  --fee-rate 0.4 \
  --out phase1_proposal/proposals/demo/roi_output_tax.md

# 弁護士
python3 phase1_proposal/roi/roi_calculator.py \
  phase1_proposal/proposals/demo/roi_input_law.csv \
  --fee-rate 0.4 \
  --out phase1_proposal/proposals/demo/roi_output_law.md
```

CSV の値を変えてからスライド側の数字も合わせて差替えること（手動）。

## 提案前チェックリスト（共通）

- [ ] 表紙・体制図の固有名詞を本物の事務所名に差替えた
- [ ] ROI試算値が `roi_output_*.md` の最新値と一致している
- [ ] 「AIドラフト・要確認」の注記が冒頭または末尾に入っている
- [ ] 本業（TBSテレビ）との利益相反がないか確認した
- [ ] 配布資料に他事務所の固有情報が混入していない
- [ ] 提案者の連絡先（メール／電話）を実値に差替えた

### 弁護士事務所向け 追加チェック
- [ ] 利益相反チェックを完了した
- [ ] 配布資料の回収・破棄方針を冒頭で口頭説明する準備ができている
- [ ] 使用LLM（Claude API等）の学習利用ポリシーの最新条項を別添資料として用意した
