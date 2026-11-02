"""Transparent analytical scenarios, not fitted cell predictions or a DFN solver."""
import csv,json,math,sys
from pathlib import Path
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
def write(name,rows):
 with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# All numbers below are declared illustrative scenario inputs, not measured commercial data.
area=[]
for qa in [2,3.5,5]:
 for rate in [0.5,1,2,3,10]:
  for a in [1,100,10000]:
   j=qa*rate
   area.append(dict(qA_mAh_cm2=qa,C_rate_per_hour=rate,A_cm2=a,j_mA_cm2=j,I_A=j*a/1000,Q_Ah=qa*a/1000))
write('area_rate_ledger.csv',area)
diff=[]
for L in [50,100,150,200,250]:
 for eps in [0.3,0.4,0.5]:
  for tor in [1.5,3,5]:
   D=1e-6;Deff=D*eps/tor;t=(L*1e-4)**2/Deff
   diff.append(dict(L_um=L,porosity=eps,tortuosity_factor=tor,D_bulk_cm2_s=D,D_eff_cm2_s=Deff,t_diff_s=t,ratio_to_50um_same_microstructure=(L/50)**2))
write('diffusion_time_sensitivity.csv',diff)
flow=[]
for q in [0.5,0.75,1,1.5,2,3,4]:
 for a in [0.3,0.5,0.8]:
  # Relative flow x=Q/Q0; illustrative km~Q^alpha and laminar deltaP~Q.
  flow.append(dict(Q_over_Q0=q,assumed_mass_transfer_exponent=a,km_over_km0=q**a,deltaP_over_deltaP0=q,pump_power_over_Ppump0=q*q))
write('dimensionless_flow_tradeoff.csv',flow)
# Exact identities check units and ratios; these do not validate the assumed physical regimes.
assert math.isclose(3.5*10,35)
assert math.isclose((200/50)**2,16)
assert all(math.isclose(r['I_A']/r['Q_Ah'],r['C_rate_per_hour']) for r in area)
assert len(area)==45 and len(diff)==45 and len(flow)==21
config={'status':'analytical_working_scenarios_not_for_submission','parameter_source':'explicitly_assumed_scenarios_not_literature_fitted','D_bulk_cm2_s':1e-6,'flow_assumptions':['km/km0=(Q/Q0)^alpha','deltaP/deltaP0=Q/Q0','pump efficiency constant'],'validation':'unit and algebraic identity checks only','not_implemented':['DFN/P2D numerical solution','CFD','lithium plating prediction','commercial operating limit inference','empirical flow correlation fitting']}
(out/'scenario_inputs.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
(out/'model_notes.md').write_text('''# 返修用解析模型工作底稿

状态：用于检查变量、单位和趋势，尚未引入稿件；不是实验结果、商用品性能预测或已验证数值模型。所有输入在 scenario_inputs.json 及 CSV 中显式列出。

## 面积与倍率
设面容量 qA 的单位为 mAh/cm²，倍率 r 的单位为 h⁻¹，则 j=qA r 的单位是 mA/cm²；I=jA，Q=qA A。脚本将总电流换成 A、总容量换成 Ah。相同 qA 与 r 下，面积增大一万倍，总电流和容量均增大一万倍，j 不变。qA=3.5 的算例纯属演示输入，不能据此宣称已证明商用统计范围。

## 厚度与扩散时间
D_eff=D_bulk ε/τ，t_diff≈L²/D_eff；这里 τ 为 tortuosity factor，避免与路径长度比定义混淆。L 从 μm 换算为 cm 后计算。相同微结构下 50→200 μm 的时间比为 16，与 D 数值无关。该量仅为特征时间，不能直接等同放电截止时刻、析锂时间或寿命，也没有包含电迁移、浓溶液耦合、粒内扩散及温升。

## 流量收益与泵耗
P_pump=Δp Q/η_p；若近似处于固定几何的线性液阻范围，Δp∝Q，则固定泵效率下 P_pump∝Q²。km/km0=(Q/Q0)^α 是用于敏感性检查的假设，α=0.3、0.5、0.8 均为假设值，不是从文献拟合所得。不能用这些曲线宣称存在已确定的 VRFB 最优流量；需要校验适用几何、流态及实验相关式后才可用于定量分析。

## 混合架构需要补充的守恒关系
可用共同端电压中的两侧过电位和电阻项组织讨论；稳态串联电池必须满足相同总电流，对不同有效面积的两侧应分别写 j1=I/A1、j2=I/A2。不能直接对面积不同的两个 j_lim 取最小值；应先转为 I_lim,k=A_k j_lim,k。液固沉积容量可从法拉第定律 Q_dep=nFρAδ/M（C）建立几何账本，再除以 3600 得 Ah；需说明有效面积、均匀致密沉积及无副反应等假设。以上待取得并核实对应原文后由分节起草阶段确定是否纳入。

## 二作者理解检查
请本人解释：为何扩大面积增加总电流却不改变同一倍率下的 j；为何增厚四倍使扩散时间增为十六倍；为什么流量增加既有收益也有代价；为什么氢气侧快并不保证混合电池整电池快。不能回答时先删减或改写相应内容，不代签“已理解”。
''',encoding='utf-8')
print('Generated 45 area/rate cases, 45 diffusion cases, 21 relative-flow cases; algebra and unit checks passed.')
