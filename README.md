# Battery-Modelling

Analytical Level 1 model scripts and illustrative scenario datasets for battery physical architecture and electrode ionic transport modeling.

> **Note**: This repository contains the reproducible calculation scripts, scenario input parameters, and generated datasets supporting the review manuscript on battery physical architectures.

---

## 📁 Repository Contents

| File | Description |
| :--- | :--- |
| [`ionic_resistance_scenarios.py`](ionic_resistance_scenarios.py) | Standalone Python script (zero third-party dependencies) calculating through-plane effective ionic resistance ($R_{\text{ion}}$) and characteristic ohmic overpotential drop ($\Delta V_{\text{ion}}$) across 36 scenarios. |
| [`ionic_resistance_inputs.json`](ionic_resistance_inputs.json) | Parameter input file specifying geometric dimensions ($L = 50\text{--}200\,\mu\text{m}$, $A = 1\text{--}100\,\text{cm}^2$), electrolyte bulk conductivity, porosity, tortuosity factor, and operational C-rates ($0.5\text{--}3.0\,\text{h}^{-1}$). |
| [`ionic_resistance_results.csv`](ionic_resistance_results.csv) | Full 36-row tabulated dataset of calculated scenario outputs ($j$, $I$, $R_{\text{ion}}$, $\text{ASR}$, $\Delta V_{\text{ion}}$ scale). |
| [`ionic_resistance_method.md`](ionic_resistance_method.md) | Detailed mathematical derivation, algebraic area cancellation rationale, parameter assumptions, and model boundary clarifications (Chinese). |
| [`transport_scenarios.py`](transport_scenarios.py) | Exploratory characteristic diffusion timescale and flow-cell pumping scenario checks. |
| [`Supplementary_Material_S1.zip`](Supplementary_Material_S1.zip) | Packaged ZIP archive of the complete supplementary material. |

---

## ⚡ Quick Start & Reproduction

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
36 illustrative scenarios; units, area cancellation and thickness scaling verified; no empirical validation claimed.
```

---

## 📐 Method & Formulation Summary

Under a uniform through-plane effective-medium slab approximation:

$$\kappa_{\text{eff}} = \kappa_{\text{bulk}} \frac{\varepsilon}{\tau}$$

$$R_{\text{ion}} = \frac{L}{\kappa_{\text{eff}} A}$$

$$I = j A$$

$$\Delta V_{\text{ion}} = I R_{\text{ion}} = \frac{j L}{\kappa_{\text{eff}}}$$

- **Area Cancellation:** Under a fixed average superficial current density $j$, scaling the projected electrode area $A$ increases the total current proportionally ($I = j A$) while decreasing total through-plane ionic resistance inversely ($R_{\text{ion}} \propto 1/A$). Consequently, the characteristic 1D ohmic potential scale $\Delta V_{\text{ion}}$ is independent of projected area.
- **Baseline Values:** With $\kappa_{\text{bulk}} = 10\,\text{mS}/\text{cm}$, $\varepsilon = 0.3$, $\tau = 3$ (yielding $\kappa_{\text{eff}} = 1\,\text{mS}/\text{cm}$), $L = 100\,\mu\text{m}$, and $j = 3.5\,\text{mA}/\text{cm}^2$ (1.0C for $3.5\,\text{mAh}/\text{cm}^2$), the baseline characteristic ionic ohmic drop is:

$$\Delta V_{\text{ion}} = 35.0\,\text{mV}$$

Doubling thickness to $L = 200\,\mu\text{m}$ increases this scale to $70.0\,\text{mV}$ at 1.0C and $210.0\,\text{mV}$ at 3.0C.

---

## 📄 License & Attribution

All scripts and configuration files are open for academic and educational research.
