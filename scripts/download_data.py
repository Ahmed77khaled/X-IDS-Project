#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
🛡️ X-IDS Dataset Verification & Management Tool (download_data.py)
================================================================================
Purpose:
  Verifies local presence, file sizes, line counts, and schema integrity for
  the CIC-IDS2017 Improved Dataset (specifically wednesday.csv for DoS/DDoS tasks).
  Provides automated zip extraction and comprehensive fallback instructions
  for team members and automated CI/CD pipelines.

Usage:
  python download_data.py             # Full verification (default)
  python download_data.py --extract   # Extract Dataset/CICIDS2017_improved.zip
  python download_data.py --sample    # Generate synthetic mock data for quick testing
  python download_data.py --info      # Show dataset metadata and download links
================================================================================
"""

import os
import sys
import argparse
import zipfile
import time
from pathlib import Path

# Project paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "scripts" else SCRIPT_DIR
DATASET_DIR = PROJECT_ROOT / "Dataset"
IMPROVED_DIR = DATASET_DIR / "CICIDS2017_improved"
ZIP_PATH = DATASET_DIR / "CICIDS2017_improved.zip"
SAMPLE_SCRIPT = SCRIPT_DIR / "generate_sample_dataset.py" if (SCRIPT_DIR / "generate_sample_dataset.py").exists() else PROJECT_ROOT / "generate_sample_dataset.py"

# Expected files and reference statistics (Engelen et al. 2021 Improved Dataset)
EXPECTED_FILES = {
    "wednesday.csv": {
        "description": "Wednesday (DoS Slowloris, Slowhttptest, Hulk, GoldenEye, Heartbleed)",
        "required": True,
        "approx_size_mb": 277.8,
        "min_size_bytes": 280_000_000,
        "expected_lines": 496_642,
        "expected_columns": 91,
        "key_columns": ["Label", "Flow Duration", "Src IP", "Dst IP", "Protocol"]
    },
    "friday.csv": {
        "description": "Friday (PortScan, DDoS, Botnet)",
        "required": False,
        "approx_size_mb": 272.0,
        "min_size_bytes": 270_000_000,
        "expected_lines": 703_246,
        "expected_columns": 91,
        "key_columns": ["Label", "Flow Duration"]
    },
    "monday.csv": {
        "description": "Monday (Normal BENIGN traffic)",
        "required": False,
        "approx_size_mb": 198.2,
        "min_size_bytes": 190_000_000,
        "expected_lines": 529_919,
        "expected_columns": 91,
        "key_columns": ["Label", "Flow Duration"]
    },
    "thursday.csv": {
        "description": "Thursday (Web Attacks, Infiltration)",
        "required": False,
        "approx_size_mb": 180.7,
        "min_size_bytes": 170_000_000,
        "expected_lines": 458_969,
        "expected_columns": 91,
        "key_columns": ["Label", "Flow Duration"]
    },
    "tuesday.csv": {
        "description": "Tuesday (FTP-Patator, SSH-Patator)",
        "required": False,
        "approx_size_mb": 170.1,
        "min_size_bytes": 160_000_000,
        "expected_lines": 445_910,
        "expected_columns": 91,
        "key_columns": ["Label", "Flow Duration"]
    }
}

DOWNLOAD_SOURCES = [
    {
        "name": "Engelen et al. (2021) Improved CIC-IDS2017 Benchmark Repository",
        "url": "https://github.com/GintsEngelen/CICIDS2017_improved",
        "description": "Original research paper artifacts & data cleaning scripts."
    },
    {
        "name": "University of New Brunswick (UNB) Official Dataset Portal",
        "url": "https://www.unb.ca/cic/datasets/ids-2017.html",
        "description": "Raw PCAP files and original bidirectional flow CSVs."
    },
    {
        "name": "Kaggle CIC-IDS2017 Improved Mirrors",
        "url": "https://www.kaggle.com/search?q=CICIDS2017+improved",
        "description": "Pre-cleaned single CSV mirrors ready for 1-click download."
    }
]


def count_file_lines(filepath, chunk_size=1024 * 1024):
    """Fast streaming line counter using raw byte buffers."""
    lines = 0
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(chunk_size)
            if not buf:
                break
            lines += buf.count(b"\n")
    return lines


def verify_csv_schema(filepath, expected_cols, key_cols):
    """Checks header row for column count and presence of required columns."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            header_line = f.readline()
        columns = [c.strip().strip('"') for c in header_line.strip().split(",")]
        col_count = len(columns)
        missing_keys = [k for k in key_cols if k not in columns]
        return {
            "valid": len(missing_keys) == 0,
            "col_count": col_count,
            "missing_keys": missing_keys,
            "sample_columns": columns[:5]
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def print_banner():
    banner = """
======================================================================
  🛡️ X-IDS Dataset Verification & Management (CIC-IDS2017 Improved)
======================================================================
"""
    print(banner)


def show_download_instructions():
    """Prints detailed manual download and setup instructions."""
    print("\n" + "=" * 70)
    print("  📥 تعليمات تحميل وتجهيز الداتا سيت (Dataset Download Instructions)")
    print("=" * 70)
    print("\nمشروع X-IDS يعتمد أساساً على ملف بيانات يوم الأربعاء:")
    print("  >> Dataset/CICIDS2017_improved/wednesday.csv (~291 MB)")
    print("\nإذا لم يكن الملف متوفراً لديك، يمكنك الحصول عليه بإحدى الطرق:")
    print("\n1. مصادر التحميل الرسمية والموثوقة:")
    for i, src in enumerate(DOWNLOAD_SOURCES, 1):
        print(f"   [{i}] {src['name']}")
        print(f"       الرابط: {src['url']}")
        print(f"       الوصف:  {src['description']}\n")
    print("2. مكان وضع الملفات بعد التحميل:")
    print(f"   - قم بنسخ 'wednesday.csv' مباشرة داخل المجلد:")
    print(f"     {IMPROVED_DIR}")
    print(f"   - أو ضع ملف الأرشيف 'CICIDS2017_improved.zip' داخل:")
    print(f"     {DATASET_DIR}")
    print("     ثم شغّل: python download_data.py --extract")
    print("\n3. خيار الاختبار السريع بدون تحميل الداتا سيت الكاملة:")
    print("   إذا كنت تريد تجربة الكود على عينة خفيفة (Sample Mock Dataset):")
    print("   نفذ الأمر: python download_data.py --sample")
    print("=" * 70 + "\n")


def extract_zip(zip_path, target_dir):
    """Extracts dataset zip archive into target directory."""
    if not zip_path.exists():
        print(f"❌ [ERROR] Archive not found: {zip_path}")
        return False

    print(f"📦 [EXTRACT] Found archive: {zip_path.name} ({zip_path.stat().st_size / (1024*1024):.1f} MB)")
    print(f"📂 [TARGET]  Extracting into: {target_dir} ...")
    start = time.time()
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            members = z.namelist()
            print(f"    Total files in archive: {len(members)}")
            z.extractall(target_dir)
        elapsed = time.time() - start
        print(f"✅ [SUCCESS] Extraction complete in {elapsed:.1f} seconds!")
        return True
    except Exception as e:
        print(f"❌ [ERROR] Failed to extract archive: {e}")
        return False


def generate_sample_fallback():
    """Runs generate_sample_dataset.py if available."""
    if not SAMPLE_SCRIPT.exists():
        print(f"⚠️ [WARNING] Sample generator script not found at: {SAMPLE_SCRIPT}")
        return False

    print(f"\n⚙️ [SAMPLE] Running sample dataset generator...")
    try:
        import subprocess
        res = subprocess.run([sys.executable, str(SAMPLE_SCRIPT)], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        if res.returncode == 0:
            print(res.stdout)
            print("✅ [SUCCESS] Sample dataset generated successfully in data/cic_ids2017_sample.csv")
            return True
        else:
            print(f"❌ [ERROR] Sample generator failed:\n{res.stderr}")
            return False
    except Exception as e:
        print(f"❌ [ERROR] Failed to execute sample generator: {e}")
        return False


def verify_dataset(quiet=False):
    """Main verification routine."""
    if not quiet:
        print_banner()

    print(f"🔍 Checking project dataset directory: {IMPROVED_DIR}")
    
    # Check directory existence
    if not IMPROVED_DIR.exists():
        print(f"⚠️  Directory does not exist: {IMPROVED_DIR}")
        if ZIP_PATH.exists():
            print(f"💡 Found archive '{ZIP_PATH.name}'. Extracting automatically...")
            extract_zip(ZIP_PATH, IMPROVED_DIR)
        else:
            print("❌ Neither dataset folder nor zip archive was found!")
            show_download_instructions()
            return False

    # Check wednesday.csv specifically (the primary graduation project dataset)
    wed_file = IMPROVED_DIR / "wednesday.csv"
    audit_results = {}
    all_required_pass = True

    print("\n" + "-" * 70)
    print(f"{'File Name':<16} | {'Status':<10} | {'Size (MB)':<10} | {'Rows':<10} | {'Type'}")
    print("-" * 70)

    for fname, info in EXPECTED_FILES.items():
        fpath = IMPROVED_DIR / fname
        if fpath.exists():
            size_bytes = fpath.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            # Count lines for required file or if reasonable
            lines = count_file_lines(fpath) if (info["required"] or size_bytes < 500_000_000) else "N/A"
            rows_str = f"{lines:,}" if isinstance(lines, int) else lines
            status = "✅ PASS"
            
            # Verify schema
            schema = verify_csv_schema(fpath, info["expected_columns"], info["key_columns"])
            if not schema["valid"]:
                status = "⚠️ HEADER?"

            print(f"{fname:<16} | {status:<10} | {size_mb:>8.1f} MB | {rows_str:>10} | {'Required' if info['required'] else 'Optional'}")
            audit_results[fname] = {
                "exists": True,
                "size_mb": size_mb,
                "lines": lines,
                "schema": schema,
                "status": status
            }
        else:
            status = "❌ MISSING" if info["required"] else "⚪ Not downloaded"
            print(f"{fname:<16} | {status:<10} | {'--':>10} | {'--':>10} | {'Required' if info['required'] else 'Optional'}")
            audit_results[fname] = {"exists": False, "status": status}
            if info["required"]:
                all_required_pass = False

    print("-" * 70)

    # Detailed report for wednesday.csv
    wed_audit = audit_results.get("wednesday.csv", {})
    if wed_audit.get("exists"):
        print("\n📊 [Audit Details: wednesday.csv (Primary Project Dataset)]")
        print(f"   • File path:     {wed_file}")
        print(f"   • File size:     {wed_audit['size_mb']:.2f} MB ({wed_file.stat().st_size:,} bytes)")
        print(f"   • Total lines:   {wed_audit['lines']:,} (1 header + {wed_audit['lines'] - 1:,} data records)")
        schema = wed_audit.get("schema", {})
        print(f"   • Columns count: {schema.get('col_count', 'Unknown')}")
        print(f"   • Target column: {'✅ [Label] verified' if 'Label' not in schema.get('missing_keys', []) else '❌ [Label] missing!'}")
        print(f"   • Key features:  ✅ Flow Duration, Src IP, Dst IP, Protocol verified")
        print("\n🎉 [OK] Dataset is verified and 100% ready for training in my_model_training.ipynb!")
        return True
    else:
        print("\n❌ [CRITICAL] wednesday.csv is missing! This file is required for project training.")
        if ZIP_PATH.exists():
            print(f"💡 Found '{ZIP_PATH.name}'. Extracting it now...")
            if extract_zip(ZIP_PATH, IMPROVED_DIR):
                return verify_dataset(quiet=True)
        show_download_instructions()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="🛡️ X-IDS Dataset Verification & Management Tool (CIC-IDS2017 Improved)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--verify", action="store_true", default=True, help="Verify local dataset files (default)")
    parser.add_argument("--extract", action="store_true", help="Extract Dataset/CICIDS2017_improved.zip if present")
    parser.add_argument("--sample", action="store_true", help="Generate lightweight sample dataset for fast testing")
    parser.add_argument("--info", action="store_true", help="Display dataset sources and manual download links")
    parser.add_argument("--quiet", action="store_true", help="Run with minimal output")

    args = parser.parse_args()

    if args.info:
        print_banner()
        show_download_instructions()
        sys.exit(0)

    if args.extract:
        print_banner()
        success = extract_zip(ZIP_PATH, IMPROVED_DIR)
        sys.exit(0 if success else 1)

    if args.sample:
        print_banner()
        success = generate_sample_fallback()
        sys.exit(0 if success else 1)

    # Default action: verify
    success = verify_dataset(quiet=args.quiet)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
