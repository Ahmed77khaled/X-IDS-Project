"""
generate_report_evidence.py
ينفذ التاسكات الستة المطلوبة من الدكتورة على داتا سيت wednesday.csv
ويحفظ مخرجات وصور عالية الجودة لاستخدامها في التقرير والبريزنتيشن.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("Reports/screenshots", exist_ok=True)

# مسار ملف البيانات
data_path = "Dataset/CICIDS2017_improved/wednesday.csv"
print(f"Loading sample from: {data_path}...")

# قراءة عينة كافية للعمل السريع والدقيق
df = pd.read_csv(data_path, nrows=10000, low_memory=False)
df.columns = df.columns.str.strip()

print(f"Dataset shape: {df.shape}")

# 1. أول 5 سطور (Head)
head_df = df[['Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Bytes/s', 'Flow Packets/s', 'Label']].head(5)
print("\n--- First 5 Rows (Head) ---")
print(head_df)

# 2. آخر 5 سطور (Tail)
tail_df = df[['Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Bytes/s', 'Flow Packets/s', 'Label']].tail(5)
print("\n--- Last 5 Rows (Tail) ---")
print(tail_df)

# 3. فحص الـ Features والـ Targets
target_counts = df['Label'].value_counts()
print("\n--- Target Distribution ---")
print(target_counts)

# 4. محاكاة وجود قيم Null و Infs وتطبيق Dropna و Fillna لإظهار الفرق
num_cols = df.select_dtypes(include=[np.number]).columns
df_with_nulls = df.copy()

# تحويل Infs إلى NaNs (مشكلة شهيرة في Flow Bytes/s)
df_with_nulls[num_cols] = df_with_nulls[num_cols].replace([np.inf, -np.inf], np.nan)

# حقن بعض القيم المفقودة في عينة للتوضيح
nan_idx = [3, 7, 12, 25, 40]
df_with_nulls.loc[nan_idx, 'Flow Bytes/s'] = np.nan

null_count_before = df_with_nulls['Flow Bytes/s'].isnull().sum()
print(f"\nNulls before handling: {null_count_before}")

# أسلوب Dropna
df_dropped = df_with_nulls.dropna()
rows_after_drop = len(df_dropped)
print(f"Rows after dropna: {rows_after_drop} (Dropped: {len(df_with_nulls) - rows_after_drop})")

# أسلوب Fillna بالوسيط (Median)
median_val = df_with_nulls['Flow Bytes/s'].median()
df_filled = df_with_nulls.copy()
df_filled['Flow Bytes/s'] = df_filled['Flow Bytes/s'].fillna(median_val)
null_count_after_fill = df_filled['Flow Bytes/s'].isnull().sum()
print(f"Nulls after fillna (median={median_val:.2f}): {null_count_after_fill}")

# إنشاء رسم بياني لتوزيع الفئات وحفظه
plt.figure(figsize=(9, 4.5))
plt.style.use('default')
target_counts.plot(kind='barh', color='#1f77b4', edgecolor='black')
plt.title("Distribution of Network Traffic Classes (Wednesday Sample)", fontsize=12, fontweight='bold')
plt.xlabel("Number of Flows")
plt.tight_layout()
plt.savefig("Reports/screenshots/target_distribution.png", dpi=200)
plt.close()

# إنشاء صورة توضح جدول أول 5 سطور Head
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.axis('off')
table = ax.table(cellText=head_df.values, colLabels=head_df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.1, 1.6)
plt.title("Sample of First 5 Rows (df.head())", fontsize=11, fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig("Reports/screenshots/head_table.png", dpi=200)
plt.close()

# إنشاء صورة توضح جدول آخر 5 سطور Tail
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.axis('off')
table = ax.table(cellText=tail_df.values, colLabels=tail_df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.1, 1.6)
plt.title("Sample of Last 5 Rows (df.tail())", fontsize=11, fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig("Reports/screenshots/tail_table.png", dpi=200)
plt.close()

# رسم توضيحي لمقارنة Dropna مقابل Fillna
fig, ax = plt.subplots(figsize=(7, 3.5))
bars = ax.bar(['Original Rows', 'After dropna()', 'After fillna()'], 
              [len(df_with_nulls), rows_after_drop, len(df_filled)], 
              color=['#2ca02c', '#d62728', '#1f77b4'])
ax.set_ylim(min(rows_after_drop - 50, len(df_with_nulls) - 50), len(df_with_nulls) + 50)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f"{int(yval):,}", ha='center', va='bottom', fontweight='bold')
plt.title("Comparison: dropna() vs fillna() on Flow Records", fontsize=11, fontweight='bold')
plt.ylabel("Row Count")
plt.tight_layout()
plt.savefig("Reports/screenshots/dropna_vs_fillna.png", dpi=200)
plt.close()

print("\n[OK] All screenshot artifacts generated in Reports/screenshots/!")
