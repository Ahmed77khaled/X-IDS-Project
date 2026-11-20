"""
generate_sample_dataset.py
--------------------------
ينشئ عينة واقعية ومصغرة تحاكي تماماً بنية داتا سيت CIC-IDS2017 Improved
حتى تتمكن من تشغيل الكود والموديل فوراً مثل كولاب والتأكد من نجاح كل المراحل
قبل وضع الملفات الضخمة الأصلية.
"""

import os
import numpy as np
import pandas as pd

def create_sample_dataset(output_path="data/cic_ids2017_sample.csv", n_samples=5000):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.random.seed(42)

    # 1. تعريف الفئات كما هي في CIC-IDS2017 Improved مع فئات الـ Attempted
    # 70% Benign, 15% DoS, 5% DoS-Attempted, 7% PortScan, 3% PortScan-Attempted
    labels = np.random.choice(
        ['BENIGN', 'DoS Hulk', 'DoS Hulk - Attempted', 'PortScan', 'PortScan - Attempted'],
        size=n_samples,
        p=[0.70, 0.15, 0.05, 0.07, 0.03]
    )

    # 2. خصائص الشبكة (Network Flow Identifiers - التي يجب حذفها لمنع الـ Data Leakage)
    src_ips = [f"192.168.10.{np.random.randint(2, 50)}" for _ in range(n_samples)]
    dst_ips = [f"172.16.0.{np.random.randint(1, 10)}" for _ in range(n_samples)]
    src_ports = np.random.randint(1024, 65535, size=n_samples)
    dst_ports = np.random.choice([80, 443, 22, 21, 8080, 53], size=n_samples)
    protocols = np.random.choice([6, 17], size=n_samples) # TCP, UDP
    timestamps = [f"05/07/2017 {np.random.randint(9, 17):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}" for _ in range(n_samples)]
    flow_ids = [f"{src_ips[i]}-{dst_ips[i]}-{src_ports[i]}-{dst_ports[i]}-{protocols[i]}" for i in range(n_samples)]

    # 3. خصائص الـ Flow الرياضية والإحصائية (Network Traffic Features)
    flow_duration = np.random.exponential(scale=100000, size=n_samples)
    tot_fwd_pkts = np.random.poisson(lam=10, size=n_samples) + 1
    tot_bwd_pkts = np.random.poisson(lam=8, size=n_samples)
    tot_len_fwd = tot_fwd_pkts * np.random.uniform(50, 1400, size=n_samples)
    tot_len_bwd = tot_bwd_pkts * np.random.uniform(50, 1400, size=n_samples)

    # Flow Bytes/s & Flow Packets/s (نضع فيها بعض الـ Infs والـ NaNs عمداً لتجربة التنظيف)
    flow_bytes_s = (tot_len_fwd + tot_len_bwd) / (flow_duration / 1000000 + 1e-6)
    flow_pkts_s = (tot_fwd_pkts + tot_bwd_pkts) / (flow_duration / 1000000 + 1e-6)

    # تعديل سلوك الهجمات لتكون مميزة إحصائياً (Ground Truth)
    for i in range(n_samples):
        if 'DoS' in labels[i]:
            flow_duration[i] = np.random.uniform(1000, 50000)
            tot_fwd_pkts[i] += np.random.randint(50, 200)
            flow_bytes_s[i] *= 10
            flow_pkts_s[i] *= 15
        elif 'PortScan' in labels[i]:
            flow_duration[i] = np.random.uniform(5, 500)
            tot_fwd_pkts[i] = 1
            tot_bwd_pkts[i] = 0

    # 4. تجميع الداتا فريم مع خصائص CICFlowMeter المعروفة
    df = pd.DataFrame({
        'Flow ID': flow_ids,
        'Source IP': src_ips,
        'Source Port': src_ports,
        'Destination IP': dst_ips,
        'Destination Port': dst_ports,
        'Protocol': protocols,
        'Timestamp': timestamps,
        'Flow Duration': flow_duration,
        'Total Fwd Packets': tot_fwd_pkts,
        'Total Backward Packets': tot_bwd_pkts,
        'Total Length of Fwd Packets': tot_len_fwd,
        'Total Length of Bwd Packets': tot_len_bwd,
        'Fwd Packet Length Max': tot_len_fwd / tot_fwd_pkts * 1.5,
        'Fwd Packet Length Min': tot_len_fwd / tot_fwd_pkts * 0.5,
        'Fwd Packet Length Mean': tot_len_fwd / tot_fwd_pkts,
        'Fwd Packet Length Std': np.random.uniform(0, 50, size=n_samples),
        'Bwd Packet Length Max': tot_len_bwd / (tot_bwd_pkts + 1) * 1.5,
        'Bwd Packet Length Min': tot_len_bwd / (tot_bwd_pkts + 1) * 0.2,
        'Bwd Packet Length Mean': tot_len_bwd / (tot_bwd_pkts + 1),
        'Flow Bytes/s': flow_bytes_s,
        'Flow Packets/s': flow_pkts_s,
        'Flow IAT Mean': np.random.exponential(scale=5000, size=n_samples),
        'Flow IAT Std': np.random.exponential(scale=2000, size=n_samples),
        'Flow IAT Max': np.random.exponential(scale=20000, size=n_samples),
        'Flow IAT Min': np.random.exponential(scale=100, size=n_samples),
        'Fwd IAT Total': np.random.exponential(scale=80000, size=n_samples),
        'Bwd IAT Total': np.random.exponential(scale=70000, size=n_samples),
        'Fwd PSH Flags': np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1]),
        'Bwd PSH Flags': np.zeros(n_samples), # عمود ثابت (constant feature) لاختبار الحذف
        'FIN Flag Count': np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15]),
        'SYN Flag Count': np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1]),
        'RST Flag Count': np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05]),
        'ACK Flag Count': np.random.choice([0, 1], size=n_samples, p=[0.4, 0.6]),
        'Down/Up Ratio': np.random.uniform(0, 5, size=n_samples),
        'Average Packet Size': (tot_len_fwd + tot_len_bwd) / (tot_fwd_pkts + tot_bwd_pkts + 1),
        'Subflow Fwd Packets': tot_fwd_pkts,
        'Subflow Fwd Bytes': tot_len_fwd,
        'Init_Win_bytes_forward': np.random.choice([8192, 29200, 65535, -1], size=n_samples),
        'Init_Win_bytes_backward': np.random.choice([8192, 29200, 65535, -1], size=n_samples),
        'Label': labels
    })

    # 5. حقن بعض القيم الفاسدة (Infs, NaNs, صفوف مكررة) لمحاكاة الداتا الحقيقية
    # قيم Infinity
    inf_indices = np.random.choice(n_samples, size=15, replace=False)
    df.loc[inf_indices[:10], 'Flow Bytes/s'] = np.inf
    df.loc[inf_indices[10:], 'Flow Packets/s'] = -np.inf

    # قيم Null / NaN
    nan_indices = np.random.choice(n_samples, size=20, replace=False)
    df.loc[nan_indices[:10], 'Flow Bytes/s'] = np.nan
    df.loc[nan_indices[10:], 'Flow IAT Mean'] = np.nan

    # صفوف مكررة
    df = pd.concat([df, df.iloc[:30]], ignore_index=True)

    df.to_csv(output_path, index=False)
    print(f"[OK] Sample dataset generated successfully at: {output_path}")
    print(f"     Total rows: {len(df)}, Columns: {df.shape[1]}")
    print(f"     Labels distribution:\n{df['Label'].value_counts()}")
    return output_path

if __name__ == '__main__':
    create_sample_dataset()
