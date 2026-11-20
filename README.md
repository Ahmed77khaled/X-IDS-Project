<div align="center">

# 🌐 &nbsp; [English 🇺🇸](#english) &nbsp;&nbsp;&bull;&nbsp;&nbsp; [العربية 🇪🇬](#arabic)

</div>

---

<div id="english"></div>

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
   * ✅ **Smart Dataset Handling:** Checks for `wednesday.csv`. If missing, prompts to download and extract it automatically from the official [DistriNet Research Repository](https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip).
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
├── README.md                      # Unified documentation (English & Arabic RTL)
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

<br />
<br />

---

<div id="arabic"></div>

<div dir="rtl" align="right">

## الشرح باللغة العربية 

<div align="center">

[⬆️ العودة للأعلى (Back to Top)](#english)

</div>

### 🛡️ مشروع X-IDS: كشف اختراقات الشبكة بالذكاء الاصطناعي وتفسير القرارات
> **منظومة متكاملة لكشف التسلل السيبراني وتفسير قرارات نماذج التعلم الآلي لمهندسي مراكز العمليات الأمنية (SOC)**  
> *مشروع تخرج أكاديمي — مبني على داتاسيت CIC-IDS2017 Improved*

---

### ⚡ التشغيل الفوري بنقرة واحدة (بدون أي إعدادات يدوية)

لو أنت شغال على ويندوز، **مش محتاج تسطب أو تظبط أي حاجة بإيدك نهائياً**:

1. **حمّل المشروع** من خلال Clone أو Download ZIP:
   ```bash
   git clone https://github.com/Ahmed77khaled/X-IDS-Project.git
   ```
2. **اضغط دبل كليك** على ملف التشغيل في المجلد الرئيسي:
   ```text
   👉 START_PROJECT.bat
   ```
3. **السكريبت هيعمل الآتي تلقائياً بالكامل:**
   * ✅ **فحص بايثون:** لو بايثون مش متسطب على جهازك، هيحمله ويسطبه أوتوماتيك ويفعل الـ PATH.
   * ✅ **إنشاء البيئة الافتراضية:** بينشئ ويفعل مجلد معزول `.venv` عشان ما يلخبطش مكتبات جهازك.
   * ✅ **تسطيب المكتبات:** بيثبت كل مكتبات الذكاء الاصطناعي المطلوبة (`pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `ipykernel`).
   * ✅ **التحقق الذكي من الداتاسيت:** بيفحص ملف `wednesday.csv`. لو مش موجود، بيسألك لو حابب يحمله أوتوماتيك من الرابط الرسمي للجامعة ويفك ضغطه في فولدر `Dataset` مباشرة.
   * ✅ **تثبيت إضافات VS Code:** بيثبت إضافات بايثون وجوبيتر الرسمية لبرنامج VS Code بشكل صامت.
   * ✅ **ربط الكيرنل تلقائياً:** بيحدد كيرنل `Python (X-IDS Machine Learning)` مسبقاً للنوت بوك.
   * ✅ **الفتح والجاهزية:** بيفتح برنامج VS Code مباشرة على النوت بوك `my_model_training.ipynb` جاهز للكتابة والتشغيل فوراً!

---

### 📌 نبذة عامة عن المشروع

مشروع **X-IDS (Explainable Intrusion Detection System)** يهدف لسد الفجوة بين نماذج الذكاء الاصطناعي عالية الدقة وبين مهندسي ومحللي الأمن السيبراني في مراكز العمليات الأمنية (SOC).

أغلب أنظمة الذكاء الاصطناعي الحالية تُعتبر "صناديق سوداء" (Black-Box)، تعطي إنذارات دون توضيح سبب الإنذار، مما يؤدي لتجاهلها لكثرة الإنذارات الكاذبة. يقدم مشروعنا حلاً حقيقياً عبر ثلاث ركائز:
1. **دقة كشف عالية (High Detection Rate):** باستخدام خوارزميات أشجار القرار المعززة (`XGBoost` و `Random Forest`) المدربة على خصائص تدفقات الشبكة.
2. **تفسيرية القرارات بالذكاء الاصطناعي (Explainable AI - XAI):** باستخدام مكتبات `SHAP` و `LIME` لتوضيح أسباب تصنيف كل حزمة أو جلسة اتصال كـ هجوم (مثل هجمات الحرمان من الخدمة DoS، أو فحص المنافذ PortScan، أو التسلل Infiltration).
3. **تطهير البيانات ومقاومة التسريب (Leakage-Resilient):** تم تنظيف البيانات وفق أحدث المعايير البحثية المحكمة لداتاسيت `CIC-IDS2017 Improved`، مع استبعاد المعرفات الخادعة.

---

### 🎙️ المساعد التعليمي الصوتي التفاعلي ("فِلحو - Fel7o")

لضمان فهم كل عضو في الفريق واللجان الأكاديمية لكل خطوة برمجية:
* **تسجيلات صوتية مدمجة:** في كل خطوة عملية من خطوات النوت بوك، يوجد مشغل صوتي يشرح بالعامية المصرية فلسفة الخطوة والهدف الهندسي منها.
* **تفريغ نصي متزامن:** صندوق قراءة كامل أسفل كل صوت لمتابعة الشرح كلمة بكلمة.
* **قوالب الأكواد والتنبيهات:** إرشادات عملية لكتابة الكود والتحذير من الأخطاء الشائعة قبل الوقوع فيها.

---

### 🛡️ المعايير الأمنية المطبقة في هندسة البيانات

1. **منع تسريب البيانات (Data Leakage Prevention):**
   * تم حذف أعمدة السوكت والمعرفات الزمنية: `Flow ID` و `Source IP` و `Destination IP` و `Source Port` و `Timestamp`.
   * لو تُركت هذه الأعمدة، سيقوم النموذج بحفظ عناوين أجهزة معمل الاختبار بدلاً من فهم الأنماط السلوكية للهجوم، ويفشل تماماً عند تشغيله في شبكة واقعية.
2. **إعادة تصنيف محاولات الهجوم (Attempted Attacks):**
   * تم إعادة تصنيف الحالات الموسومة بـ `Attempted` إلى فئة `BENIGN`، لأنها محاولات فاشلة لم تخترق الشبكة، وذلك التزاماً بالمنهجية العلمية لأبحاث داتاسيت `CIC-IDS2017 Improved`.
3. **التعويض الإحصائي المتين بالوسيط (Median Imputation):**
   * تم استخدام الوسيط الحسابي (`Median`) بدلاً من المتوسط (`Mean`) لتعويض الخانات المفقودة، لأن بيانات حركة الشبكات تتضمن قيماً شاذة وانفجارات لحظية ضخمة ناتجة عن هجمات DoS، تجعل المتوسط مشوهاً وغير واقعي.

---

### 📄 حقوق العمل والإسناد الأكاديمي
تم إعداد وتطوير هذا المشروع كمشروع تخرج أكاديمي في تخصص **الذكاء الاصطناعي والأمن السيبراني**.  
مرجعية الداتاسيت: *Canadian Institute for Cybersecurity (CIC)* وأبحاث الورقة المرجعية *CIC-IDS2017 Improved (Engelen et al., 2021)*.

<div align="center">

[⬆️ العودة للأعلى (Back to Top)](#english)

</div>

</div>
