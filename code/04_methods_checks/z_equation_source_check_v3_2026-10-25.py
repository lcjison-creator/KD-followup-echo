"""Which published coronary Z-score equation reproduces the Z values reported by the Wuhan Children's Hospital echo laboratory?
Version 3: adds Dallaire F, Dahdah N. New equations and a critical appraisal of coronary artery Z scores in healthy
children. J Am Soc Echocardiogr 2011;24:60-74 (doi:10.1016/j.echo.2010.10.004), Table 5 (p65), equation on p63:
Z = [D - (a + b sqrt(BSA))] / (aSE + bSE sqrt(BSA)), BSA by Haycock (p61). Version 2 added the Beijing Children's
Hospital equations (all seven printed models), a test of which functional form the reported values follow (section 5b)
and a clinical illustration (section 6).

Run: python3 -I z_equation_source_check_v3_2026-10-25.py   (from kd30/methods_checks; reads ../data)
Inputs: z_pairs.parquet (diameter D in mm, reported Z, height H in cm, weight W in kg, Stevenson BSA, year; text-extracted
2018-2026 reports) and lab_z_equations_fit.csv (equation reconstructed from these pairs on 2026-09-30).

Candidates
- Beijing Children's Hospital (Zheng L, Du ZD, Jin LZ, et al. Zhonghua Er Ke Za Zhi 2013;51:371-6,
  doi:10.3760/cma.j.issn.0578-1310.2013.05.011). Selected model (text p373, Tables 4, 5 and 7):
  ln(D) = alpha + beta ln(BSA); Z = (ln D - alpha - beta ln BSA) / sqrt(MSE).
  LCA (left main) 1.119, 0.357, MSE 0.008; LAD 0.915, 0.360, MSE 0.012; RCA 1.003, 0.360, MSE 0.011.
  BSA was computed by the ultrasound machine from height and weight (formula not stated), so four BSA formulas are tried.
  MSE is printed to three decimals, so sqrt(MSE) is uncertain by up to about 6% (LCA).
- Shenzhen Children's Hospital multicenter (Fan SM et al. BMC Pediatr 2021;21:429, doi:10.1186/s12887-021-02877-9):
  ln(D) = a + b ln(BSA), Z = (ln D - fitted) / RSE; Haycock and Stevenson versions.
- Functional forms fitted freely to the reported pairs (section 5b): the best that any published equation of each form
  could achieve, including the ln D = alpha + beta ln BSA form shared by Beijing and Shenzhen.
A reported Z is "reproduced" when |Z_equation - Z_reported| <= 0.1.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
zp = pd.read_parquet(ROOT / "data" / "z_pairs.parquet").dropna(subset=["D", "Z", "H", "W", "BSA_ste"]).copy()
fit = pd.read_csv(ROOT / "data" / "lab_z_equations_fit.csv").set_index("vessel")

BSA = {"Stevenson": zp["BSA_ste"],
       "Haycock": 0.024265 * zp["H"] ** 0.3964 * zp["W"] ** 0.5378,
       "DuBois": 0.007184 * zp["H"] ** 0.725 * zp["W"] ** 0.425,
       "Mosteller": np.sqrt(zp["H"] * zp["W"] / 3600)}
for k, v in BSA.items():
    zp["BSA_" + k] = v

f = fit.loc[zp["vessel"]].reset_index(drop=True)
zp = zp.reset_index(drop=True)
zp["Z_lab"] = (zp.D - (f.a + f.b_sqrtBSA * np.sqrt(zp.BSA_Stevenson) + f.c_BSA * zp.BSA_Stevenson)) / f.SD_mm

BJ = {"LMCA": (1.119, 0.357, 0.008), "LAD": (0.915, 0.360, 0.012), "RCA": (1.003, 0.360, 0.011)}
SZ = {"Haycock": {"LMCA": (1.0084, 0.3740, 0.115), "LAD": (0.8063, 0.3697, 0.119), "RCA": (0.8040, 0.3291, 0.150)},
      "Stevenson": {"LMCA": (1.0042, 0.3494, 0.114), "LAD": (0.8013, 0.3448, 0.120), "RCA": (0.8107, 0.3098, 0.150)}}

cols = {"Z_lab": "lab equation (a + b sqrt(BSA) + c BSA, Stevenson)"}
for k in BSA:
    a, b, m = (zp.vessel.map({v: c[i] for v, c in BJ.items()}) for i in range(3))
    zp["Z_BJ_" + k] = (np.log(zp.D) - a - b * np.log(zp["BSA_" + k])) / np.sqrt(m)
    cols["Z_BJ_" + k] = f"Beijing 2013, {k} BSA"
for k, coef in SZ.items():
    a, b, s = (zp.vessel.map({v: c[i] for v, c in coef.items()}) for i in range(3))
    zp["Z_SZ_" + k] = (np.log(zp.D) - a - b * np.log(zp["BSA_" + k])) / s
    cols["Z_SZ_" + k] = f"Shenzhen 2021, {k} BSA"

# Dallaire & Dahdah 2011 (Table 5): Z = [D - (a + b sqrt(BSA))] / (aSE + bSE sqrt(BSA)), Haycock BSA in the paper
DAL = {"LMCA": (-0.1817, 2.9238, 0.1801, 0.2530), "LAD": (-0.1502, 2.2672, 0.1709, 0.2293),
       "RCA": (-0.3039, 2.7521, 0.1626, 0.2881),  # proximal RCA
       "RCA_mid": (-0.3060, 2.4078, 0.1324, 0.3259), "RCA_distal": (-0.3185, 2.3295, 0.1099, 0.3198)}
SEGKEY = zp.vessel.where(zp.vessel != "RCA", np.where(zp.seg.isin(["中段", "中远段"]), "RCA_mid",
                                                      np.where(zp.seg.isin(["远段", "远端"]), "RCA_distal", "RCA")))
for k in BSA:
    for label, key in [("proximal RCA equation for all RCA values", zp.vessel), ("RCA segment from the report", SEGKEY)]:
        a, b, ase, bse = (key.map({v: c[i] for v, c in DAL.items()}) for i in range(4))
        r = np.sqrt(zp["BSA_" + k])
        col = f"Z_DAL_{k}" + ("" if label.startswith("proximal") else "_seg")
        zp[col] = (zp.D - (a + b * r)) / (ase + bse * r)
        if label.startswith("proximal") or k in ("Haycock", "Stevenson"):
            cols[col] = f"Dallaire 2011, {k} BSA" + ("" if label.startswith("proximal") else ", RCA by segment")

def summary(d):
    rows = []
    for c, label in cols.items():
        e = (d[c] - d.Z).abs()
        rows.append({"equation": label, "within 0.1 (%)": round(100 * (e <= 0.1).mean(), 1),
                     "within 0.25 (%)": round(100 * (e <= 0.25).mean(), 1), "within 0.5 (%)": round(100 * (e <= 0.5).mean(), 1),
                     "median |diff|": round(e.median(), 3)})
    return pd.DataFrame(rows).set_index("equation")

pd.set_option("display.width", 200)
print(f"Measurements with diameter, reported Z, height and weight: {len(zp)} ({zp.vessel.value_counts().to_dict()}); "
      f"years {zp.yr.min()}-{zp.yr.max()}")
print("\n1. ALL MEASUREMENTS")
print(summary(zp).to_string())
core = zp[zp.Z.abs() <= 5]
print(f"\n2. REPORTED |Z| <= 5 (n = {len(core)}; the range that decides normal, dilation and small aneurysm)")
print(summary(core).to_string())

print("\n3. BY YEAR: % reproduced within 0.1")
t = pd.DataFrame({"n": zp.groupby("yr").size()})
for c, lab in [("Z_lab", "lab"), ("Z_BJ_Stevenson", "Beijing Ste"), ("Z_BJ_Haycock", "Beijing Hay"),
               ("Z_BJ_DuBois", "Beijing DuB"), ("Z_BJ_Mosteller", "Beijing Mos"), ("Z_SZ_Stevenson", "Shenzhen Ste"),
               ("Z_SZ_Haycock", "Shenzhen Hay"), ("Z_DAL_Haycock", "Dallaire Hay"), ("Z_DAL_Stevenson", "Dallaire Ste")]:
    t[lab] = ((zp[c] - zp.Z).abs() <= 0.1).groupby(zp.yr).mean().mul(100).round(1)
print(t.to_string())

miss = zp[(zp.Z_lab - zp.Z).abs() > 0.1]
bj_any = pd.concat([(miss["Z_BJ_" + k] - miss.Z).abs() <= 0.1 for k in BSA], axis=1).any(axis=1)
sz_any = pd.concat([(miss["Z_SZ_" + k] - miss.Z).abs() <= 0.1 for k in SZ], axis=1).any(axis=1)
dal_any = pd.concat([(miss[c] - miss.Z).abs() <= 0.1 for c in miss.columns if c.startswith("Z_DAL_")], axis=1).any(axis=1)
print(f"\n4. NOT REPRODUCED BY THE LAB EQUATION: {len(miss)}; reproduced by Beijing (any BSA) {int(bj_any.sum())}; "
      f"by Shenzhen (either BSA) {int(sz_any.sum())}; by Dallaire (any BSA, either RCA rule) {int(dal_any.sum())}; "
      f"by none {int((~bj_any & ~sz_any & ~dal_any).sum())}")

print("\n4b. DALLAIRE Z AGAINST REPORTED Z (Haycock BSA, RCA by segment), |reported Z| <= 5, by vessel")
core_d = zp[zp.Z.abs() <= 5]
for v, g in core_d.groupby("vessel"):
    s, i = np.polyfit(g.Z, g.Z_DAL_Haycock_seg, 1)
    e = (g.Z_DAL_Haycock_seg - g.Z).abs()
    print(f"   {v}: within 0.1 {100 * (e <= 0.1).mean():.1f}%; median |diff| {e.median():.2f}; "
          f"Z_Dallaire = {i:+.2f} + {s:.2f} x Z_reported; r = {np.corrcoef(g.Z, g.Z_DAL_Haycock_seg)[0, 1]:.3f}")

print("\n5. BEIJING Z AGAINST REPORTED Z (Stevenson BSA), |reported Z| <= 5: least-squares line and correlation")
for v, g in core.groupby("vessel"):
    s, i = np.polyfit(g.Z, g.Z_BJ_Stevenson, 1)
    print(f"   {v}: Z_Beijing = {i:+.2f} + {s:.2f} x Z_reported; r = {np.corrcoef(g.Z, g.Z_BJ_Stevenson)[0, 1]:.3f}; "
          f"n = {len(g)}")

print("\n5b. WHICH FUNCTIONAL FORM DO THE REPORTED VALUES FOLLOW? Every form below is fitted freely to the reported pairs")
print("    (|reported Z| <= 5; least squares of reported Z on the form's terms, refitted 12 times on the 85% of pairs")
print("    closest to the current fit so that transcription errors do not pull the fit), so its result approximates the")
print("    best that any published equation of that form could achieve. % of pairs reproduced within 0.1:")
FORMS = {
    "D = a + b sqrt(BSA) + c BSA, constant SD (lab reconstruction)": lambda d, B: [d.D, np.sqrt(B), B],
    "D = a + b sqrt(BSA), constant SD": lambda d, B: [d.D, np.sqrt(B)],
    "D = a + b BSA + c BSA^2 + d BSA^3, constant SD (Zhang 2014 Shanghai form)": lambda d, B: [d.D, B, B ** 2, B ** 3],
    "ln D = a + b ln BSA, constant SD (Beijing 2013 and Shenzhen 2021 form)": lambda d, B: [np.log(d.D), np.log(B)],
    "ln D = a + b BSA + c BSA^2 + d BSA^3, constant SD (Pettersen 2008 form)": lambda d, B: [np.log(d.D), B, B ** 2, B ** 3],
}
rows = []
for label, terms in FORMS.items():
    for k in ["Stevenson", "Haycock"]:
        pred = pd.Series(np.nan, index=zp.index)
        for v, g in zp.groupby("vessel"):
            fitg = g[g.Z.abs() <= 5]
            X = np.column_stack([np.ones(len(fitg))] + terms(fitg, fitg["BSA_" + k]))
            keep = np.ones(len(fitg), dtype=bool)
            for _ in range(12):
                coef, *_ = np.linalg.lstsq(X[keep], fitg.Z.values[keep], rcond=None)
                r = np.abs(X @ coef - fitg.Z.values)
                keep = r <= np.quantile(r, 0.85)
            Xa = np.column_stack([np.ones(len(g))] + terms(g, g["BSA_" + k]))
            pred.loc[g.index] = Xa @ coef
        e = (pred - zp.Z).abs()
        rows.append({"form": label, "BSA": k, "all pairs within 0.1 (%)": round(100 * (e <= 0.1).mean(), 1),
                     "|Z| <= 5 within 0.1 (%)": round(100 * (e[zp.Z.abs() <= 5] <= 0.1).mean(), 1),
                     "median |diff|": round(e.median(), 3)})
print(pd.DataFrame(rows).set_index(["form", "BSA"]).to_string())

print("\n5c. ALL SEVEN BEIJING 2013 MODELS (Tables 4, 5 and 7; Z = (y - fitted) / sqrt(MSE), y = D or ln D):")
print("    % of all pairs reproduced within 0.1, by BSA formula")
BJ7 = {  # vessel: [(log_outcome, intercept, [coef BSA, BSA^2, BSA^3] or None for ln(BSA) model, beta_lnBSA, MSE)]
    "LMCA": [(False, 1.828, [1.1827], None, 0.077), (False, 1.410, [2.236, -0.556], None, 0.068),
             (False, 0.811, [4.771, -3.528, 1.016], None, 0.062), (True, 0.654, [0.434], None, 0.012),
             (True, 0.412, [1.044, -0.322], None, 0.009), (True, 0.124, [2.261, -1.748, 0.487], None, 0.008),
             (True, 1.119, None, 0.357, 0.008)],
    "LAD": [(False, 1.517, [0.937], None, 0.072), (False, 1.072, [2.059, -0.593], None, 0.061),
            (False, 0.645, [3.865, -2.710, 0.724], None, 0.058), (True, 0.453, [0.429], None, 0.017),
            (True, 0.165, [1.156, -0.384], None, 0.013), (True, -0.128, [2.393, -1.834, 0.496], None, 0.012),
            (True, 0.915, None, 0.360, 0.012)],
    "RCA": [(False, 1.626, [1.058], None, 0.074), (False, 1.231, [2.054, -0.526], None, 0.066),
            (False, 0.870, [3.581, -2.316, 0.612], None, 0.064), (True, 0.534, [0.438], None, 0.015),
            (True, 0.285, [1.064, -0.331], None, 0.012), (True, 0.049, [2.063, -1.501, 0.400], None, 0.011),
            (True, 1.003, None, 0.360, 0.011)]}
LABELS = ["D linear", "D quadratic", "D cubic", "ln D linear", "ln D quadratic", "ln D cubic", "ln D on ln BSA (selected)"]
rows = []
for m, lab in enumerate(LABELS):
    row = {"Beijing model": lab}
    for k in BSA:
        z = pd.Series(np.nan, index=zp.index)
        for v, g in zp.groupby("vessel"):
            is_log, a, poly, b_ln, mse = BJ7[v][m]
            B = g["BSA_" + k]
            fitted = a + (b_ln * np.log(B) if poly is None else sum(c * B ** (i + 1) for i, c in enumerate(poly)))
            y = np.log(g.D) if is_log else g.D
            z.loc[g.index] = (y - fitted) / np.sqrt(mse)
        row[k] = round(100 * ((z - zp.Z).abs() <= 0.1).mean(), 1)
    rows.append(row)
print(pd.DataFrame(rows).set_index("Beijing model").to_string())

print("\n6. ILLUSTRATION: diameter at reported Z = 2.0 and 2.5 for a child of 100 cm and 16 kg")
H, W = 100.0, 16.0
b_ste = 0.0061 * H + 0.0128 * W - 0.1529
for v in ["LMCA", "LAD", "RCA"]:
    fl = fit.loc[v]
    mean_lab = fl.a + fl.b_sqrtBSA * np.sqrt(b_ste) + fl.c_BSA * b_ste
    a, b, m = BJ[v]
    mu = a + b * np.log(b_ste)
    b_hay = 0.024265 * H ** 0.3964 * W ** 0.5378
    da, db, dase, dbse = DAL[v]
    mu_d, sd_d = da + db * np.sqrt(b_hay), dase + dbse * np.sqrt(b_hay)
    print(f"   {v}: lab equation {mean_lab + 2 * fl.SD_mm:.2f} / {mean_lab + 2.5 * fl.SD_mm:.2f} mm; "
          f"Beijing {np.exp(mu + 2 * np.sqrt(m)):.2f} / {np.exp(mu + 2.5 * np.sqrt(m)):.2f} mm (Stevenson BSA {b_ste:.3f}); "
          f"Dallaire {mu_d + 2 * sd_d:.2f} / {mu_d + 2.5 * sd_d:.2f} mm (Haycock BSA {b_hay:.3f})")
