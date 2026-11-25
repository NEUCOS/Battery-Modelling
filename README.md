# Battery-Modelling

Analytical Level 1 scaling script and illustrative 12-scenario dataset for battery physical architecture and electrode ionic transport analysis.

> **Note**: This repository contains the reproducible calculation scripts, scenario input parameters, and generated datasets supporting Section 7.1 of the review manuscript on battery physical architectures.

---

## Repository Contents

| File | Description |
| :--- | :--- |
| [`ionic_resistance_scenarios.py`](ionic_resistance_scenarios.py) | Standalone Python script (zero third-party dependencies) calculating area-specific through-plane ionic resistance ($\text{ASR}$) and characteristic ohmic potential drop ($\Delta V_{\text{ion}}$) across 12 thickness $\times$ C-rate combinations, while verifying algebraic area invariance. |
| [`ionic_resistance_inputs.json`](ionic_resistance_inputs.json) | Parameter input file specifying electrode thicknesses ($L = 50, 100, 200\,\mu\text{m}$), reference projected area ($A_{\text{ref}} = 1\,\text{cm}^2$), electrolyte bulk conductivity, porosity, tortuosity factor, nominal areal capacity ($3.5\,\text{mAh cm}^{-2}$), and C-rates ($0.5, 1, 2, 3\,\text{h}^{-1}$). |
| [`ionic_resistance_results.csv`](ionic_resistance_results.csv) | 12-row tabulated dataset of calculated scenario outputs ($j$, $I_{\text{ref}}$, $R_{\text{ion,ref}}$, $\text{ASR}$, $\Delta V_{\text{ion}}$ scale), spanning $8.75\,\text{mV}$ ($50\,\mu\text{m}$, $0.5\,\text{h}^{-1}$) to $210.0\,\text{mV}$ ($200\,\mu\text{m}$, $3\,\text{h}^{-1}$). |
| [`ionic_resistance_method.md`](ionic_resistance_method.md) | Mathematical derivation, algebraic area-cancellation rationale, parameter assumptions, and model boundary clarifications (Chinese). |
| [`transport_scenarios.py`](transport_scenarios.py) | Exploratory characteristic diffusion timescale and flow-cell pumping scenario checks. |
| [`Supplementary_Material_S1.zip`](Supplementary_Material_S1.zip) | Packaged ZIP archive of the complete supplementary material. |

---

## Quick Start & Reproduction

The calculation uses strictly the **Python standard library** (`math`, `json`, `csv`, `pathlib`). No additional packages (such as NumPy or Pandas) are required.

```bash
# Clone the repository
git clone https://github.com/NEUCOS/Battery-Modelling.git
cd Battery-Modelling

# Run the parameter sweep and verification
python ionic_resistance_scenarios.py
```

Expected output:
```text
12 thickness-rate scenarios; units, area invariance and thickness scaling verified; no empirical validation claimed.
```

---

## Method & Formulation Summary

Under a uniform through-plane effective-medium slab approximation:

$$\kappa_{\text{eff}} = \kappa_{\text{bulk}} \frac{\varepsilon}{\tau}$$

$$\text{ASR} = \frac{L}{\kappa_{\text{eff}}}, \qquad R_{\text{ion}} = \frac{\text{ASR}}{A} = \frac{L}{\kappa_{\text{eff}} A}$$

$$I = j A, \qquad \Delta V_{\text{ion}} = j \cdot \text{ASR} = I R_{\text{ion}} = \frac{j L}{\kappa_{\text{eff}}}$$

- **Area Invariance (Why 12 Combinations):** Under a fixed average superficial current density $j$, $\text{ASR}$ and $\Delta V_{\text{ion}}$ are independent of projected electrode area $A$ (because $I \propto A$ and $R_{\text{ion}} \propto 1/A$ cancel identically). Accordingly, the sweep focuses on the 12 independent thickness $\times$ C-rate combinations, using $A_{\text{ref}} = 1\,\text{cm}^2$ solely to report total cell current $I_{\text{ref}}$ and resistance $R_{\text{ion,ref}}$.
- **Baseline & Range:** With $\kappa_{\text{bulk}} = 10\,\text{mS}/\text{cm}$, $\varepsilon = 0.3$, $\tau = 3$ (yielding $\kappa_{\text{eff}} = 1\,\text{mS}/\text{cm}$), $L = 100\,\mu\text{m}$, and $j = 3.5\,\text{mA}/\text{cm}^2$ (1.0C for $3.5\,\text{mAh}/\text{cm}^2$), the baseline characteristic ionic ohmic drop is $\Delta V_{\text{ion}} = 35.0\,\text{mV}$. Across the 12 combinations, $\Delta V_{\text{ion}}$ spans from $8.75\,\text{mV}$ ($50\,\mu\text{m}$, $0.5\text{C}$) to $210.0\,\text{mV}$ ($200\,\mu\text{m}$, $3\text{C}$).

---

## License & Attribution

All scripts and configuration files are open for academic and educational research.
