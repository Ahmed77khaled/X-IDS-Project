#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
توليد ملفات mp3 التعليمية لمشروع كشف التسلل X-IDS باستخدام Microsoft Neural TTS.
يقرأ النصوص من audio/scripts/*.txt ويطبق قاموس النطق التقني الصوتي من audio/pronunciation.json.

طريقة الاستخدام:
    pip install -r requirements-audio.txt
    python audio/generate_audio.py                  # توليد الملفات الناقصة فقط
    python audio/generate_audio.py --force          # إعادة توليد كافة الخطوات
    python audio/generate_audio.py --voice ar-EG-ShakirNeural   # استخدام صوت شاكر
    python audio/generate_audio.py --rate=-5%       # التحكم في سرعة الإلقاء
    python audio/generate_audio.py --step 1         # توليد خطوة محددة
"""
import argparse
import asyncio
import json
import os
import re
import shutil
import sys
from pathlib import Path

# معالجة حلقة الأحداث لنظام ويندوز مع بايثون لتفادي أخطاء ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import edge_tts

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
OUT_DIR = ROOT
PRON_FILE = ROOT / "pronunciation.json"


def load_pronunciation() -> dict:
    """تحميل قاموس النطق الصوتي وتجهيزه."""
    if PRON_FILE.exists():
        try:
            return json.loads(PRON_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ خطأ أثناء قراءة {PRON_FILE.name}: {e}")
    return {}


def prepare_text(text: str, pron: dict) -> str:
    """
    تجهيز النص للتوليد الصوتي:
    1. استبدال المصطلحات الإنجليزية بالتعريب الصوتي المتقن لمنع التقطيع (Robotic Stuttering).
    2. الأطول أولاً لضمان عدم تداخل الكلمات المركبة.
    3. إزالة رموز الماركداون والأسطر الزائدة.
    """
    for en in sorted(pron, key=len, reverse=True):
        pattern = re.escape(en)
        text = re.sub(pattern, pron[en], text, flags=re.IGNORECASE)

    # إزالة علامات الماركداون والرموز التنسيقية
    text = re.sub(r"[#*`>_~\[\]\(\)\$]", "", text)
    # توحيد المسافات والأسطر الفارغة
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text


async def generate_file(
    txt_file: Path,
    voice: str,
    rate: str,
    pitch: str,
    force: bool,
    pron: dict
) -> Path:
    """توليد ملف صوت mp3 من ملف نصي محدد."""
    base_name = txt_file.stem
    mp3_file = OUT_DIR / f"{base_name}.mp3"

    # التحقق من وجود الملف
    if mp3_file.exists() and not force:
        print(f"⏩ تخطي: {mp3_file.name} (موجود مسبقاً)")
    else:
        raw_text = txt_file.read_text(encoding="utf-8")
        clean_text = prepare_text(raw_text, pron)
        
        print(f"🎙️ جاري توليد: {mp3_file.name} باستخدام {voice}...")
        communicator = edge_tts.Communicate(
            clean_text,
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        await communicator.save(str(mp3_file))
        size_kb = mp3_file.stat().st_size // 1024
        print(f"✅ تم بنجاح: {mp3_file.name} ({size_kb} KB)")

    # توليد نسخة متوافقة بالاسم القصير stepX.mp3 إذا كان الاسم مطابقاً
    step_match = re.match(r"^(step\d+)", base_name, re.IGNORECASE)
    if step_match:
        short_name = f"{step_match.group(1).lower()}.mp3"
        short_mp3 = OUT_DIR / short_name
        if short_mp3 != mp3_file:
            try:
                shutil.copy2(mp3_file, short_mp3)
                print(f"   ↳ نسخة متوافقة: {short_name}")
            except Exception as e:
                print(f"   ⚠️ تعذر نسخ {short_name}: {e}")

    return mp3_file


async def main():
    parser = argparse.ArgumentParser(description="مولد الشرح الصوتي لمشروع X-IDS")
    parser.add_argument(
        "--voice",
        default="ar-EG-SalmaNeural",
        help="اسم الصوت العصبي (الافتراضي: ar-EG-SalmaNeural صوت مصري دافئ، متاح أيضاً: ar-EG-ShakirNeural)"
    )
    parser.add_argument(
        "--rate",
        default="-5%",
        help="سرعة التحدث، مثال: -5%% أو -10%% لشرح هادئ ومريح"
    )
    parser.add_argument(
        "--pitch",
        default="+0Hz",
        help="نبرة الصوت (الافتراضي: +0Hz)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="إعادة توليد الملفات حتى لو كانت موجودة مسبقاً"
    )
    parser.add_argument(
        "--step",
        default=None,
        help="توليد خطوة محددة فقط (مثال: 1 أو step1 أو step1_import_libraries)"
    )
    args = parser.parse_args()

    pron = load_pronunciation()
    print(f"📚 تم تحميل قاموس النطق الصوتي: {len(pron)} مصطلح تقني.")

    if not SCRIPTS_DIR.exists():
        raise SystemExit(f"❌ مجلد النصوص غير موجود: {SCRIPTS_DIR}")

    files = sorted(SCRIPTS_DIR.glob("*.txt"))
    if not files:
        raise SystemExit(f"❌ لم يتم العثور على ملفات نصوص في: {SCRIPTS_DIR}")

    # التصفية بحسب الخطوة إذا طُلبت
    if args.step:
        target = str(args.step).strip().lower()
        if target.isdigit():
            target = f"step{target}"
        files = [f for f in files if target in f.stem.lower()]
        if not files:
            raise SystemExit(f"❌ لم يتم العثور على أي ملف يطابق الخطوة: {args.step}")

    print(f"🚀 بدء توليد {len(files)} ملف صوتي...")
    for f in files:
        await generate_file(
            txt_file=f,
            voice=args.voice,
            rate=args.rate,
            pitch=args.pitch,
            force=args.force,
            pron=pron
        )

    print("\n🎉 اكتملت العملية بنجاح! جميع الملفات الصوتية متوفرة في مجلد audio/.")


if __name__ == "__main__":
    asyncio.run(main())
