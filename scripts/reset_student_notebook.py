import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🛡️ مشروع X-IDS: كشف اختراقات الشبكة بالذكاء الاصطناعي\n",
    "### دفتر التدريب العملي الخاص بالطالب (من الصفر حتى التدريب الكامل)\n",
    "\n",
    "> **ملاحظة:** هذا الدفتر مخصص لك لتكتب كل سطر كود بيدك، وتنفذ المهام الستة المطلوبة خطوة بخطوة."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 1️⃣ استدعاء المكتبات (Import Libraries)\n",
    "**المطلوب منك:** استدعاء مكتبات `pandas`, `numpy`, `matplotlib.pyplot`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود استدعاء المكتبات هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 2️⃣ قراءة البيانات (Load Dataset)\n",
    "**المطلوب منك:** قراءة ملف البيانات `Dataset/CICIDS2017_improved/wednesday.csv` وعرض أبعاد الداتا (`shape`)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود قراءة ملف الـ CSV هنا وعرض shape:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 3️⃣ استعراض أول 5 سطور (First 5 Rows - `head`)\n",
    "**المطلوب منك:** إظهار أول 5 سطور من البيانات باستخدام دالة `head()`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود عرض أول 5 سطور هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 4️⃣ استعراض آخر 5 سطور (Last 5 Rows - `tail`)\n",
    "**المطلوب منك:** إظهار آخر 5 سطور من البيانات باستخدام دالة `tail()`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود عرض آخر 5 سطور هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 5️⃣ تحديد المدخلات والهدف (Features vs Target)\n",
    "**المطلوب منك:**\n",
    "1. استعراض توزيع فئات الهدف في عمود `Label` باستخدام `value_counts()`.\n",
    "2. فصل المدخلات `X` (حذف عمود Label) والهدف `y` (عمود Label فقط)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود فحص توزيع الفئات وتحديد X و y هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 6️⃣ فحص القيم الفارغة واللانهائية (Infs & Nulls)\n",
    "**المطلوب منك:**\n",
    "1. استبدال قيم `np.inf` و `-np.inf` بقيم `np.nan` في الأعمدة الرقمية.\n",
    "2. حساب عدد القيم الفارغة في كل عمود باستخدام `isnull().sum()`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود استبدال Infs وفحص الـ Nulls هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 7️⃣ المهمة 5: حذف الصفوف التي تحتوي على قيم فارغة (`dropna`)\n",
    "**المطلوب منك:** تطبيق دالة `dropna()` ومقارنة عدد الصفوف قبل وبعد الحذف."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود حذف القيم الفارغة بـ dropna هنا:\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 8️⃣ المهمة 6: ملء وتعويض القيم الفارغة (`fillna` بالوسيط)\n",
    "**المطلوب منك:** تعويض القيم الفارغة بقيمة الوسيط الحسابي (`median`) باستخدام دالة `fillna()`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود تعويض القيم الفارغة بـ fillna هنا:\n",
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
print("Student notebook is now completely clean and waiting for user code!")
