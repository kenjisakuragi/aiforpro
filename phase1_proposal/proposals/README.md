# 提案書テンプレート（業種別）

| ファイル | 用途 |
|---|---|
| `tax_office_proposal.md` | 税理士事務所向け 業務効率化提案書（15スライド構成） |
| `law_office_proposal.md` | 弁護士事務所向け 業務効率化提案書（15スライド構成） |

## 完成版デモ

実際のペルソナで全数値を埋め切り、Marp 形式でスライド化した実例：
- `demo/tax_office_slides.md` ── 神田税理士事務所（仮）／15スライド
- `demo/law_office_slides.md` ── 丸の内総合法律事務所（仮）／15スライド
- 出力方法・架空ペルソナの設定は [demo/README.md](./demo/README.md) を参照

## 構成方針

- H2見出し（`## Slide N`）が1スライドに対応
- `{{ ... }}` プレースホルダはヒアリング・ROI試算結果から差替え
- Markdown のまま [Marp](https://marp.app/) でPDF/PPTX化、または Google Slides / PowerPoint に転記可能

## 差替え元データ

```
hearing_sheets/<industry>_hearing.md  → Slide 4（ヒアリング所見）
phase2_analysis/automation_scoring_template.csv → Slide 5（4象限マップ）
roi/roi_input_template.csv            → Slide 6（PoC候補）
roi/roi_calculator.py の出力          → Slide 7（ROI数値）
differentiation_table.md               → Slide 13（差別化）
shared/disclaimers.md                  → 付録A（注記文言）
```

## 提案前チェック（共通）

- [ ] 表紙の事務所名・代表名に誤字がないか
- [ ] ROI試算値が `roi_calculator.py` の出力と一致しているか
- [ ] 「AIドラフト・要確認」の注記が入っているか
- [ ] 本業（TBSテレビ）との利益相反がないか
- [ ] 提案資料中に他事務所の固有情報が混入していないか

## 弁護士事務所向け 追加チェック

- [ ] 利益相反チェックを完了したか
- [ ] 配布資料の回収・破棄方針を冒頭で口頭説明する準備ができているか
- [ ] 使用LLMの学習利用ポリシーの最新条項を別添資料として用意したか
