#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
🚀 ElevenLabs Turnkey Audio Generator for X-IDS Graduation Project
========================================================================================
Convert project task explanations to ultra-realistic Egyptian AI voices using ElevenLabs.

Default Voice: "Masry" (ID: LXrTqFIgiubkrMkwvOUr) - Professional Egyptian Dialect.
Default Model: "eleven_v4" (ElevenLabs Flagship AI Model, 94 languages) or "eleven_multilingual_v2".

Usage:
    python audio/elevenlabs_generator.py --sample                  # Generate Step 1 test sample
    python audio/elevenlabs_generator.py --all                     # Synthesize all 9 steps
    python audio/elevenlabs_generator.py --step 1                  # Synthesize specific step
    python audio/elevenlabs_generator.py --model-id eleven_v4      # Use flagship v4
========================================================================================
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

# Paths setup
AUDIO_DIR = Path(__file__).resolve().parent
PROJECT_DIR = AUDIO_DIR.parent
ENV_FILE = PROJECT_DIR / ".env"
SCRIPTS_DIR = AUDIO_DIR / "scripts"
PRON_FILE = AUDIO_DIR / "pronunciation.json"
SAMPLES_DIR = AUDIO_DIR / "samples"

# Load environment variable from .env
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# The user's chosen authentic Egyptian voice "Masry"
MASRY_VOICE_ID = "LXrTqFIgiubkrMkwvOUr"
DEFAULT_VOICE_ID = MASRY_VOICE_ID
DEFAULT_MODEL_ID = "eleven_v4"  # Flagship ElevenLabs model

STEP_FILES = {
    1: "step1_import_libraries.txt",
    2: "step2_load_dataset.txt",
    3: "step3_first_5_rows.txt",
    4: "step4_last_5_rows.txt",
    5: "step5_target_distribution.txt",
    6: "step6_handle_infinities.txt",
    7: "step7_test_dropna.txt",
    8: "step8_fillna_median.txt",
    9: "step9_prevent_data_leakage.txt"
}


def get_client() -> ElevenLabs:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY is not set.")
        print(f"Please ensure your API key is configured in {ENV_FILE}")
        sys.exit(1)
    return ElevenLabs(api_key=api_key)


def load_pronunciation() -> dict:
    if PRON_FILE.exists():
        try:
            return json.loads(PRON_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def apply_pronunciation(text: str, pron: dict) -> str:
    import re
    for en in sorted(pron, key=len, reverse=True):
        text = re.sub(re.escape(en), pron[en], text, flags=re.IGNORECASE)
    # Remove markdown formatting characters
    text = re.sub(r"[#*`>_]", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text


def get_step_text(step_num: int) -> str:
    pron = load_pronunciation()
    script_file = SCRIPTS_DIR / STEP_FILES.get(step_num, f"step{step_num}.txt")
    if script_file.exists():
        raw = script_file.read_text(encoding="utf-8")
        return apply_pronunciation(raw, pron)
    default_text = (
        "أهلاً بيك في الخطوة الأولى من مشروع كشف اختراقات الشبكة بالذكاء الاصطناعي. "
        "في الخطوة دي بنجهز بيئة العمل ونستدعي المكتبات الأساسية: "
        "مكتبة بانداس للتعامل مع جداول البيانات، ونمباي للعمليات الرياضية، "
        "ومات بلوت ليب لتجهيز الرسوم البيانية. "
        "اكتب كود الاستدعاء واضغط شيفت مع إنتر لتشغيل أول خلية."
    )
    return apply_pronunciation(default_text, pron)


def synthesize_step(step_num: int, voice_id: str, model_id: str, out_path: Path, client: ElevenLabs):
    text = get_step_text(step_num)
    print(f"🎙️ Synthesizing Step {step_num} with Voice [{voice_id}] using [{model_id}]...")
    
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id
    )
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
            
    print(f"✅ Generated: {out_path.name} ({out_path.stat().st_size:,} bytes)")


def list_voices(client: ElevenLabs):
    print("\n📋 Available Voices in Your ElevenLabs Account:")
    response = client.voices.get_all()
    for v in response.voices:
        print(f"  • {v.name:<25} ID: {v.voice_id:<25} Category: {v.category}")


def main():
    parser = argparse.ArgumentParser(description="ElevenLabs Audio Generator for X-IDS")
    parser.add_argument("--step", type=int, help="Synthesize a specific step (1-9)")
    parser.add_argument("--all", action="store_true", help="Synthesize all 9 steps")
    parser.add_argument("--sample", action="store_true", help="Synthesize Step 1 as a test sample")
    parser.add_argument("--voice-id", default=DEFAULT_VOICE_ID, help="ElevenLabs Voice ID")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="ElevenLabs Model ID")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    
    args = parser.parse_args()
    client = get_client()

    if args.list_voices:
        list_voices(client)
        return

    if args.sample:
        out_sample = SAMPLES_DIR / f"sample_masry_step1_{args.model_id}.mp3"
        synthesize_step(1, args.voice_id, args.model_id, out_sample, client)
        return

    if args.step:
        out_file = AUDIO_DIR / f"step{args.step}.mp3"
        synthesize_step(args.step, args.voice_id, args.model_id, out_file, client)
        return

    if args.all:
        print(f"🚀 Starting full synthesis of all 9 steps with ElevenLabs ({args.voice_id} | {args.model_id})...")
        for s in range(1, 10):
            out_file = AUDIO_DIR / f"step{s}.mp3"
            synthesize_step(s, args.voice_id, args.model_id, out_file, client)
            desc_file = AUDIO_DIR / (STEP_FILES[s].replace(".txt", ".mp3"))
            import shutil
            shutil.copy2(out_file, desc_file)
        print("🎉 All 9 audio files successfully synthesized with ElevenLabs!")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
