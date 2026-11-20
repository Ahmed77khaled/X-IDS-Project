"""
=============================================================================
X-IDS: Explainable Network Intrusion Detection System
Pipeline & Model Training Engine
=============================================================================
بناءً على وثيقة مشروع X-IDS وداتا سيت CIC-IDS2017 Improved:
1. تنظيف البيانات (Missing Values, Infs, Duplicates, Zero-Variance).
2. منع الـ Data Leakage بحذف أعمدة الـ Sockets والـ Timestamps.
3. معالجة تصنيفات Attempted بحسب توصيات الباحثين.
4. فصل الـ Features عن الـ Target (X & y).
5. تدريب الموديلات (Random Forest & XGBoost) مع معالجة Class Imbalance.
6. التقييم الشامل (Precision, Recall, F1, ROC-AUC, Confusion Matrix).
7. اختبار التعميم (Leave-One-Attack-Out Evaluation).
8. التفسير بـ SHAP (Explainable AI).
=============================================================================
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import xgboost as xgb
import shap

class XIDSPipeline:
    def __init__(self, data_path="data/cic_ids2017_sample.csv"):
        self.data_path = data_path
        self.raw_df = None
        self.clean_df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.rf_model = None
        self.xgb_model = None
        self.feature_names = []

    def load_data(self):
        """تحميل الداتا سيت سواء كانت ملفاً واحداً أو عدة ملفات CSV"""
        print("\n" + "="*50)
        print("[1] Loading Dataset...")
        print("="*50)
        
        # فحص إذا كان المسار مجلد يحتوي على عدة ملفات CSV
        if os.path.isdir(self.data_path):
            csv_files = glob.glob(os.path.join(self.data_path, "*.csv"))
            if not csv_files:
                raise FileNotFoundError(f"لم يتم العثور على أي ملف CSV في المجلد: {self.data_path}")
            print(f"-> وجدنا {len(csv_files)} ملفات CSV، جاري الدمج...")
            dfs = [pd.read_csv(f, low_memory=False) for f in csv_files]
            self.raw_df = pd.concat(dfs, ignore_index=True)
        else:
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"الملف غير موجود: {self.data_path}")
            print(f"-> جاري قراءة الملف: {self.data_path}")
            self.raw_df = pd.read_csv(self.data_path, low_memory=False)

        # تنظيف المسافات البيضاء في أسماء الأعمدة (مشكلة شائعة في CIC-IDS2017)
        self.raw_df.columns = self.raw_df.columns.str.strip()
        print(f"-> حجم البيانات الأصلي: {self.raw_df.shape[0]:,} صف و {self.raw_df.shape[1]} عمود.")
        return self.raw_df

    def inspect_data(self):
        """فحص البيانات: القيم الفارغة، القيم اللانهائية، والتكرار"""
        print("\n" + "="*50)
        print("[2] Inspecting Data (فحص القيم الشاذة والمفقودة)...")
        print("="*50)
        
        df = self.raw_df
        # حساب التكرار
        dup_count = df.duplicated().sum()
        print(f"-> عدد الصفوف المكررة (Duplicates): {dup_count:,}")

        # حساب القيم الفارغة (NaN/Nulls)
        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        print(f"-> إجمالي القيم الفارغة (Null/NaN): {total_nulls:,}")

        # حساب قيم Infinity في الأعمدة الرقمية
        num_cols = df.select_dtypes(include=[np.number]).columns
        inf_counts = np.isinf(df[num_cols]).sum().sum()
        print(f"-> إجمالي قيم اللانهاية (np.inf / -np.inf): {inf_counts:,}")

        # توزيع الـ Labels
        print("\n-> توزيع الفئات (Target Distribution):")
        print(df['Label'].value_counts())
        return {
            'duplicates': dup_count,
            'nulls': total_nulls,
            'infs': inf_counts
        }

    def clean_data(self, handle_attempted='benign'):
        """
        تنظيف ومعالجة البيانات طبقاً لقواعد مشروع X-IDS:
        1. استبدال الـ Infs بقيم NaN ثم ملء القيم الفارغة بالـ Median
        2. حذف التكرارات
        3. حذف أعمدة الـ Identifiers لمنع الـ Data Leakage
        4. حذف الأعمدة الثابتة (Zero Variance)
        5. معالجة تصنيفات الـ Attempted
        """
        print("\n" + "="*50)
        print("[3] Cleaning & Preprocessing Data...")
        print("="*50)
        
        df = self.raw_df.copy()

        # أ) حذف التكرار
        initial_rows = len(df)
        df = df.drop_duplicates()
        print(f"-> تم حذف {initial_rows - len(df):,} صفوف مكررة.")

        # ب) استبدال الـ Infs بـ NaN
        num_cols = df.select_dtypes(include=[np.number]).columns
        df[num_cols] = df[num_cols].replace([np.inf, -np.inf], np.nan)

        # ج) معالجة الـ NaNs (تعويض القيم المفقودة بالـ Median لكل عمود)
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        print("-> تم استبدال الـ Infs والـ NaNs بالوسيط الحسابي (Median Imputation).")

        # د) منع الـ Data Leakage (حذف أسماء ومعرفات الشبكة والوقت)
        # هذه الأعمدة تجعل الموديل يحفظ IPs أو أوقات معينة ولا يتعلم سلوك الهجوم
        leakage_cols = [
            'Flow ID', 'Source IP', 'Src IP', 'Destination IP', 'Dst IP',
            'Source Port', 'Src Port', 'Timestamp', 'Unnamed: 0'
        ]
        cols_to_drop = [c for c in leakage_cols if c in df.columns]
        df = df.drop(columns=cols_to_drop)
        print(f"-> تم حذف أعمدة الـ Sockets والـ Timestamps لمنع الـ Data Leakage: {cols_to_drop}")

        # هـ) حذف الأعمدة الثابتة (Constant features ذات التباين الصفري)
        numeric_df = df.select_dtypes(include=[np.number])
        constant_cols = [col for col in numeric_df.columns if numeric_df[col].std() == 0]
        if constant_cols:
            df = df.drop(columns=constant_cols)
            print(f"-> تم حذف أعمدة ذات قيمة واحدة ثابتة (Zero Variance): {constant_cols}")

        # و) معالجة الـ Attempted Labels طبقاً لورقة Engelen et al. (Rule #1)
        # Attempted يعني محاولة هجوم لم تنجح، ولا تعتبر هجوماً مكتملاً
        if handle_attempted == 'benign':
            # إعادة تعيين Attempted كـ BENIGN
            df['Label'] = df['Label'].apply(lambda l: 'BENIGN' if 'Attempted' in str(l) else l)
            print("-> تم دمج الـ Attempted كـ BENIGN (لأنها محاولات غير ناجحة لا تمثل تهديداً مكتملاً).")
        elif handle_attempted == 'drop':
            # حذف حالات Attempted بالكامل
            df = df[~df['Label'].str.contains('Attempted', na=False)]
            print("-> تم استبعاد حالات Attempted بالكامل من الداتا سيت.")

        self.clean_df = df
        print(f"-> الحجم النهائي للبيانات النظيفة: {df.shape[0]:,} صف و {df.shape[1]} عمود.")
        return self.clean_df

    def prepare_features_and_target(self, binary=True, test_size=0.25):
        """
        استخراج الـ Features (X) والـ Target (y) وعمل Split مع حماية التوزيع (Stratified)
        """
        print("\n" + "="*50)
        print("[4] Splitting Features (X) and Target (y)...")
        print("="*50)

        df = self.clean_df.copy()
        
        if binary:
            # تصنيف ثنائي: 0 للـ BENIGN و 1 للهجمات (Attacks)
            y = df['Label'].apply(lambda l: 0 if str(l).strip().upper() == 'BENIGN' else 1).values
            print("-> الوضع المختار: Binary Classification (0: BENIGN, 1: Attack)")
        else:
            # تصنيف متعدد الفئات (Multi-class)
            y = self.label_encoder.fit_transform(df['Label'])
            print(f"-> الوضع المختار: Multi-class ({len(self.label_encoder.classes_)} Classes)")

        X = df.drop(columns=['Label'])
        # الاحتفاظ فقط بالأعمدة الرقمية
        X = X.select_dtypes(include=[np.number])
        self.feature_names = X.columns.tolist()

        # Stratified Split لمنع تشويه نسب الهجمات النادرة
        X_train_raw, X_test_raw, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # تطبيق StandardScaler فقط على الـ Train وتطبيقه على الـ Test لمنع تسريب الإحصائيات
        self.X_train = self.scaler.fit_transform(X_train_raw)
        self.X_test = self.scaler.transform(X_test_raw)

        print(f"-> بيانات التدريب (Train): {self.X_train.shape[0]:,} عينة")
        print(f"-> بيانات الاختبار (Test):  {self.X_test.shape[0]:,} عينة")
        print(f"-> عدد الـ Features المدخلة: {self.X_train.shape[1]}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_models(self):
        """
        تدريب نموذجين أساسيين لمقارنة الأداء:
        1. Random Forest (مع class_weight='balanced' لمواجهة عدم التوازن)
        2. XGBoost (مع scale_pos_weight لمواجهة الـ Imbalance)
        """
        print("\n" + "="*50)
        print("[5] Training Baseline & Tree Models...")
        print("="*50)

        # حساب وزن الفئات للـ XGBoost
        neg_count = np.sum(self.y_train == 0)
        pos_count = np.sum(self.y_train == 1)
        scale_pos = neg_count / max(pos_count, 1)

        # أ) Random Forest
        print("-> [A] تدريب Random Forest Classifier...")
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(self.X_train, self.y_train)
        print("   [Done] تم تدريب Random Forest بنجاح.")

        # ب) XGBoost
        print("-> [B] تدريب XGBoost Classifier...")
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos,
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        )
        self.xgb_model.fit(self.X_train, self.y_train)
        print("   [Done] تم تدريب XGBoost بنجاح.")

    def evaluate_model(self, model, model_name="Model"):
        """تقييم النموذج بمقاييس الأمان المتعددة (مش بس Accuracy)"""
        print(f"\n--- نتائج تقييم: {model_name} ---")
        y_pred = model.predict(self.X_test)
        
        # مقاييس الأداء
        acc = accuracy_score(self.y_test, y_pred)
        prec = precision_score(self.y_test, y_pred, zero_division=0)
        rec = recall_score(self.y_test, y_pred, zero_division=0)
        f1 = f1_score(self.y_test, y_pred, zero_division=0)
        
        try:
            y_proba = model.predict_proba(self.X_test)[:, 1]
            auc = roc_auc_score(self.y_test, y_proba)
        except Exception:
            auc = 0.0

        print(f"  • Accuracy:        {acc*100:.2f}%")
        print(f"  • Precision (الدقة): {prec*100:.2f}% (نسبة التنبيهات الصادقة)")
        print(f"  • Recall (الاكتشاف): {rec*100:.2f}% (نسبة الهجمات المكتشفة فعلياً)")
        print(f"  • F1-Score:        {f1*100:.2f}% (التوازن بين الدقة والاكتشاف)")
        print(f"  • ROC-AUC:         {auc:.4f}")
        
        print("\n  Classification Report:")
        print(classification_report(self.y_test, y_pred, digits=4))

        cm = confusion_matrix(self.y_test, y_pred)
        print(f"  Confusion Matrix:\n  TN={cm[0,0]} | FP={cm[0,1]}\n  FN={cm[1,0]} | TP={cm[1,1]}")
        return {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1': f1,
            'ROC_AUC': auc,
            'Confusion_Matrix': cm
        }

    def leave_one_attack_out_test(self, unseen_attack='PortScan'):
        """
        اختبار التعميم (Rule #3: Generalization - Leave-One-Attack-Out):
        نستبعد نوع هجوم معين من الـ Training نهائياً، وندرب الموديل،
        ثم نختبر هل الموديل يقدر يكتشف الهجوم ده كهجوم (Anomaly/Attack) رغم إنه ما شافهوش!
        """
        print("\n" + "="*50)
        print(f"[6] Leave-One-Attack-Out Test (استبعاد هجوم: {unseen_attack})...")
        print("="*50)

        df = self.clean_df.copy()

        # استبعاد الهجوم من التدريب
        train_df = df[~df['Label'].str.contains(unseen_attack, case=False, na=False)]
        test_df = df[df['Label'].str.contains(unseen_attack, case=False, na=False)]

        if len(test_df) == 0:
            print(f"-> الهجوم {unseen_attack} غير موجود في البيانات لتنفيذ الاختبار.")
            return

        # تدريب على باقي البيانات
        y_train_loao = train_df['Label'].apply(lambda l: 0 if str(l).strip().upper() == 'BENIGN' else 1).values
        X_train_loao = train_df.drop(columns=['Label']).select_dtypes(include=[np.number])
        
        # اختبار على الهجوم المستبعد (جميعها هجمات أي Ground Truth = 1)
        y_test_loao = np.ones(len(test_df), dtype=int)
        X_test_loao = test_df.drop(columns=['Label']).select_dtypes(include=[np.number])

        # مطابقة الأعمدة
        X_train_loao = X_train_loao[self.feature_names]
        X_test_loao = X_test_loao[self.feature_names]

        # تدريب موديل مخصص
        scaler = StandardScaler()
        X_tr = scaler.fit_transform(X_train_loao)
        X_te = scaler.transform(X_test_loao)

        loao_model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
        loao_model.fit(X_tr, y_train_loao)

        # التوقع
        preds = loao_model.predict(X_te)
        detection_rate = np.mean(preds == 1) * 100
        print(f"-> نسبة اكتشاف الهجوم الجديد [{unseen_attack}] دون تدريبه عليه: {detection_rate:.2f}%")
        print("   (هذا يقيس قدرة نظام X-IDS الحقيقية على اكتشاف Zero-Day Attacks)")

    def explain_with_shap(self, sample_size=100, save_plot="shap_summary.png"):
        """
        تفسير قرارات الموديل باستخدام SHAP (Explainable AI - XAI):
        تحديد أهم الخصائص التي أدت لكشف الهجمات وتفسير قرار عينة معينة.
        """
        print("\n" + "="*50)
        print("[7] Explainable AI (SHAP Analysis)...")
        print("="*50)
        
        # نأخذ عينة صغيرة لحساب الـ SHAP بسرعة
        X_sample = self.X_test[:sample_size]
        
        print("-> جاري حساب قيم SHAP باستخدام TreeExplainer...")
        explainer = shap.TreeExplainer(self.xgb_model)
        shap_values = explainer.shap_values(X_sample)

        # حساب متوسط التأثير المطلق للخصائص (Mean |SHAP Value|)
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': mean_abs_shap
        }).sort_values(by='Importance', ascending=False)

        print("\n-> أهم 10 خصائص أثرت في قرارات كشف الهجمات (Top 10 Influential Features):")
        for rank, row in enumerate(importance_df.head(10).itertuples(), 1):
            print(f"  {rank:2d}. {row.Feature:<28} | SHAP Importance: {row.Importance:.4f}")

        # رسم المخطط البياني وحفظه
        try:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Importance', y='Feature', data=importance_df.head(12), palette='viridis')
            plt.title("X-IDS: Top Features Influencing Intrusion Detection Decisions (SHAP)", fontsize=12, fontweight='bold')
            plt.xlabel("Mean |SHAP Value| (Impact on Model Decision)")
            plt.tight_layout()
            plt.savefig(save_plot, dpi=300)
            plt.close()
            print(f"\n-> تم حفظ رسم تفسير القرارات (SHAP Plot) بنجاح في: {save_plot}")
        except Exception as e:
            print(f"-> تعذر رسم المخطط: {e}")

        return importance_df

def run_full_pipeline():
    pipeline = XIDSPipeline(data_path="data/cic_ids2017_sample.csv")
    pipeline.load_data()
    pipeline.inspect_data()
    pipeline.clean_data(handle_attempted='benign')
    pipeline.prepare_features_and_target(binary=True)
    pipeline.train_models()
    pipeline.evaluate_model(pipeline.rf_model, model_name="Random Forest")
    pipeline.evaluate_model(pipeline.xgb_model, model_name="XGBoost")
    pipeline.leave_one_attack_out_test(unseen_attack='PortScan')
    pipeline.explain_with_shap(sample_size=150, save_plot="shap_feature_importance.png")

if __name__ == '__main__':
    run_full_pipeline()
