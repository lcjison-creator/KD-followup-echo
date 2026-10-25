"""Build comparison_extraction_v2.csv from v1 plus the full texts received on 25 Oct 2026, and check every number against
the extracted PDF text.

Run: python3 -I build_comparison_v2.py <scratchpad dir>
The scratchpad holds one folder per PDF (pdf_wang2022, pdf_matsuoka2020, pdf_tuohy2001), each with text.txt from
pdftotext -layout. Each new row carries evidence strings that must occur in that text (after removing the
"Journal Pre-proof" watermark fragments and collapsing white space); the script stops if any is missing.
Lee 2005 is taken from the PubMed abstract (PMID 16640036); its full text was not available.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = Path(sys.argv[1])
WATERMARK = {"of", "ro", "-p", "re", "lP", "na", "ur", "Jo", "f", "oo", "pr", "e-", "P", "r", "o", "-", "pr", "-     pr"}


def norm_text(path):
    lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip() not in WATERMARK]
    return re.sub(r"\s+", " ", " ".join(lines))


# both the layout text (tables) and the reading-order text (two-column prose; pdftotext without -layout) are searched
TEXT = {k: norm_text(SP / f"pdf_{k}" / "text.txt") + " || " + norm_text(SP / f"pdf_{k}" / "text_raw.txt")
        for k in ["wang2022", "matsuoka2020", "tuohy2001"]}

FIELDS = ["study", "journal", "doi", "centers", "country", "z_system", "baseline_definition", "window_group", "window_timing",
          "outcome", "events", "n", "source_location", "status", "note"]

WANG = dict(study="Wang 2022", journal="J Pediatr 2022;244:133-138.e1", doi="10.1016/j.jpeds.2021.11.022", centers="1",
            country="Japan (Tokyo)",
            z_system="Kobayashi 2016 (LMS, Japanese reference); Zmax = larger of proximal RCA and proximal LAD",
            status="checked from full text (accepted manuscript PDF supplied 25 Oct 2026)")
MATS = dict(study="Matsuoka 2020", journal="J Pediatr 2020;227:224-230.e3", doi="10.1016/j.jpeds.2020.08.032", centers="1",
            country="Japan (Fukuoka)", z_system="Kobayashi 2016 (LMS, Japanese reference); Zmax of four branches",
            status="checked from full text (accepted manuscript PDF supplied 25 Oct 2026)")
TUOHY = dict(study="Tuohy 2001", journal="Am J Cardiol 2001;88:328-330", doi="10.1016/s0002-9149(01)01655-1", centers="3",
             country="USA (Salt Lake City; Chicago; Houston)",
             z_system="no Z score: ectasia = above de Zorzi 1998 normal values; aneurysm = 1.5 x adjacent segment; perivascular echogenicity counted",
             status="checked from full text (PDF supplied 25 Oct 2026)")

NEW_ROWS = [
    (dict(WANG, baseline_definition="Zmax < 2.5 within 9 days of treatment initiation (n = 386; 350 with Zmax < 2)",
          window_group="first follow-up", window_timing="1 month after treatment initiation (days 20-50)",
          outcome="aneurysm (Zmax >= 2.5)", events=4, n=376,
          source_location="Table 3, 1-month column: patients 11 (8.68), 14 (3.03), 15 (14.10), 16 (12.64); Table 2 (n = 376)",
          note="all 4 had Zmax < 2 within 9 days; patients 11, 15 and 16 (Zmax >= 5) were first seen at the 2-week echo (done in 135)"),
     "wang2022", ["8.68", "3.03", "14.10", "12.64", "376 (97.4%) at one", "detected CALs in nine patients, including three (0.8%) with coronary aneurysms"]),
    (dict(WANG, baseline_definition="Zmax < 2.5 within 9 days of treatment initiation (n = 386)",
          window_group="first follow-up", window_timing="1 month after treatment initiation (days 20-50)",
          outcome="any involvement (Zmax >= 2)", events=9, n=376,
          source_location="Results p9 \"nine (2.4%) ... had Zmax >= 2 at one month\"; Table 2 (Zmax < 2 in 367 of 376)",
          note="3 of the 9 already had Zmax 2.0-2.4 within 9 days (patients 3, 9, 10)"),
     "wang2022", ["nine (2.4%), six (1.6%), eight (2.4%), and one (0.4%) patient had Zmax ≥ 2 at one", "367 (97.6)"]),
    (dict(WANG, baseline_definition="Zmax < 2 at the 1-month echo (n = 367)", window_group="late",
          window_timing="2 months (days 50-120) to 5 years after treatment initiation",
          outcome="any involvement (Zmax >= 2) first documented after a normal 1-month echo", events=7, n=367,
          source_location="Results p10 \"Three and four patients had CALs first documented at two months and one year, respectively, despite having normal Zmax at one month\"; Table 3",
          note="denominator = all with Zmax < 2 at 1 month; how many of them were re-imaged is not reported; none needed a change in management; 5 resolved, 2 lost"),
     "wang2022", ["Three and four patients had CALs first documented at two months and one year, respectively, despite having normal Zmax at one month", "367 (97.6)"]),
    (dict(WANG, baseline_definition="Zmax < 2 at the 1-month echo (n = 367)", window_group="late",
          window_timing="2 months to 5 years after treatment initiation", outcome="aneurysm (Zmax >= 2.5)", events=1, n=367,
          source_location="Table 3: patient 8, Zmax 0.63 at 1 month and 3.58 at 1 year (no later echo)",
          note="the other 6 late findings were Zmax 2.14-2.41"),
     "wang2022", ["3.58", "0.63"]),
    (dict(MATS, baseline_definition="pre-treatment Zmax <= 2.0 in IVIG responders (single or repeated infusions; complete KD; no rescue therapy)",
          window_group="first follow-up", window_timing="4 weeks after onset", outcome="aneurysm (Zmax >= 2.5)", events=4, n=235,
          source_location="Abstract; Results p5-6; Table II (pre-treatment Zmax > 2.0 in 90 of 325); Table IV patients 2, 5, 8, 9 (pre-treatment Zmax 1.37, 1.35, 1.99, 0.96)",
          note="the 4 were first seen on illness days 7-16 (likely before or around discharge); all small (Zmax 2.58-3.98 at 4 weeks); normal by 2-8 months; with a <= 2.5 cut-off 4/285 (Table VII groups C and D)"),
     "matsuoka2020", ["> 2.0, n = 90", "> 2.5, n = 40", "Four single-dose IVIG-responders developed CAA although they had pre-treatment Zmax of <2.0", "n = 281"]),
    (dict(MATS, baseline_definition="no aneurysm at 4 weeks (n = 312)", window_group="late",
          window_timing="after 4 weeks, follow-up to 24 months", outcome="new aneurysm (Zmax >= 2.5)", events=0, n=312,
          source_location="Results p4 \"No patient was newly diagnosed with CAA after the 4-week time-point\"; p5 \"No patients died or dropped out\"",
          note="echo schedule after 4-6 weeks not stated"),
     "matsuoka2020", ["No patient was newly diagnosed with CAA after the 4-week time-point", "No patients died or dropped out of the study"]),
    (dict(TUOHY, baseline_definition="normal initial echocardiogram (mean day 10 +/- 12, median day 6 after onset)",
          window_group="first follow-up", window_timing="1-2 months after onset (new findings between 1 and 8 weeks)",
          outcome="new abnormality (aneurysm or ectasia)", events=10, n=277,
          source_location="p329 \"Of the remaining 277 patients, 267 had normal echocardiograms at 1- to 2-month follow-up. The remaining 10 patients (4%) ... (7 aneurysms and 3 ectasia)\"",
          note="125 of 402 with a normal initial echo were lost to follow-up; inclusion required echoes at presentation, 1-2 months and >5 months; 1984-2000"),
     "tuohy2001", ["Of the remaining 277 patients, 267 had normal echocardiograms at 1- to 2-month follow-up", "(7 aneurysms and 3 ectasia)", "125 were lost to follow-up"]),
    (dict(TUOHY, baseline_definition="normal initial echocardiogram (mean day 10, median day 6)", window_group="first follow-up",
          window_timing="1-2 months after onset", outcome="new aneurysm (1.5 x adjacent segment)", events=7, n=277,
          source_location="p329 \"(7 aneurysms and 3 ectasia)\"", note="aneurysm defined by shape, not Z score"),
     "tuohy2001", ["(7 aneurysms and 3 ectasia)"]),
    (dict(TUOHY, baseline_definition="normal echocardiogram at 1-2 months (n = 329: 267 normal throughout and 62 resolved)",
          window_group="late", window_timing="> 5 months after onset", outcome="any abnormality", events=0, n=217,
          source_location="p329 \"Of the total 329 patients ... 217 patients underwent further echocardiographic evaluation >5 months ... remained normal\"",
          note="112 of the 329 had no later echo"),
     "tuohy2001", ["Of the total 329 pa", "217 patients underwent further", "For all 217 patients, the study re"]),
]

LEE = dict(study="Lee 2005", journal="Acta Paediatr Taiwan 2005;46:346-351", doi="", centers="1", country="Taiwan (Kaohsiung)",
           z_system="not stated in abstract", baseline_definition="normal echocardiogram at 1-2 months after onset",
           window_group="late", window_timing="beyond 2 months (follow-up to 2 years)", outcome="any abnormality", events=0, n="",
           source_location="PubMed abstract (PMID 16640036) \"No patient who had normal echocardiographic findings at 1-2 months developed subsequent abnormalities\"",
           status="abstract only (full text not obtained)",
           note="denominator not reported in the abstract; 120 children with >= 3 echoes (admission, 1-2 months, > 2 months); 67 normal at admission; abnormalities first documented at a mean of 13 days (3-37)")

missing = []
for row, key, evidence in NEW_ROWS:
    for ev in evidence:
        if re.sub(r"\s+", " ", ev) not in TEXT[key]:
            missing.append((row["study"], ev))
if missing:
    for m in missing:
        print("NOT FOUND:", m)
    sys.exit("evidence check failed")

with open(HERE / "comparison_extraction_v1.csv", newline="", encoding="utf-8") as fh:
    v1 = list(csv.DictReader(fh))
kept = [r for r in v1 if r["study"] not in {"Wang 2022", "Matsuoka 2020", "Tuohy 2001", "Lee 2005"}]
rows = kept + [r for r, _, _ in NEW_ROWS] + [LEE]
with open(HERE / "comparison_extraction_v2.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

print(f"evidence strings checked: {sum(len(e) for _, _, e in NEW_ROWS)}; all found")
print(f"rows: kept from v1 {len(kept)}; new {len(NEW_ROWS) + 1}; total {len(rows)}")
for r in rows:
    ev, n = r["events"], r["n"]
    pct = f"{100 * int(ev) / int(n):.2f}%" if str(n).strip() else "n/a"
    print(f"  {r['study']:<17} {r['window_group']:<15} {r['outcome'][:55]:<55} {ev}/{n or '?'} ({pct})")
