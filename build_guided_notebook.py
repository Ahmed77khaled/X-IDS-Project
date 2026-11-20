import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🛡️ مشروع X-IDS: كشف اختراقات الشبكة بالذكاء الاصطناعي\n",
    "## 🎓 دفتر التدريب التفاعلي الموجه (Guided Hands-on Workbook)\n",
    "\n",
    "أهلاً بك يا بطل! الدفتر ده معمول خصيصاً عشان تكون **أنت اللي بتكتب كل سطر كود بإيدك** من الصفر، وفي نفس الوقت تكون فاهم كل خطوة بتعملها نظرياً وعملياً.\n",
    "\n",
    "### 📌 نظام العمل في كل خطوة:\n",
    "1. **🎥 فيديو يوتيوب محدد:** تخش تتفرج على الدقائق أو المفهوم المشروح فيه الأول.\n",
    "2. **🧠 نقاط لازم تفهمها وتركز فيها:** ليه بنعمل الخطوة دي تحديداً في شبكات الـ Intrusion Detection؟\n",
    "3. **💻 المهمة البرمجية:** تكتب الكود المطلوب بنفسك في الخلية الفاضية وتنفذه بـ `Shift + Enter`.\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1️⃣ الخطوة الأولى: استدعاء المكتبات البرمجية (Import Libraries)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Python Data Analysis (قائمة يوتيوب)](https://www.youtube.com/playlist?list=PLdDo53W10MXs)\n",
    "* **شاهد فيديو:** مقدمة المكتبات والتعامل مع `Pandas` و `NumPy`.\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* **`pandas`:** المكتبة الأساسية للتعامل مع الجداول (DataFrames)، هنستخدمها لقراءة وتحليل ملفات الـ CSV.\n",
    "* **`numpy`:** بنحتاجها عشان العمليات الرياضية السريعة والتعامل مع القيم اللانهائية (`np.inf`) والمفقودة (`np.nan`).\n",
    "* **`matplotlib.pyplot`:** بنستدعيها لتجهيز أدوات الرسم البياني عشان نرسم الجداول ونشوف الإحصائيات.\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "اكتب كود استدعاء المكتبات الثلاثة واطبع رسالة نجاح:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. اكتب كود استدعاء المكتبات (pandas, numpy, matplotlib.pyplot) هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 2️⃣ الخطوة الثانية: قراءة ملف الداتا سيت ومعرفة أبعادها (Load Dataset & Shape)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Pandas DataFrames & Reading CSVs](https://www.youtube.com/playlist?list=PLdDo53W10MXs)\n",
    "* **شاهد فيديو:** قراءة ملفات الـ CSV باستخدام `read_csv` ودراسة خصائص الـ DataFrame (`shape`, `columns`).\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* إحنا هنقرأ ملف بيانات يوم الأربعاء من المسار: `Dataset/CICIDS2017_improved/wednesday.csv`.\n",
    "* ملفات داتا سيت CIC-IDS2017 أحياناً بيكون فيها مسافات زيادة قبل أو بعد أسماء الأعمدة (مثل `' Label'` بدلاً من `'Label'`)، فلازم بعد القراءة ننضف أسماء الأعمدة باستخدام: `df.columns = df.columns.str.strip()`.\n",
    "* خاصية `df.shape` بترجع رقمين: الأول هو عدد الصفوف (عدد الـ Network Flows) والتاني هو عدد الأعمدة (الخصائص).\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "اقرأ ملف الـ CSV في متغير اسمه `df` ونضف أسماء الأعمدة واطبع الـ `shape`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. اكتب كود قراءة ملف wednesday.csv وتنظيف أسماء الأعمدة وطباعة df.shape هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 3️⃣ الخطوة الثالثة: استعراض أول 5 سطور من البيانات (First 5 Rows - `head`)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Exploring Data with head()](https://www.youtube.com/playlist?list=PLdDo53W10MXs)\n",
    "* **شاهد فيديو:** استعراض بدايات ونهايات الجداول في بايثون.\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* دالة `df.head(5)` بتعرض أول 5 تدفقات شبكية تم تسجيلها في بداية اليوم.\n",
    "* ركز في أسماء الأعمدة وشوف طبيعة الأرقام: هل هي أزمنة؟ أحجام حزم؟ أعلام شبكة؟\n",
    "* في أغلب مجموعات بيانات الشبكة، حركة المرور في بداية الملف بتكون حركة طبيعية وسليمة (`BENIGN`).\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "اكتب دالة استعراض أول 5 سطور:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. اكتب كود عرض أول 5 سطور باستخدام head(5) هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 4️⃣ الخطوة الرابعة: استعراض آخر 5 سطور من البيانات (Last 5 Rows - `tail`)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Exploring Data with tail()](https://www.youtube.com/playlist?list=PLdDo53W10MXs)\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* دالة `df.tail(5)` بتعرض آخر 5 سجلات في نهاية الملف.\n",
    "* في داتا سيت يوم الأربعاء (Wednesday)، المهاجمون بدأوا شن هجمات حجب الخدمة (DoS Slowloris) في الجزء الأخير من اليوم، فلما تشغل `tail()` هتلاحظ إن قيم عمود `Label` بقت هجمات وليست حركة طبيعية!\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "اكتب دالة استعراض آخر 5 سطور:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. اكتب كود عرض آخر 5 سطور باستخدام tail(5) هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 5️⃣ الخطوة الخامسة: تحديد المدخلات والهدف (Features vs Target)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الفيديو:** [Step-by-Step ML Project: Inputs and Outputs](https://classcentral.com/classroom/youtube-ml-series-step-by-step-ml-project-implementation-eda-fe-feature-selection-model-training-day10-207653)\n",
    "* **شاهد الجزء الخاص بـ:** فهم وتحديد المتغير التابع (Target / Label) والمتغيرات المستقلة (Features / Inputs).\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* **الهدف (Target / Output - $y$):** هو عمود `Label` فقط، ومهم تفحص توزيعه بالدالة السحرية `value_counts()` عشان تعرف كام هجوم حصل في اليوم وكام حركة طبيعية.\n",
    "* **المدخلات (Features / Inputs - $X$):** هي كل الأعمدة التانية ما عدا عمود `Label` (يعني بنعمل له drop من الـ Features).\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "1. اطبع توزيع الفئات في عمود `Label` باستخدام `df['Label'].value_counts()`.\n",
    "2. افصل المدخلات `X` والهدف `y` واطبع أبعاد كل واحد منهم:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. اكتب كود استعراض توزيع فئات Label وفصل X و y هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 6️⃣ الخطوة السادسة: فحص القيم الشاذة (Infinity) والقيم المفقودة (Nulls)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Handling Missing Values & Data Cleaning](https://www.youtube.com/playlist?list=PLUD2gKdRqrQE)\n",
    "* **شاهد فيديو:** فحص واستكشاف القيم المفقودة `isnull().sum()`.\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* في بيانات تدفق الشبكات، أداة الاستخراج (CICFlowMeter) لما بتيجي تحسب معدل البايتات في الثانية (`Flow Bytes/s = Bytes / Duration`) ولو كان زمن الاتصال 0، عملية القسمة على صفر بتطلع قيمة `Infinity` في بايثون!\n",
    "* بايثون مش بيعتبر `Infinity` قيمة فارغة تلقائياً، فلازم خطوة إجبارية نحول الـ `np.inf` و `-np.inf` إلى `np.nan` عشان نعرف نحذفها أو نعوضها.\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "1. استبدل قيم `np.inf` و `-np.inf` بقيم `np.nan` في الداتا.\n",
    "2. احسب إجمالي القيم الفارغة في الأعمدة باستخدام `isnull().sum()`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 6. اكتب كود استبدال قيم inf بقيم nan وفحص عدد الـ nulls هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 7️⃣ الخطوة السابعة: المهمة 5 - حذف الصفوف التي تحتوي على قيم فارغة (`dropna`)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Dropping Missing Data](https://www.youtube.com/playlist?list=PLUD2gKdRqrQE)\n",
    "* **شاهد فيديو:** استخدام دالة `dropna()` لحذف الصفوف الفاسدة.\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* دالة `df.dropna()` بتمشي على الجدول سطر سطر، وأي سطر تلاقي فيه خانة واحدة فاضية أو فاسدة بتمسحه كله.\n",
    "* **الميزة:** الداتا اللي باقية بتضمن إنها نقية 100% ومفيهاش أي قيم مفترضة.\n",
    "* **الخطر:** لو الهجمات أصلاً عددها قليل وكان فيها قيم مفقودة، ممكن الحذف يمسح عينات نادرة محتاجينها.\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "طبق `dropna()` في متغير جديد اسمه `df_dropped` واطبع عدد الصفوف قبل الحذف وبعد الحذف:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7. اكتب كود تطبيق dropna ومقارنة عدد الصفوف قبل وبعد الحذف هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 8️⃣ الخطوة الثامنة: المهمة 6 - تعويض القيم الفارغة بالوسيط الحسابي (`fillna`)\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الكورس:** [Zero Grad – Imputation Methods (Mean vs Median)](https://www.youtube.com/playlist?list=PLUD2gKdRqrQE)\n",
    "* **شاهد فيديو:** تعويض القيم المفقودة باستخدام دالة `fillna()`.\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* **ليه بنستخدم الوسيط (Median) مش المتوسط (Mean) في بيانات الـ Network؟**\n",
    "  لأن الشبكة بيكون فيها حزم عادية جداً (مثلاً 50 بايت) وفجأة هجوم DoS يبعت حزمة ضخمة جداً (Outlier). المتوسط بيتأثر جداً بالقيم المتطرفة دي وبيطلع رقم مشوه، بينما الوسيط بيعبر عن القيمة الوسطية الحقيقية للداتا.\n",
    "* دالة `fillna(df[col].median())` بتملأ أي خانة فاضية بقيمة الوسيط الحسابي للعمود.\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "طبق دالة `fillna` بالوسيط الحسابي على الأعمدة الرقمية وتأكد إن مابقاش عندك أي قيم فارغة:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 8. اكتب كود تعويض القيم الفارغة بالوسيط باستخدام fillna هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "### 🌟 الخطوة التاسعة (إضافة احترافية): منع الـ Data Leakage ومعالجة الـ Attempted\n",
    "\n",
    "#### 🎥 الفيديو المطلوب مشاهدته أولاً:\n",
    "* **الفيديو الحاسم:** [Kaggle 30 Days of ML: XGBoost and Data Leakage](https://rosetta.to/u/1littlecoder/kaggle-30-days-of-ml-day-14-xgboost-data-leakage-learn-python-ml-in-30-days)\n",
    "\n",
    "#### 🧠 نقاط لازم تفهمها وتكون في بالك وأنت شغال:\n",
    "* **أخطر غلطة بيقع فيها 90% من الطلاب:** إنهم بيسيبوا أعمدة زي `Source IP` و `Destination IP` و `Timestamp` و `Source Port` جوه الـ Features. الموديل كدة مش بيتعلم يعني إيه هجوم، ده بيحفظ أرقام الـ IPs بتاعة أجهزة المعمل بس! أول ما يخرج للواقع يفشل.\n",
    "* لازم نحذف أعمدة الـ Sockets والوقت دي فوراً قبل أي تدريب.\n",
    "* **فئات الـ Attempted:** محاولات الهجوم الفاشلة طبقا لأبحاث CIC-IDS2017 Improved بنعيد تصنيفها كـ `BENIGN` لأنها لم تؤدِ لاختراق فعلي.\n",
    "\n",
    "#### 💻 مهمتك الآن:\n",
    "احذف أعمدة الـ Sockets وأعد تعيين حالات الـ Attempted كـ BENIGN:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 9. اكتب كود حذف أعمدة التسريب (IPs, Ports, Timestamp) ومعالجة Attempted هنا:\n",
    ""
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open(r"D:\HIE\AI\05 - ملخصات ومشاريع (Summaries & Labs)\project\my_model_training.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)
print("Interactive Guided Notebook built successfully!")
