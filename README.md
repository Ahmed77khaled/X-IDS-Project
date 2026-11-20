# 🛡️ مشروع X-IDS: كشف اختراقات الشبكة وتفسير القرارات بالذكاء الاصطناعي
### Explainable Network Intrusion Detection System (X-IDS)

مشروع عملي متكامل لتطبيق التعلم الآلي وتفسير القرارات (XAI) على شبكات كشف ومنع التسلل (IDS / IPS)، متوافق علمياً مع داتا سيت **CIC-IDS2017 Improved** (ورقة Engelen et al. 2021).

---

## 📁 محتويات مجلد المشروع
```text
x-ids/
├── data/
│   └── cic_ids2017_sample.csv       # عينة بيانات واقعية تحاكي الداتا سيت بالكامل
├── x_ids_colab_notebook.ipynb       # دفتر تفاعلي (Notebook) جاهز للتشغيل في VS Code أو كولاب
├── x_ids_pipeline.py               # كود بايثون متكامل لتشغيل كل المراحل دفعة واحدة
├── generate_sample_dataset.py      # سكريبت لتوليد عينات اختبار متوافقة
├── shap_feature_importance.png     # مخطط أهم الخصائص المؤثرة بـ SHAP
└── README.md                       # دليل التشغيل والمواصفات
```

---

## ⚙️ التجهيزات التي تمت على جهازك بنجاح
تم تسطيب جميع المكتبات والأدوات الناقصة على بيئة بايثون الخاصة بك:
- ✅ **Scikit-Learn**: لتقسيم البيانات والـ Preprocessing والـ Random Forest ومقاييس التقييم.
- ✅ **XGBoost**: لتدريب أشجار القرار المعززة ومعالجة عدم توازن الفئات (`scale_pos_weight`).
- ✅ **SHAP**: لحساب التفسير الرياضي للقرارات (`TreeExplainer`).
- ✅ **Seaborn & Matplotlib**: لرسم مصفوفات الارتباك ومخططات التأثير.
- ✅ **IPyKernel**: لتشغيل ملفات الـ `.ipynb` كـ Notebook تفاعلي داخل VS Code مباشرة مثل Google Colab.

---

## 🚀 طريقة التشغيل

### الطريقة الأولى: التشغيل كـ Notebook داخل VS Code (زي كولاب تماماً)
1. افتح VS Code.
2. من قائمة `File` اختر `Open Folder` وحدد المسار:
   `C:\Users\msi\.gemini\antigravity\scratch\x-ids`
3. افتح الملف: `x_ids_colab_notebook.ipynb`.
4. من الزاوية العلوية يميناً في المحرر، اضغط على **Select Kernel** واختر مفسر بايثون المثبت على جهازك:
   `Python 3.8.2 ('base')` أو مساره `C:\Users\msi\AppData\Local\Programs\Python\Python38\python.exe`.
5. اضغط على **Run All** أو شغّل الخلايا واحدة تلو الأخرى بالترتيب لتشاهد النتائج والرسومات التفاعلية.

### الطريقة الثانية: التشغيل السريع عبر سطر الأوامر (Terminal)
افتح التيرمينال واكتب:
```bash
python x_ids_pipeline.py
```

---

## 📌 القواعد والضوابط المطبقة (Best Practices):
1. **معالجة Attempted Labels**: تم التعامل مع محاولات الهجوم غير المكتملة وإعادة توجيهها أو استبعادها وفقاً لتوصيات الورقة البحثية.
2. **منع Data Leakage**: تم إزالة معرّفات الشبكة (`Flow ID`, `Source IP`, `Destination IP`, `Source Port`, `Timestamp`) حتى لا يحفظ الموديل أرقام الـ IPs بل يتعلم السلوك.
3. **معالجة القيم الفاسدة**: استبدال الـ `Infinity` بـ `NaN` وحذف التكرارات وتعويض المفقود بالـ Median.
4. **تجاوز فخ الـ Accuracy**: قياس `Precision`, `Recall`, `F1-Score`, `ROC-AUC` لكل فئة بشكل مستقل.
5. **اختبار التعميم (Leave-One-Attack-Out)**: استبعاد هجوم معين بالكامل واختبار اكتشافه كـ Anomaly.
6. **التفسير بـ SHAP**: توضيح أي خصائص شبكية (مثل طول الحزم، معدل البايتات، زمن التدفق) هي المسؤولة عن اعتبار هذا الاتصال هجوماً.
