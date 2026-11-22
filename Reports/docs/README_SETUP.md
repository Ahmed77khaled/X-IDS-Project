# 🛡️ دليل تشغيل وتجهيز مشروع X-IDS (دليل فريق العمل)
### X-IDS: Team Setup & Quickstart Guide

مرحباً بك في مستودع مشروع **X-IDS (Explainable Network Intrusion Detection System)**.  
هذا الدليل مجهز لمساعدتك في تشغيل المشروع وبدء تدريب النماذج والاستماع إلى الشرح الصوتي في **أقل من دقيقتين** باختيار إحدى الطرق الثلاث التالية:

---

## ⚡ طرق التشغيل (3 طرق، اختر الأنسب لك):

```
                       ┌─────────────────────────────┐
                       │   اختر طريقة التشغيل المناسبة  │
                       └──────────────┬──────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│  1. Codespaces   │        │ 2. DevContainer  │        │  3. setup.bat    │
│  سحابي بالكامل    │        │ Docker محلي      │        │  ويندوز 1-Click  │
│  بدون تثبيت أي شيء│        │ بيئة معزولة تماماً│        │  أو بايثون محلي  │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

---

### ☁️ الطريقة 1: GitHub Codespaces (تشغيل سحابي فوري بنقرة واحدة - موصى به)
> **ميزة هذه الطريقة:** تعمل على أي جهاز (حتى لو ضعيف أو تابلت) دون الحاجة لتثبيت أي برامج محلياً.

1. ادخل على صفحة المستودع على **GitHub**.
2. اضغط على الزر الأخضر **`<> Code`** ثم اختر تبويب **`Codespaces`**.
3. اضغط على **`Create codespace on main`**.
4. سيتم تلقائياً قراءة إعدادات الحاوية السحابية من `.devcontainer/devcontainer.json`:
   - تثبيت بيئة **Python 3.10**.
   - تثبيت كافة حزم ومكتبات المشروع من `requirements.txt`.
   - تثبيت إضافات VS Code و Jupyter.
   - تسجيل الكيرنل: `Python (X-IDS Machine Learning)`.
5. فور اكتمال التجهيز، سيفتح لك محرر VS Code داخل المتصفح. افتح الدفتر الأساسي:
   ```text
   my_model_training.ipynb
   ```
6. من أعلى اليمين اختر الكيرنل **`Python (X-IDS Machine Learning)`** واضغط **Run All**!

---

### 🐳 الطريقة 2: VS Code + Docker (Dev Containers محلياً)
> **ميزة هذه الطريقة:** توفر بيئة Linux مطابقة تماماً لسيرفرات الإنتاج وتمنع أي تعارض في مكتبات النظام.

1. تأكد من تشغيل **Docker Desktop** على جهازك.
2. ثبّت إضافة **Dev Containers** في برنامج VS Code.
3. افتح مجلد المشروع في VS Code:
   - ستظهر لك نافذة في الزاوية تطلب: `Reopen in Container`، اضغط عليها.
   - أو اضغط `F1` واكتب: `Dev Containers: Reopen in Container`.
4. سيقوم Docker ببناء البيئة وتثبيت كل المتطلبات تلقائياً داخل الحاوية.
5. افتح `my_model_training.ipynb` وابدأ التدريب فوراً.

---

### 💻 الطريقة 3: التشغيل المحلي على جهازك (Local Python / setup.bat)

#### أ) لمستخدمي نظام ويندوز (1-Click Windows Setup):
1. تأكد من تثبيت Python (3.8 إلى 3.11) مع تحديد خيار `Add Python to PATH`.
2. اضغط مرتين (Double Click) على الملف التنفيذي:
   ```text
   setup.bat
   ```
3. سيقوم السكريبت تلقائياً بـ:
   - فحص بايثون وإنشاء البيئة الافتراضية المنعزلة `.venv`.
   - تحديث `pip` وتثبيت كافة الحزم من `requirements.txt`.
   - تسجيل كيرنل جوبيتر `Python (X-IDS Machine Learning)`.
   - فتح VS Code تلقائياً داخل مجلد المشروع.

#### ب) التشغيل اليدوي عبر سطر الأوامر (Windows / Linux / macOS):
```bash
# 1. إنشاء البيئة الافتراضية
python -m venv .venv

# 2. تفعيل البيئة:
# على ويندوز (CMD / PowerShell):
.venv\Scripts\activate
# على لينكس / ماك:
source .venv/bin/activate

# 3. تحديث pip وتثبيت المتطلبات:
pip install --upgrade pip
pip install -r requirements.txt

# 4. تسجيل كيرنل Jupyter:
python -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)"
```

---

## 📊 فحص وتجهيز الداتا سيت (Dataset Verification)

المشروع يعتمد على عينة بيانات يوم الأربعاء من داتا سيت **CIC-IDS2017 Improved** (`wednesday.csv`).
لقد أعددنا أداة فحص ذكية للتحقق من سلامة البيانات:

```bash
# فحص الداتا سيت والتأكد من عدد الأسطر والأعمدة
python download_data.py

# فك ضغط الأرشيف تلقائياً في حال وجود CICIDS2017_improved.zip
python download_data.py --extract

# عرض روابط التحميل الرسمية والمصادر
python download_data.py --info

# توليد عينة خفيفة (Sample) للاختبار السريع بدون الداتا سيت الكاملة
python download_data.py --sample
```

---

## 🎧 الاستماع إلى الشرح الصوتي للخطوات (listen() Helper)

جميع ملفات التعليق الصوتي باللهجة المصرية التقنية الطبيعية تم توليدها مسبقاً وحفظها في مجلد `audio/`:
- `audio/step1.mp3` إلى `audio/step9.mp3`
- **لا تحتاج لتثبيت أي مكتبات صوت إضافية للاستماع!**

### الاستماع التفاعلي داخل أي Notebook:
1. تم دمج مشغل صوتي أنيق في بطاقة كل خطوة داخل `my_model_training.ipynb`.
2. كما يمكنك تشغيل الصوت من أي خلية كود برمجياً باستخدام الدالة المساعدة `listen()`:

```python
from IPython.display import Audio, display
from pathlib import Path

def listen(step):
    """
    دالة مساعدة للاستماع للشرح الصوتي لأي خطوة في المشروع.
    أمثلة:
      listen(1)         # تشغيل خطوة 1 (استيراد المكتبات)
      listen("step2")   # تشغيل خطوة 2 (تحميل الداتا سيت)
    """
    step_str = str(step).strip().lower()
    if not step_str.startswith("step"):
        step_str = f"step{step_str}"
    if not step_str.endswith(".mp3"):
        step_str = f"{step_str}.mp3"
    
    # البحث عن مسار الصوت من المجلد الحالي أو المجلد الأب
    candidates = [
        Path("audio") / step_str,
        Path("../audio") / step_str,
        Path("project/audio") / step_str
    ]
    for p in candidates:
        if p.exists():
            display(Audio(str(p)))
            return
    print(f"⚠️ لم يتم العثور على ملف الصوت: {step_str}")

# مثال: استمع لشرح الخطوة الأولى
listen(1)
```

---

## 🎙️ تعديل وتوليد ملفات الصوت (صاحب المشروع / المطور فقط)

إذا أردت تعديل النصوص أو إعادة توليد ملفات الصوت، يمكنك تثبيت أدوات التوليد عبر:
```bash
pip install -r requirements-audio.txt
python audio/generate_audio.py
```
- النصوص البرمجية الصوتية موجودة في: `audio/scripts/`
- قاموس النطق التقني الصوتي موجود في: `audio/pronunciation.json`

---

## ❓ المشاكل الشائعة وحلولها (Troubleshooting)

1. **الكيرنل لا يظهر في القائمة:**
   - اضغط `Ctrl + Shift + P` (أو `Cmd + Shift + P` على ماك).
   - اكتب: `Developer: Reload Window`.
   - أعد فتح النوت بوك واضغط **Select Kernel** وستجد `Python (X-IDS Machine Learning)`.

2. **الداتا سيت غير موجودة عند تشغيل الخلية:**
   - تأكد من وجود ملف `Dataset/CICIDS2017_improved/wednesday.csv`.
   - شغّل أمر: `python download_data.py` للتحقق التلقائي والتشخيص السريع.

---
*نتمنى لكم تجربة عمل ممتعة وتدريباً ناجحاً لفريق X-IDS! 🚀*
