# 🚀 دليل تشغيل بيئة العمل لفريق مشروع X-IDS
### Team Collaboration & Environment Setup Guide

مرحباً بك في مشروع **X-IDS (Explainable Network Intrusion Detection System)**.  
هذا الدليل مخصص لأي عضو في الفريق لبدء العمل وتشغيل ملفات التدريب والـ Notebooks في أقل من دقيقتين، سواء على جهازك المحلي (Windows / Mac / Linux) أو سحابياً بالكامل عبر **GitHub Codespaces** دون الحاجة لتثبيت أي برامج!

---

## 📑 خيارات التشغيل المتاحة

اختر الطريقة الأنسب لك:
1. [الخيار الأول: التشغيل التلقائي بنقرة واحدة على ويندوز (1-Click Windows Setup)](#1--الخيار-الأول-التشغيل-التلقائي-بنقرة-واحدة-على-ويندوز-1-click-setup) — **(الأسرع والأسهل)**
2. [الخيار الثاني: التشغيل السحابي عبر GitHub Codespaces](#2--الخيار-الثاني-التشغيل-السحابي-عبر-github-codespaces-1-click-cloud) — **(بدون أي تسطيب محلي)**
3. [الخيار الثالث: التشغيل اليدوي (Manual Setup - Linux / macOS / Windows)](#3--الخيار-الثالث-التشغيل-اليدوي-manual-setup)

---

## 1. ⚡ الخيار الأول: التشغيل التلقائي بنقرة واحدة على ويندوز (1-Click Setup)

تم إعداد ملف تشغيلي ذكي يقوم بجميع خطوات التثبيت نيابة عنك:
- فحص بيئة بايثون.
- إنشاء بيئة افتراضية منعزلة `.venv`.
- تحديث مدير الحزم `pip`.
- تثبيت كافة المكتبات بالإصدارات الدقيقة من `requirements.txt`.
- تسجيل كيرنل جوبيتر `Python (X-IDS Machine Learning)`.
- فتح مجلد المشروع مباشرة داخل VS Code.

### الخطوات:
1. تأكد من تثبيت **Python (3.8 إلى 3.11)** مع تفعيل خيار `Add Python to PATH`.
2. اضغط مرتين (Double Click) على الملف:
   ```text
   setup.bat
   ```
3. انتظر انتهاء التثبيت، وسيفتح VS Code تلقائياً.
4. افتح النوت بوك الأساسي:
   ```text
   my_model_training.ipynb
   ```
5. من أعلى يمين الشاشة اضغط على **Select Kernel** ثم اختر:
   ```text
   Python (X-IDS Machine Learning)
   ```
6. اضغط على **Run All** وابدأ العمل مباشرة!

---

## 2. ☁️ الخيار الثاني: التشغيل السحابي عبر GitHub Codespaces (1-Click Cloud)

إذا كنت تستخدم جهازاً بمواصفات محدودة أو نظاماً لا تود تثبيت المكتبات عليه، يمكنك تشغيل بيئة العمل بالكامل على سيرفرات GitHub السحابية مجاناً:

### الخطوات:
1. افتح مستودع المشروع على **GitHub**.
2. اضغط على الزر الأخضر **`<> Code`**.
3. انتقل إلى تبويب **Codespaces**.
4. اضغط على **`Create codespace on main`**.
5. سيقوم GitHub تلقائياً بقراءة تكوين `.devcontainer/devcontainer.json`:
   - بناء حاوية Docker مبنية على Python 3.10.
   - تثبيت كافة الحزم والمكتبات المعرفة في `requirements.txt`.
   - تثبيت إضافات VS Code الأساسية للذكاء الاصطناعي و Jupyter.
   - تهيئة الكيرنل.
6. سيفتح لك VS Code داخل المتصفح (أو يمكنك ربطه بتطبيق VS Code المكتبي).
7. افتح `my_model_training.ipynb` واضغط **Run All** فوراً!

---

## 3. 🛠️ الخيار الثالث: التشغيل اليدوي (Manual Setup)

إذا كنت تفضل استخدام التيرمينال أو تعمل على نظام **Linux** أو **macOS**:

### على أنظمة Linux / macOS:
```bash
# 1. إنشاء البيئة الافتراضية
python3 -m venv .venv

# 2. تفعيل البيئة
source .venv/bin/activate

# 3. تحديث pip وتثبيت الحزم
pip install --upgrade pip
pip install -r requirements.txt

# 4. تسجيل كيرنل Jupyter في النظام
python -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)"
```

### على نظام Windows (عبر PowerShell أو CMD):
```powershell
# 1. إنشاء البيئة وتفعيلها
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. تثبيت الحزم المسجلة
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. تسجيل كيرنل Jupyter
python -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)"
```

---

## 📦 حزم المشروع المثبتة (Pinned Dependencies)

تم تثبيت إصدارات دقيقة في `requirements.txt` لضمان عدم حدوث أي تعارضات برمجية بين أعضاء الفريق:

| الحزمة | الإصدار المثبت | الاستخدام في المشروع |
| :--- | :---: | :--- |
| **pandas** | `2.0.3` | قراءة ومعالجة جداول شبكة CIC-IDS2017 وتجهيز الـ DataFrames |
| **numpy** | `1.24.4` | العمليات المصفوفية الرياضية السريعة والتعامل مع الأرقام |
| **scikit-learn** | `1.3.2` | تقسيم البيانات (Train/Test) ونماذج Random Forest ومقاييس الأداء |
| **xgboost** | `2.1.4` | تدريب نموذج أشجار القرار المعززة ومعالجة عدم توازن الفئات |
| **shap** | `0.44.1` | تفسير قرارات الذكاء الاصطناعي (XAI) وحساب SHAP Values |
| **matplotlib** | `3.7.5` | رسم المخططات البيانية الأساسية ونتائج الموديل |
| **seaborn** | `0.13.2` | رسم مصفوفات الارتباك (Confusion Matrices) الملونة |
| **jupyter** | `1.0.0` | بيئة الدفاتر التفاعلية |
| **ipykernel** | `6.29.5` | محرك تشغيل الخلايا داخل VS Code |
| **edge-tts** | `7.3.1` | توليد التعليق الصوتي لملخصات المشروع والعروض التقديمية |
| **python-docx** | `1.1.2` | التوليد التلقائي لتقارير Word الشاملة |
| **python-pptx** | `1.0.2` | التوليد التلقائي لشرائح PowerPoint التفاعلية |

---

## 📂 خريطة ملفات المشروع الرئيسية

```text
project/
├── .devcontainer/
│   └── devcontainer.json        # تكوين البيئة السحابية الجاهزة لـ GitHub Codespaces
├── Dataset/                     # الداتا سيت الكاملة أو العينات المسحوبة
├── data/
│   └── cic_ids2017_sample.csv   # عينة بيانات نظيفة لمحاكاة التدريب
├── presentation/                # العروض التقديمية وشرائح المناقشة
├── Reports/                     # التقارير الشاملة التوثيقية
├── .venv/                       # البيئة الافتراضية (يتم إنشاؤها تلقائياً بعد التشغيل)
├── requirements.txt             # ملف الحزم بالإصدارات المثبتة
├── setup.bat                    # سكريبت التثبيت التلقائي لويندوز بنقرة واحدة
├── TEAM_GUIDE.md                # هذا الدليل الإرشادي للفريق
├── my_model_training.ipynb      # الدفتر الرئيسي للتدريب والتقييم واختبار الـ SHAP
├── x_ids_pipeline.py            # خط الأنابيب البرمجي الكامل للتدريب والتقييم
└── README.md                    # وثيقة المشروع الفنية
```

---

## ❓ حل المشاكل الشائعة (Troubleshooting)

### 1. رسالة `python is not recognized` في ويندوز:
- **السبب**: بايثون غير مضاف إلى متغيرات النظام `PATH`.
- **الحل**: أعد تثبيت بايثون من [python.org](https://www.python.org/) وتأكد من تفعيل علامة الصح بجانب **"Add Python to PATH"** في أول شاشة تثبيت.

### 2. الكيرنل `Python (X-IDS Machine Learning)` لا يظهر في VS Code:
- اضغط `Ctrl + Shift + P` داخل VS Code.
- اكتب: `Developer: Reload Window` واضغط Enter.
- افتح `my_model_training.ipynb` مرة أخرى واضغط على **Select Kernel** -> **Jupyter Kernel...** وستجده متاحاً.

### 3. خطأ `ExecutionPolicy` عند تشغيل PowerShell:
- إذا واجهت رسالة تمنع تشغيل السكريبتات في PowerShell، نفذ الأمر التالي مرة واحدة بصلاحية مسؤول:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

---
*تم إعداد وتجهيز البيئة لضمان تجربة تشغيل موحدة وخالية من المشاكل لجميع أعضاء الفريق.*
