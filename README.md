# 🧪 DFT Molecular Benchmark

**Reproducible Density Functional Theory Pipeline using ASE + GPAW**

[![PDF Report](https://img.shields.io/badge/PDF-Report-blue)](pdf/DFT_Molecular_Benchmark_Report.pdf)

---

## 📊 Overview

This project demonstrates a standardized DFT workflow for molecular systems:

- ✅ **Core analysis** (H₂, CO, H₂O): geometry, orbitals, dipole, charges
- ✅ **Deep dive** (H₂ only): potential curve, vibrational frequency
- ✅ **Automated pipeline** with BFGS optimization
- ✅ **Publication-quality figures** (300 DPI)
- ✅ **OpenClaw workflow** (human-AI collaboration)

---

## 🎯 Results Summary

### Core Analysis (All Molecules)

| Molecule | Bond (Å) | Exp (Å) | Error | HOMO-LUMO Gap (eV) | Dipole (D) |
|----------|----------|---------|-------|-------------------|-----------|
| H₂       | 0.751    | 0.741   | 1.35% | 10.56 (exp ~11)   | 0.000     |
| CO       | 1.137    | 1.128   | 0.80% | 12.00 (exp ~14)   | 0.202     |
| H₂O      | 0.971    | 0.957   | 1.46% | 11.70 (exp ~12.6) | 1.807     |

**Average Geometry Error:** 1.20% ✅

### H₂ Deep Dive

- **Potential curve:** R_eq = 0.755 Å (exp: 0.741 Å, error 1.94%)
- **Vibrational frequency:** 3770 cm⁻¹ (exp: 4401 cm⁻¹, error 14.3%)

All results validated against NIST Chemistry WebBook.

---

## 📄 Main Output

**📕 [PDF Report](pdf/DFT_Molecular_Benchmark_Report.pdf)** (1.4 MB, ~12-14 pages)

**Contents:**
- **Section 3:** Core Analysis (geometry, orbitals, dipole, charges)
- **Section 4:** H₂ Deep Dive (potential curve, vibrational frequency)
- **Section 5:** Discussion (limitations, best practices)

**Structure:**
- Core properties for all molecules (standardized)
- Deep dive only for H₂ (1D potential is meaningful)
- No 1D curves for polyatomics (H₂O has 3N-6 modes, not representative)

---

## 📁 Project Structure

```
project_dft_tests/
├── modules/              # Calculation modules
├── runs/                 # DFT outputs (H2, CO, H2O)
│   └── */bfgs_history.csv   # Optimization traces
├── results/              # Processed data (JSON, CSV)
│   ├── core_analysis.json
│   └── h2_vibrational.json
├── plots/                # Figures (300 DPI)
│   ├── geometry_summary_core.png
│   ├── molecular_orbitals_core.png
│   ├── dipole_moments_core.png
│   ├── convergence_analysis_pub.png
│   ├── h2_potential_curve.png
│   └── h2_vibrational_deep.png
├── pdf/                  # Final report
│   └── DFT_Molecular_Benchmark_Report.pdf
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python3 -m venv dft_env
source dft_env/bin/activate
pip install ase gpaw matplotlib numpy scipy pandas
```

### 2. Run Pipeline

```bash
python3 run_all.py
```

**Expected runtime:** ~2 hours (geometry optimization + analysis)

### 3. View Results

```bash
cat results/core_analysis.json
open pdf/DFT_Molecular_Benchmark_Report.pdf
```

---

## ⚙️ Computational Setup

**DFT Parameters:**
- Exchange-Correlation: PBE (GGA)
- Mode: Finite difference (real-space)
- Grid Spacing: 0.18 Å
- Energy Convergence: 10⁻⁵ eV
- Force Convergence: 0.02 eV/Å
- Optimizer: BFGS

**Software:**
- Python 3.12.3
- ASE 3.23.0
- GPAW 24.6.0

---

## 📈 Analysis Structure

### Core Analysis (H₂, CO, H₂O)

**1. Optimized Geometries**
- Bond lengths within 1.5% of experimental
- Angles within 0.5% of experimental

**2. Electronic Properties**
- HOMO-LUMO gaps (4-14% underestimation, typical GGA)
- Molecular orbital diagrams

**3. Dipole Moments**
- H₂O: 2.3% error (excellent!)
- CO: 80% error (known PBE pathology)

**4. Atomic Charges**
- Qualitative distribution (Mulliken-like)

### Deep Dive (H₂ Only)

**5. Potential Energy Curve**
- 11-point scan (R = 0.5-1.5 Å)
- Quadratic fit near minimum
- R_eq extraction

**6. Vibrational Frequency**
- Harmonic approximation
- Force constant calculation
- Comparison with experimental

**Rationale:** 1D potential curves only meaningful for diatomic molecules. Polyatomics like H₂O have 3N-6 modes; focus on geometry and dipole instead.

---

## 🔬 Key Findings

### What PBE Does Well ✅
- **Geometries:** 1.2% average error (excellent)
- **H₂O dipole:** 2.3% error (excellent)
- **H₂ equilibrium distance:** 1.94% error (excellent)

### Known Limitations ⚠️
- **HOMO-LUMO gaps:** 4-14% underestimation (GGA self-interaction error)
- **CO dipole:** 80% overestimation (known PBE pathology)
- **Vibrational frequencies:** 14% underestimation (PBE softer potential)

### Best Practices
- Use PBE for **geometry optimization** (reliable)
- Use hybrid functionals for **electronic gaps** (B3LYP, PBE0)
- Interpret **atomic charges** qualitatively only
- Focus on **geometry + dipole** for polyatomics (not 1D scans)

---

## 🤖 OpenClaw Workflow

Human-AI collaboration for scientific computing:

| Aspect | Human (Rick) | AI (Faraday) |
|--------|--------------|--------------|
| Strategy | Define protocol | Implement pipeline |
| Validation | Physics interpretation | Execute calculations |
| Documentation | Review quality | Generate reports |

**Timeline:** ~2 hours from concept to publication-ready results

---

## 📚 Citation

```bibtex
@software{dft_molecular_benchmark_2026,
  title={DFT Molecular Benchmark: Standardized Core Analysis + Deep Dive},
  author={Rick and Faraday},
  year={2026},
  url={https://github.com/LuisRicardoMontoya/dft-molecular-benchmark}
}
```

**Software:**
- ASE: https://wiki.fysik.dtu.dk/ase/
- GPAW: https://wiki.fysik.dtu.dk/gpaw/
- OpenClaw: https://docs.openclaw.ai/

---

## 📝 License

MIT License - See LICENSE file for details

---

**Generated with OpenClaw Experimental Workflow**  
*Human Strategy (Rick) + AI Execution (Faraday)*

March 2, 2026
