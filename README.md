# 🛡️ X-IDS: Explainable AI Network Intrusion Detection System
> **An End-to-End Explainable Machine Learning Pipeline for Network Intrusion Detection & Security Analytics**  
> *Academic Graduation Project — Based on the CIC-IDS2017 Improved Dataset*

---

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter Notebook" />
  <img src="https://img.shields.io/badge/XGBoost-Tree%20Ensemble-EB6C24?style=for-the-badge" alt="XGBoost" />
  <img src="https://img.shields.io/badge/SHAP-Explainable%20AI-0052CC?style=for-the-badge" alt="SHAP" />
  <img src="https://img.shields.io/badge/Platform-Windows%201-Click-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
</p>

---

## ⚡ 1-Click Quickstart (Zero Configuration)

If you are running on Windows, **you do not need to install or configure anything manually**.

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/Ahmed77khaled/X-IDS-Project.git
   ```
2. **Double-click** the launcher script in the project root:
   ```text
   👉 START_PROJECT.bat
   ```
3. **What `START_PROJECT.bat` does automatically:**
   * ✅ Checks if Python is installed; if not, automatically downloads and installs Python 3.11 with PATH configuration.
   * ✅ Creates an isolated virtual environment (`.venv`).
   * ✅ Installs all machine learning dependencies (`pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `ipykernel`).
   * ✅ Silently installs the VS Code Python & Jupyter extensions.
   * ✅ Automatically binds the kernel **`Python (X-IDS Machine Learning)`** as the default.
   * ✅ Launches VS Code directly into `my_model_training.ipynb`, pre-connected and ready to run immediately.

---

## 📌 Project Overview

**X-IDS** is an Explainable Network Intrusion Detection System designed to bridge the gap between high-accuracy machine learning classifiers and human-interpretable cybersecurity operations. 

Modern Security Operations Centers (SOCs) often reject black-box AI models due to unexplained false alarms. X-IDS addresses this challenge by providing:
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

<br/>

<div dir="rtl" style="text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">

# 📖 الدليل العربي السريع (لأعضاء الفريق والباحثين)

أهلاً بكم في مستودع مشروع التخرج **X-IDS**. تم بناء هذا المشروع ليكون متكاملاً وسهل التشغيل بدون أي خطوات معقدة.

### 🎯 طريقة التشغيل في خطوة واحدة:
كل ما عليك فعله بعد تنزيل المشروع هو الضغط مرتين على ملف:
> ### `START_PROJECT.bat`

* الملف سيقوم تلقائياً بفحص وتثبيت بايثون (لو لم يكن موجوداً)، وتثبيت المكتبات، وربط الكيرنل ببرنامج **VS Code**، وفتح دفتر العمل **`my_model_training.ipynb`**.
* البيئة ستفتح وهي **جاهزة للتشغيل الفوري** بدون الحاجة للضغط على أي أزرار إعداد أو اختيار الكيرنل يدوياً.

### 🎙️ المساعد الصوتي التفاعلي (فِلحو - Fel7o):
* داخل كل خطوة من خطوات النوت بوك ستجد **مشغل صوتي مدمج** بصوت باللهجة المصرية لشرح الفكرة الهندسية وطريقة كتابة الكود والهدف منه.
* أسفل كل مقطع صوتي يوجد **تفريغ نصي كامل** للمتابعة بالقراءة أثناء الاستماع.

### 🛡️ قواعد الأمان المتبعة في تجهيز البيانات:
1. **منع تسريب البيانات (Data Leakage):** حذف أعمدة `Flow ID`, `Source IP`, `Destination IP`, `Timestamp` حتى يتعلم النموذج السلوك الإحصائي لحركة الهجوم بدلاً من حفظ عناوين الأجهزة.
2. **معالجة محاولات الهجوم (Attempted):** تصحيح تصنيف المحاولات التي لم تنجح كاختراق فعلي وإعادتها لتصنيف `BENIGN` وفق أحدث المنهجيات البحثية.
3. **التعويض بالوسيط (Median Imputation):** للحفاظ على سلامة البيانات من الانحرافات الناتجة عن القيم المتطرفة في هجمات DoS.

</div>

---

## 📄 License & Academic Attribution
Developed as an **Academic Graduation Project in Artificial Intelligence & Cybersecurity**.  
Dataset attribution: *Canadian Institute for Cybersecurity (CIC)* & the *CIC-IDS2017 Improved* benchmark (Engelen et al.).
