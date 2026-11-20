<div align="center">

## 🌐 Languages / اللغات: &nbsp; [English 🇺🇸](README.md) &nbsp;&bull;&nbsp; [العربية 🇪🇬](README.ar.md)

</div>

---

# 🛡️ X-IDS: Explainable AI Network Intrusion Detection System
> **An End-to-End Explainable Machine Learning Pipeline for Network Intrusion Detection & Security Analytics**  
> *Academic Graduation Project — Based on the CIC-IDS2017 Improved Benchmark Dataset*

---

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter Notebook" />
  <img src="https://img.shields.io/badge/XGBoost-Tree%20Ensemble-EB6C24?style=for-the-badge" alt="XGBoost" />
  <img src="https://img.shields.io/badge/SHAP-Explainable%20AI-0052CC?style=for-the-badge" alt="SHAP" />
  <img src="https://img.shields.io/badge/Platform-Windows%201--Click-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
</p>

---

## ⚡ 1-Click Autonomous Launcher (Zero Configuration)

If you are running on Windows, **you do not need to install or configure anything manually**.

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/Ahmed77khaled/X-IDS-Project.git
   ```
2. **Double-click** the launcher script in the project root:
   ```text
   👉 START_PROJECT.bat
   ```
3. **What `START_PROJECT.bat` handles automatically:**
   * ✅ **Python Verification:** Checks if Python is installed; if missing, automatically downloads and installs Python with PATH configuration enabled.
   * ✅ **Virtual Environment:** Creates and isolates `.venv`.
   * ✅ **Dependencies:** Installs all machine learning dependencies (`pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `ipykernel`).
   * ✅ **VS Code Integration:** Silently installs the VS Code Python & Jupyter extensions.
   * ✅ **Kernel Auto-Binding:** Sets **`Python (X-IDS Machine Learning)`** as the pre-selected kernel.
   * ✅ **Ready-to-Run Launch:** Launches VS Code directly into `my_model_training.ipynb`, fully bound and ready to run immediately.

---

## 📌 Project Overview

**X-IDS** is an Explainable Network Intrusion Detection System designed to bridge the gap between high-accuracy machine learning classifiers and human-interpretable cybersecurity operations. 

Modern Security Operations Centers (SOCs) often struggle with black-box AI models due to unverified predictions and unexplained false alarms. X-IDS addresses this challenge by providing:
1. **High Detection Rate (DR):** Leveraging tree ensembles (XGBoost, Random Forest) tuned specifically for network flow metrics.
2. **Explainability (XAI):** Utilizing **SHAP (SHapley Additive exPlanations)** and **LIME** to explain *why* a particular network packet/flow was classified as malicious (e.g., DoS, PortScan, Infiltration).
3. **Leakage-Resilient Data Engineering:** Cleaned strictly in accordance with modern cybersecurity benchmark research (Engelen et al., *CIC-IDS2017 Improved*), removing deceptive socket and timestamp identifiers.

---

## 📂 Repository Structure

```text
X-IDS-Project/
├── START_PROJECT.bat              # Autonomous 1-click launcher for Windows
├── setup.bat                      # Standard environment setup alias
├── my_model_training.ipynb        # Primary interactive guided notebook (Tasks 1-9)
├── requirements.txt               # Pinned dependencies for Python
├── README.md                      # English documentation & overview
├── README.ar.md                   # Arabic documentation & RTL guide
├── .gitignore                     # Optimized exclusion rules (dataset & secrets protected)
│
├── audio/                         # Curated voiceover narration (Fel7o Persona)
│   ├── step1.mp3 to step9.mp3     # High-fidelity ElevenLabs audio files for each task
│   └── scripts/                   # Exact text transcripts for every step
│
├── data/                          # Offline test samples & benchmark schema
│   └── cic_ids2017_sample.csv     # Lightweight sample for rapid offline verification
│
├── Dataset/                       # Local dataset folder (Excluded from Git / ~1.4GB)
│   └── CICIDS2017_improved/       # Wednesday-workingHours.pcap_ISCX.csv
│
├── Reports/                       # Academic milestones, slide decks, and blueprints
│   ├── 01_تسليم_المرحلة_الأولى/   # Phase 1 submission report (.docx, .pdf, .pptx)
│   └── 02_وثائق_المشروع_الرئيسية/  # Graduation project blueprint & architecture
│
└── .vscode/                       # Workspace configurations & auto-bound kernel settings
    ├── settings.json              # Relative interpreter binding (${workspaceFolder}/.venv)
    └── extensions.json            # Recommended extensions
```

---

## 🗺️ Project Pipeline & Roadmap

| Phase | Stage | Description | Status |
|:---:|:---|:---|:---:|
| **01** | **Data Engineering & Hygiene** | 9 interactive tasks: NaN/Inf sanitization, median imputation, socket removal (anti-leakage), and re-labeling `Attempted` to `BENIGN`. | **Completed** |
| **02** | **Feature Engineering** | Multi-class encoding, feature scaling (RobustScaler), and stratified splitting. | *Upcoming* |
| **03** | **Model Training & Tuning** | Tree Ensembles (XGBoost, Random Forest, LightGBM) with hyperparameter optimization. | *Upcoming* |
| **04** | **Evaluation & Metrics** | Confusion Matrix, Detection Rate vs False Alarm Rate, PR-AUC, and F1-Score. | *Upcoming* |
| **05** | **Explainable AI (XAI)** | Global feature attribution & local packet explanation using SHAP and LIME. | *Upcoming* |
| **06** | **SOC Web Dashboard** | Interactive frontend dashboard for network flow inspection and real-time alerts. | *Upcoming* |

---

## 🛡️ Rigorous Cybersecurity Preprocessing Standards

* **Socket & Identifier Removal:** Strips `Flow ID`, `Source IP`, `Destination IP`, `Source Port`, and `Timestamp` to force the AI to learn attack behaviors rather than memorizing laboratory testbed network addresses.
* **Attempted Label Reclassification:** Reclassifies non-breach attempts into `BENIGN` status according to the Engelen et al. (2021) peer-reviewed benchmark methodology.
* **Median Imputation for Robustness:** Uses feature medians rather than means to prevent mathematical skew caused by extreme DoS traffic volumes.

---

## 📄 License & Academic Attribution
Developed as an **Academic Graduation Project in Artificial Intelligence & Cybersecurity**.  
Dataset attribution: *Canadian Institute for Cybersecurity (CIC)* & the *CIC-IDS2017 Improved* benchmark (Engelen et al.).
