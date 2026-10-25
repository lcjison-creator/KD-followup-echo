"""When did post-discharge echocardiograms actually happen after an uncomplicated course? (descriptive; for the Methods
sentence on the routine follow-up schedule). Derivation cohort C1 (index admissions 2018-2024 without 2021), uncomplicated
course (in_max == 0, n = 2,839). One echocardiogram per child per day.

Run: python3 -I followup_visit_timing_2026-10-25.py   (from kd30/methods_checks; reads ../data)
Illness day = days after discharge + illness day at discharge, the latter known for children with a 1-30-day echo
(post30_illday_first - post30_day_first).
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] / "data"
c = pd.read_csv(ROOT / "output_kd_echo_surveillance_v4_1" / "cohort_C1_primary.csv", dtype={"index_enc": str})
u = c[c.in_max == 0].copy()
u["ill_at_dis"] = u.post30_illday_first - u.post30_day_first
print(f"uncomplicated children: {len(u)}; illness day at discharge (children with a 1-30-day echo, n = "
      f"{u.ill_at_dis.notna().sum()}): median {u.ill_at_dis.median():.0f} (IQR {u.ill_at_dis.quantile(.25):.0f}-"
      f"{u.ill_at_dis.quantile(.75):.0f})")

e = pd.read_parquet(ROOT / "echo_timeline.parquet", columns=["index_enc", "d_dis", "phase"])
e = e[e.index_enc.isin(u.index_enc) & e.phase.isin(["post30", "d31_90", "d91_365", "gt365"])].copy()
e = e.merge(u[["index_enc", "ill_at_dis"]], on="index_enc", how="left")
e["ill"] = e.d_dis + e.ill_at_dis
e["day"] = e.d_dis.round()
e = e.drop_duplicates(["index_enc", "day"]).sort_values(["index_enc", "d_dis"])
e["k"] = e.groupby("index_enc").cumcount() + 1
print(f"post-discharge echocardiograms (child-days): {len(e)} in {e.index_enc.nunique()} children\n")


def q(s):
    s = s.dropna()
    return f"{s.median():.0f} ({s.quantile(.25):.0f}-{s.quantile(.75):.0f})" if len(s) else "-"


rows = [{"post-discharge echo": k, "children": len(g), "days after discharge, median (IQR)": q(g.d_dis),
         "illness day, median (IQR)": q(g.ill), "illness day known": int(g.ill.notna().sum())}
        for k, g in e.groupby("k") if k <= 5]
print(pd.DataFrame(rows).to_string(index=False))

print("\nAll post-discharge echocardiograms by days after discharge:")
bins = [0, 7, 14, 21, 28, 42, 56, 70, 98, 120, 150, 180, 240, 300, 365, 450, 730, 100000]
print(pd.cut(e.d_dis, bins).value_counts().sort_index().to_string())
