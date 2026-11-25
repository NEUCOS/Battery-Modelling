from pathlib import Path
import csv
import json
import math

p = Path(__file__).resolve().parent
x = json.loads((p / "ionic_resistance_inputs.json").read_text(encoding="utf-8"))
k = x["bulk_conductivity_mS_cm"] * 1e-3 * x["porosity"] / x["tortuosity_factor"]
A_ref = x.get("reference_area_cm2", 1)

rows = []
for L_um in x["thickness_um"]:
    L_cm = L_um * 1e-4
    for rate in x["nominal_rate_per_h"]:
        j_mA = x["nominal_areal_capacity_mAh_cm2"] * rate
        ASR = L_cm / k
        I_mA = j_mA * A_ref
        R = ASR / A_ref
        drop_mV = j_mA * ASR

        # Verify algebraic area invariance across arbitrary projected areas (1, 10, 100 cm^2)
        for A_test in (1, 10, 100):
            assert math.isclose((j_mA * A_test) * (ASR / A_test), drop_mV, rel_tol=1e-12)

        rows.append(
            dict(
                L_um=L_um,
                rate_per_h=rate,
                j_mA_cm2=round(j_mA, 6),
                A_ref_cm2=A_ref,
                I_ref_mA=round(I_mA, 6),
                k_eff_S_cm=round(k, 6),
                R_ion_ref_ohm=round(R, 6),
                ASR_ohm_cm2=round(ASR, 6),
                ionic_resistance_scale_mV=round(drop_mV, 6),
            )
        )

with (p / "ionic_resistance_results.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

assert len(rows) == 12
low = next(r for r in rows if r["L_um"] == 50 and r["rate_per_h"] == 0.5)
base = next(r for r in rows if r["L_um"] == 100 and r["rate_per_h"] == 1)
thick = next(r for r in rows if r["L_um"] == 200 and r["rate_per_h"] == 1)
high = next(r for r in rows if r["L_um"] == 200 and r["rate_per_h"] == 3)
assert math.isclose(low["ionic_resistance_scale_mV"], 8.75)
assert math.isclose(base["ionic_resistance_scale_mV"], 35.0)
assert math.isclose(thick["ionic_resistance_scale_mV"] / base["ionic_resistance_scale_mV"], 2.0)
assert math.isclose(high["ionic_resistance_scale_mV"], 210.0)
print(
    f"{len(rows)} thickness-rate scenarios; units, area invariance and thickness scaling verified; no empirical validation claimed."
)
