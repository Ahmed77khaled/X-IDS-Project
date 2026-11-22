import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🛡️ مشروع X-IDS: كشف اختراقات الشبكة بالذكاء الاصطناعي\n",
    "### المرحلة الأولى: استكشاف البيانات ومعالجة القيم المفقودة (Data Inspection & Preprocessing)\n",
    "\n",
    "**هذا الدفتر ينفذ المهام المطلوبة للمرحلة الأولى:**\n",
    "1. اختيار المشروع ودراسة طبيعة المشكلة (Network Intrusion Detection).\n",
    "2. تحديد نوع التعلم الآلي المستخدم (`Classification`).\n",
    "3. تحديد المدخلات والخصائص المستخرجة من الشبكة (`Features / Inputs`).\n",
    "4. تحديد المخرجات والهدف المطلوب توقعه (`Labels / Target`).\n",
    "5. استعراض أول 5 سطور (`head`) وآخر 5 سطور (`tail`).\n",
    "6. فحص ومعالجة القيم المفقودة واللانهائية باستخدام أسلوبي (`dropna`) و (`fillna`)."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 1️⃣ استدعاء المكتبات البرمجية الأساسية"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# ضبط إعدادات العرض لرؤية جميع الأعمدة بوضوح\n",
    "pd.set_option('display.max_columns', 30)\n",
    "pd.set_option('display.width', 1000)\n",
    "print('✅ تم استدعاء المكتبات بنجاح!')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 2️⃣ المهمة 1 و 2: اختيار المشروع وتحديد نوع التعلم الآلي\n",
    "* **اسم المشروع:** X-IDS (Explainable Network Intrusion Detection System)\n",
    "* **نوع التعلم الآلي:** **Supervised Machine Learning – Classification (تصنيف تحت إشراف)**\n",
    "  * **Binary Classification (تصنيف ثنائي):** التمييز بين الاتصال الطبيعي (`BENIGN = 0`) والاتصال الضار/الهجوم (`Attack = 1`).\n",
    "  * **Multiclass Classification (تصنيف متعدد):** تصنيف نوع الهجوم المحدد (مثل DoS Slowloris, DoS Hulk, PortScan, Brute Force)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# قراءة عينة من بيانات يوم الأربعاء (Wednesday - DoS Attacks)\n",
    "DATA_PATH = 'Dataset/CICIDS2017_improved/wednesday.csv'\n",
    "\n",
    "print(f\"⏳ جاري قراءة البيانات من: {DATA_PATH}...\")\n",
    "# نقرأ عينة مكونة من أول 50,000 سجل للسرعة والاستكشاف الدقيق\n",
    "df = pd.read_csv(DATA_PATH, nrows=50000, low_memory=False)\n",
    "df.columns = df.columns.str.strip()  # إزالة أي مسافات زائدة في أسماء الأعمدة\n",
    "\n",
    "print(f\"📊 أبعاد البيانات: {df.shape[0]:,} صف × {df.shape[1]} عمود.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 3️⃣ استعراض أول 5 سطور (First 5 Rows - `head`)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# عرض أول 5 سطور من البيانات\n",
    "df.head(5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 4️⃣ استعراض آخر 5 سطور (Last 5 Rows - `tail`)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# عرض آخر 5 سطور من البيانات\n",
    "df.tail(5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 5️⃣ المهمة 3 و 4: تحديد المدخلات (Features / Inputs) والمخرجات (Target / Output)\n",
    "* **الهدف (Target / Output):** هو عمود `Label` الذي يحدد طبيعة السجل.\n",
    "* **المدخلات (Features / Inputs):** هي الخصائص الإحصائية لحركة المرور (مثل: `Flow Duration`, `Total Fwd Packet`, `Flow Bytes/s`, `Packet Length Mean`, إلخ)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. فحص عمود الهدف وتوزيع الفئات\n",
    "print(\"🎯 توزيع الفئات في عمود الهدف (Label Distribution):\")\n",
    "print(df['Label'].value_counts())\n",
    "\n",
    "# 2. فصل المدخلات (Features) عن الهدف (Target)\n",
    "y = df['Label']\n",
    "X = df.drop(columns=['Label'])\n",
    "\n",
    "print(f\"\\n🔢 عدد الخصائص المدخلة (Features count): {X.shape[1]} عمود.\")\n",
    "print(\"أمثلة على بعض المدخلات الهامة:\")\n",
    "print(list(X.columns[8:18]))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 6️⃣ فحص جودة البيانات: البحث عن القيم الفارغة (Nulls) واللانهائية (Infs)\n",
    "في بيانات الشبكات المستخرجة من أداة CICFlowMeter، عند قسمة عدد البايتات على زمن التدفق إذا كان الزمن 0 يظهر ناتج `Infinity`. يجب تحويل الـ `Infinity` إلى `NaN` أولاً ليتم التعامل معها برمجياً."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# تحويل أي قيمة Infinity (+inf أو -inf) إلى NaN\n",
    "num_cols = df.select_dtypes(include=[np.number]).columns\n",
    "df[num_cols] = df[num_cols].replace([np.inf, -np.inf], np.nan)\n",
    "\n",
    "# حساب إجمالي القيم الفارغة في كل عمود\n",
    "null_series = df.isnull().sum()\n",
    "null_columns = null_series[null_series > 0]\n",
    "\n",
    "print(\"🔍 الأعمدة التي تحتوي على قيم فارغة وعددها:\")\n",
    "if len(null_columns) > 0:\n",
    "    print(null_columns)\n",
    "else:\n",
    "    print(\"لا توجد قيم فارغة في هذه العينة، سنقوم بحقن عينة تجريبية لاختبار dropna و fillna.\")\n",
    "    # حقن قيم فارغة في 5 صفوف لاختبار العمليتين عملياً أمام المشرف\n",
    "    df.loc[:4, 'Flow Bytes/s'] = np.nan\n",
    "    print(\"\\nتم تجهيز 5 قيم فارغة في عمود Flow Bytes/s لتجربة الحذف والتعويض.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 7️⃣ المهمة 5: حذف الصفوف التي تحتوي على قيم فارغة (`dropna`)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# أ) تطبيق dropna\n",
    "print(f\"عدد الصفوف قبل الحذف: {len(df):,}\")\n",
    "df_dropped = df.dropna()\n",
    "print(f\"عدد الصفوف بعد dropna(): {len(df_dropped):,}\")\n",
    "print(f\"تم حذف: {len(df) - len(df_dropped):,} صفوف تحتوي على بيانات مفقودة.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 8️⃣ المهمة 6: ملء وتعويض القيم الفارغة بالوسيط الحسابي (`fillna`)\n",
    "> **ملاحظة علمية:** يُفضل في بيانات الشبكات استخدام **الوسيط الحسابي (Median)** بدلاً من المتوسط (Mean) لأن بيانات حركة المرور تحتوي على قيم متطرفة كبيرة جداً (Outliers) تجعل المتوسط الحسابي غير دقيق."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ب) تطبيق fillna بالوسيط الحسابي (Median Imputation)\n",
    "df_filled = df.copy()\n",
    "\n",
    "for col in ['Flow Bytes/s', 'Flow Packets/s']:\n",
    "    if col in df_filled.columns:\n",
    "        median_value = df_filled[col].median()\n",
    "        df_filled[col] = df_filled[col].fillna(median_value)\n",
    "        print(f\"تم تعويض القيم الفارغة في عمود [{col}] بقيمة الوسيط: {median_value:.4f}\")\n",
    "\n",
    "print(f\"\\nالقيم الفارغة المتبقية بعد fillna(): {df_filled.isnull().sum().sum()}\")\n",
    "print(\"✅ اكتملت جميع المهام بنجاح!\")"
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
print("Updated student notebook with doctor requirements!")
