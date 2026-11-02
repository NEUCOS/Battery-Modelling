from pathlib import Path
import json,csv,math
p=Path(__file__).resolve().parent
x=json.loads((p/'ionic_resistance_inputs.json').read_text(encoding='utf-8'))
k=x['bulk_conductivity_mS_cm']*1e-3*x['porosity']/x['tortuosity_factor']
rows=[]
for L_um in x['thickness_um']:
 L_cm=L_um*1e-4
 for rate in x['nominal_rate_per_h']:
  j_mA=x['nominal_areal_capacity_mAh_cm2']*rate
  for A in x['projected_area_cm2']:
   I_mA=j_mA*A;R=L_cm/(k*A);ASR=R*A;drop_mV=I_mA*R
   assert math.isclose(drop_mV,j_mA*L_cm/k,rel_tol=1e-12)
   rows.append(dict(L_um=L_um,A_cm2=A,rate_per_h=rate,j_mA_cm2=j_mA,I_mA=I_mA,k_eff_S_cm=k,R_ion_ohm=R,ASR_ohm_cm2=ASR,ionic_resistance_scale_mV=drop_mV))
with (p/'ionic_resistance_results.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
base=next(r for r in rows if r['L_um']==100 and r['A_cm2']==1 and r['rate_per_h']==1)
large=next(r for r in rows if r['L_um']==100 and r['A_cm2']==100 and r['rate_per_h']==1)
thick=next(r for r in rows if r['L_um']==200 and r['A_cm2']==1 and r['rate_per_h']==1)
assert math.isclose(base['ionic_resistance_scale_mV'],35)
assert math.isclose(large['I_mA']/base['I_mA'],100)
assert math.isclose(large['R_ion_ohm']/base['R_ion_ohm'],0.01)
assert math.isclose(thick['ionic_resistance_scale_mV']/base['ionic_resistance_scale_mV'],2)
print(f'{len(rows)} illustrative scenarios; units, area cancellation and thickness scaling verified; no empirical validation claimed.')
