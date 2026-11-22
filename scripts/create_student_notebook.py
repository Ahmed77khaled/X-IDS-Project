import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🛡️ تدريب موديل كشف التسلل (Network IDS) - من البداية للنهاية\n",
    "### الدفتر ده معمول عشان تكتب كل سطر كود بإيدك وتدرب الموديل بنفسك خطوة بخطوة 🚀\n",
    "\n",
    "**ملاحظة:** البيئة متجهزة بالكامل وكل المكتبات (`pandas`, `numpy`, `sklearn`, `xgboost`, `shap`, `seaborn`) متسطبة وتقدر تشتغل **أوفلاين بدون نت**."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1️⃣ استدعاء المكتبات (Import Libraries)\n",
    "اكتب هنا استدعاء مكتبات `pandas`, `numpy`, `sklearn`, `matplotlib` وأي مكتبة هتحتاجها:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود استدعاء المكتبات هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2️⃣ تحميل واستكشاف البيانات (Load & Inspect Dataset)\n",
    "اقرأ ملف الـ CSV وشوف شكله الأولي (`shape`, `head`, `info`):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود قراءة ملف الـ CSV هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3️⃣ فحص وتجهيز البيانات (Data Cleaning)\n",
    "- افحص القيم المكررة (`duplicated`) واحذفها.\n",
    "- استبدل قيم `np.inf` بقيم `np.nan`.\n",
    "- عوّض القيم الفاضية (Missing / Nulls) بالوسيط (`median`) أو احذفها."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود تنظيف البيانات ومعالجة الـ Nulls والـ Infs هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4️⃣ منع الـ Data Leakage (حذف معرّفات الـ Network والـ IPs)\n",
    "احذف الأعمدة اللي ممكن الموديل يحفظها (زي `Flow ID`, `Source IP`, `Destination IP`, `Timestamp`, إلخ):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود حذف أعمدة الـ Sockets والـ Timestamps هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 5️⃣ فصل المدخلات والهدف (Extract X & y) وتقسيم البيانات (Train / Test Split)\n",
    "افصل الـ Features ($X$) عن الـ Target ($y$) وقسّمهم لـ `train` و `test`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود تحديد X و y وعمل train_test_split هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 6️⃣ تقييس البيانات (Feature Scaling)\n",
    "طبق `StandardScaler` على `X_train` فقط وطبقه على `X_test`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود الـ StandardScaler هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 7️⃣ بناء وتدريب الموديل (Model Training)\n",
    "اختار الموديل اللي تحبه (Random Forest, Decision Tree, XGBoost, etc.) ودرّبه (`model.fit`):"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود بناء وتدريب الموديل هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 8️⃣ تقييم أداء الموديل (Evaluation Metrics)\n",
    "احسب `Accuracy`, `Precision`, `Recall`, `F1-Score` ومصفوفة الارتباك `Confusion Matrix`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# اكتب كود التقييم وحساب الـ Metrics هنا\n",
    ""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 9️⃣ شرح القرارات بـ SHAP (Explainable AI - اختياري)\n",
    "طبق `shap.TreeExplainer` عشان تشوف أنهي Features كان ليها أكبر تأثير في كشف الهجوم:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# كود الـ SHAP التفسيري\n",
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

with open(r"C:\Users\msi\.gemini\antigravity\scratch\x-ids\my_model_training.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)
print("Student notebook created!")
