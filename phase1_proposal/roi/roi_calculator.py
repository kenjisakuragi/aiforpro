#!/usr/bin/env python3
"""ROI試算ツール（成果報酬型コンサル提案用）

入力CSV（roi_input_template.csv と同じ列構成）を読み込み、
業務単位の年間削減コスト・成果報酬額・回収期間を試算して
Markdown 表＋集計サマリを標準出力に出す。

使い方:
    python roi_calculator.py path/to/input.csv [--fee-rate 0.4] [--out result.md]

列定義（CSVヘッダ・固定）:
    業務名 / 現状の月間所要時間_h / 削減見込み率_pct / 担当者時給_円 /
    自動化後の月間運用工数_h / 初期構築費_円 / 月額運用費_円
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = [
    "業務名",
    "現状の月間所要時間_h",
    "削減見込み率_pct",
    "担当者時給_円",
    "自動化後の月間運用工数_h",
    "初期構築費_円",
    "月額運用費_円",
]


@dataclass
class TaskROI:
    name: str
    monthly_saved_hours: float
    monthly_saved_cost: int
    annual_saved_cost: int
    annual_running_cost: int
    initial_cost: int
    annual_net_benefit: int
    annual_consulting_fee: int
    payback_months: float | None


def parse_row(row: dict[str, str]) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for col in REQUIRED_COLUMNS[1:]:
        raw = (row.get(col) or "").strip()
        if raw == "":
            raise ValueError(f"列『{col}』が空欄です（業務名: {row.get('業務名', '?')}）")
        try:
            parsed[col] = float(raw)
        except ValueError as exc:
            raise ValueError(
                f"列『{col}』の値『{raw}』を数値に変換できません（業務名: {row.get('業務名', '?')}）"
            ) from exc
    return parsed


def compute_roi(row: dict[str, str], fee_rate: float) -> TaskROI:
    nums = parse_row(row)
    current_hours = nums["現状の月間所要時間_h"]
    reduction_rate = nums["削減見込み率_pct"] / 100.0
    hourly = nums["担当者時給_円"]
    post_ops_hours = nums["自動化後の月間運用工数_h"]
    initial_cost = int(nums["初期構築費_円"])
    monthly_running = int(nums["月額運用費_円"])

    monthly_saved_hours = max(current_hours * reduction_rate - post_ops_hours, 0.0)
    monthly_saved_cost = int(monthly_saved_hours * hourly)
    annual_saved_cost = monthly_saved_cost * 12
    annual_running_cost = monthly_running * 12
    annual_net_benefit = annual_saved_cost - annual_running_cost - initial_cost
    annual_consulting_fee = int(annual_saved_cost * fee_rate)

    monthly_net = monthly_saved_cost - monthly_running
    payback_months = (
        round(initial_cost / monthly_net, 1) if monthly_net > 0 else None
    )

    return TaskROI(
        name=row["業務名"].strip(),
        monthly_saved_hours=round(monthly_saved_hours, 1),
        monthly_saved_cost=monthly_saved_cost,
        annual_saved_cost=annual_saved_cost,
        annual_running_cost=annual_running_cost,
        initial_cost=initial_cost,
        annual_net_benefit=annual_net_benefit,
        annual_consulting_fee=annual_consulting_fee,
        payback_months=payback_months,
    )


def yen(value: int) -> str:
    return f"{value:,}円"


def render_markdown(rows: list[TaskROI], fee_rate: float) -> str:
    lines: list[str] = []
    lines.append("# ROI試算レポート（AI導入コンサル）\n")
    lines.append(f"成果報酬比率: **{fee_rate * 100:.0f}%**（年間削減コストに対する初年度報酬）\n")
    lines.append("")
    lines.append(
        "| # | 業務名 | 月間削減時間 | 月間削減コスト | 年間削減コスト | 年間運用費 | 初期構築費 | 年間純便益 | 成果報酬（初年度） | 投資回収 |"
    )
    lines.append(
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"
    )
    for i, r in enumerate(rows, 1):
        payback = f"{r.payback_months}ヶ月" if r.payback_months is not None else "—"
        lines.append(
            "| {n} | {name} | {hours}h | {ms} | {ys} | {yr} | {ic} | {nb} | {fee} | {pb} |".format(
                n=i,
                name=r.name,
                hours=r.monthly_saved_hours,
                ms=yen(r.monthly_saved_cost),
                ys=yen(r.annual_saved_cost),
                yr=yen(r.annual_running_cost),
                ic=yen(r.initial_cost),
                nb=yen(r.annual_net_benefit),
                fee=yen(r.annual_consulting_fee),
                pb=payback,
            )
        )

    total_hours = sum(r.monthly_saved_hours for r in rows)
    total_annual_saved = sum(r.annual_saved_cost for r in rows)
    total_annual_net = sum(r.annual_net_benefit for r in rows)
    total_fee = sum(r.annual_consulting_fee for r in rows)

    lines.append("")
    lines.append("## 集計サマリ\n")
    lines.append(f"- 月間削減時間合計: **{round(total_hours, 1)}時間**")
    lines.append(f"- 年間削減コスト合計: **{yen(total_annual_saved)}**")
    lines.append(f"- 年間純便益（初期費・運用費差引後）: **{yen(total_annual_net)}**")
    lines.append(f"- 成果報酬合計（初年度・{fee_rate * 100:.0f}%）: **{yen(total_fee)}**")
    lines.append("")
    lines.append("> ※AIドラフト・要確認。各業務の削減見込み率はヒアリング値ベース。")
    lines.append("> 実測はPoC期間（3ヶ月）の前後比較にて確定する。")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="成果報酬型AIコンサル ROI試算ツール")
    parser.add_argument("input_csv", help="入力CSVファイル（roi_input_template.csv 参照）")
    parser.add_argument(
        "--fee-rate",
        type=float,
        default=0.4,
        help="成果報酬比率（年間削減コストに対する割合、0〜1）。既定 0.4",
    )
    parser.add_argument("--out", help="出力Markdownファイル（省略時は標準出力）")
    args = parser.parse_args()

    if not 0 < args.fee_rate <= 1:
        print("エラー: --fee-rate は 0 より大きく 1 以下で指定してください。", file=sys.stderr)
        return 2

    csv_path = Path(args.input_csv)
    if not csv_path.exists():
        print(f"エラー: 入力CSVが見つかりません: {csv_path}", file=sys.stderr)
        return 2

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or any(c not in reader.fieldnames for c in REQUIRED_COLUMNS):
            print(
                "エラー: CSVヘッダが不正です。必要列: " + ", ".join(REQUIRED_COLUMNS),
                file=sys.stderr,
            )
            return 2
        rows: list[TaskROI] = []
        for line_no, row in enumerate(reader, start=2):
            if not (row.get("業務名") or "").strip():
                continue
            try:
                rows.append(compute_roi(row, args.fee_rate))
            except ValueError as exc:
                print(f"エラー（{line_no}行目）: {exc}", file=sys.stderr)
                return 2

    if not rows:
        print("エラー: 試算対象の業務が0件でした。CSVの中身を確認してください。", file=sys.stderr)
        return 2

    output = render_markdown(rows, args.fee_rate)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"出力しました: {args.out}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
