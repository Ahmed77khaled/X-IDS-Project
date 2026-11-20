# -*- coding: utf-8 -*-
"""
X-IDS Intelligent Dataset Resolver & Auto-Downloader
Handles all 4 real-world student scenarios:
 1. Dataset already in place (Dataset/CICIDS2017_improved/wednesday.csv).
 2. Dataset extracted directly in Dataset/ or another local folder -> Auto-relocated.
 3. Dataset downloaded as zip in Downloads/Desktop -> Auto-detected & unzipped.
 4. Dataset completely missing -> Downloads from official research source with progress bar.
"""

import os
import sys
import time
import shutil
import zipfile
import urllib.request
from pathlib import Path

DATASET_DIR = Path("Dataset")
TARGET_SUBDIR = DATASET_DIR / "CICIDS2017_improved"
TARGET_FILE = TARGET_SUBDIR / "wednesday.csv"
DATASET_URL = "https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip"

def print_banner(msg):
    print("\n" + "=" * 78)
    print(f"  {msg}")
    print("=" * 78)

def progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100.0, (downloaded / total_size) * 100.0)
        mb_down = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        bar_len = 30
        filled = int(bar_len * downloaded / total_size)
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(f"\r  [{bar}] {percent:5.1f}% ({mb_down:5.1f}/{mb_total:5.1f} MB)")
        sys.stdout.flush()

def search_local_files():
    """Search common user folders (Downloads, Desktop, Documents, Project) for dataset files."""
    home = Path.home()
    search_roots = [
        Path(".").resolve(),
        Path("..").resolve(),
        home / "Downloads",
        home / "Desktop",
        home / "Documents"
    ]
    
    found_csv = None
    found_zip = None

    for root in search_roots:
        if not root.exists():
            continue
        try:
            # Check 1 level deep for speed
            for item in root.glob("*"):
                name_lower = item.name.lower()
                if item.is_file():
                    if name_lower in ["wednesday.csv", "wednesday-workinghours.pcap_iscx.csv"]:
                        found_csv = item
                        return found_csv, found_zip
                    if name_lower in ["cicids2017_improved.zip", "dataset.zip", "cicids2017.zip"]:
                        if not found_zip:
                            found_zip = item
                elif item.is_dir():
                    # Check inside folders like Downloads/CICIDS2017_improved
                    try:
                        for sub_item in item.glob("*.csv"):
                            if sub_item.name.lower() in ["wednesday.csv", "wednesday-workinghours.pcap_iscx.csv"]:
                                found_csv = sub_item
                                return found_csv, found_zip
                        for sub_item in item.glob("*.zip"):
                            if sub_item.name.lower() in ["cicids2017_improved.zip"]:
                                if not found_zip:
                                    found_zip = sub_item
                    except PermissionError:
                        pass
        except PermissionError:
            pass

    return found_csv, found_zip

def resolve_dataset():
    TARGET_SUBDIR.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # Scenario 1: Already verified in place
    # -------------------------------------------------------------------------
    if TARGET_FILE.exists() and TARGET_FILE.stat().st_size > 10 * 1024 * 1024:
        size_mb = TARGET_FILE.stat().st_size / (1024 * 1024)
        print(f"[OK] Dataset is already verified in place ({size_mb:.1f} MB): {TARGET_FILE}")
        return True

    # -------------------------------------------------------------------------
    # Scenario 2: wednesday.csv in Dataset/ root (extracted without subfolder)
    # -------------------------------------------------------------------------
    alt_file = DATASET_DIR / "wednesday.csv"
    if alt_file.exists() and alt_file.stat().st_size > 10 * 1024 * 1024:
        print(f"[*] Found 'wednesday.csv' in Dataset root. Relocating to {TARGET_SUBDIR}...")
        shutil.copy2(alt_file, TARGET_FILE)
        print(f"[OK] Dataset placed in {TARGET_FILE}")
        return True

    # Check for zip in Dataset/ root
    local_zip = DATASET_DIR / "CICIDS2017_improved.zip"
    if local_zip.exists() and local_zip.stat().st_size > 50 * 1024 * 1024:
        print(f"[*] Found local zip: {local_zip}. Extracting into {TARGET_SUBDIR}...")
        with zipfile.ZipFile(local_zip, 'r') as z:
            z.extractall(TARGET_SUBDIR)
        print(f"[OK] Extracted successfully to {TARGET_SUBDIR}")
        return True

    # -------------------------------------------------------------------------
    # Scenario 3: Search common user folders (Downloads, Desktop, etc.)
    # -------------------------------------------------------------------------
    print("[*] Searching common local folders (Downloads, Desktop, Project) for existing dataset...")
    found_csv, found_zip = search_local_files()

    if found_csv:
        print(f"[+] Found existing CSV file at: {found_csv}")
        print(f"[*] Copying into project folder: {TARGET_FILE}...")
        shutil.copy2(found_csv, TARGET_FILE)
        print("[OK] Dataset copied successfully!")
        return True

    if found_zip:
        print(f"[+] Found downloaded dataset archive at: {found_zip}")
        print(f"[*] Extracting into {TARGET_SUBDIR}...")
        with zipfile.ZipFile(found_zip, 'r') as z:
            z.extractall(TARGET_SUBDIR)
        print("[OK] Dataset extracted successfully!")
        return True

    # -------------------------------------------------------------------------
    # Scenario 4: Missing entirely -> Prompt to auto-download with progress bar
    # -------------------------------------------------------------------------
    print_banner("DATASET AUTOMATIC DOWNLOADER")
    print("The benchmark dataset (wednesday.csv) was not found on your system.")
    print("Official Research Source:")
    print(f"  {DATASET_URL}\n")

    user_choice = input("Do you want to download it automatically now (~320 MB)? (Y/n): ").strip().lower()
    if user_choice not in ["", "y", "yes"]:
        print("\n[!] Download skipped. If you have the file elsewhere, you can place it in:")
        print(f"    {TARGET_FILE.resolve()}")
        return False

    temp_zip = DATASET_DIR / "temp_download.zip"
    print("\n[*] Downloading dataset from official research server...")
    try:
        urllib.request.urlretrieve(DATASET_URL, temp_zip, reporthook=progress_hook)
        print("\n[OK] Download completed successfully!")
        
        print(f"[*] Extracting files into {TARGET_SUBDIR}...")
        with zipfile.ZipFile(temp_zip, 'r') as z:
            z.extractall(TARGET_SUBDIR)
            
        if temp_zip.exists():
            temp_zip.unlink()
            
        print("[OK] Dataset extraction completed successfully!")
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to download automatically: {e}")
        print(f"Please download the zip manually from: {DATASET_URL}")
        print(f"and extract it into: {TARGET_SUBDIR.resolve()}")
        return False

if __name__ == "__main__":
    resolve_dataset()
