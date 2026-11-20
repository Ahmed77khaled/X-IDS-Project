# -*- coding: utf-8 -*-
"""
🎧 دالة الاستماع للشرح الصوتي (listen helper)
انسخ هذا الكود أو شغله في أي Notebook للاستماع لشرح خطوات مشروع X-IDS
"""
from IPython.display import Audio, display
from pathlib import Path

def listen(step):
    """
    دالة مساعدة للاستماع للشرح الصوتي لأي خطوة في المشروع.
    أمثلة:
      listen(1)                         # تشغيل audio/step1.mp3
      listen("step2")                   # تشغيل audio/step2.mp3
      listen("step1_dataset_inspection")# تشغيل بالاسم الوصفي إذا وجد
    """
    step_str = str(step).strip().lower()
    if not step_str.endswith(".mp3"):
        # جرب أولاً إذا كان رقماً فقط أو يبدأ بـ step
        if step_str.isdigit():
            step_str = f"step{step_str}.mp3"
        elif not step_str.startswith("step"):
            step_str = f"step_{step_str}.mp3"
        else:
            step_str = f"{step_str}.mp3"

    candidates = [
        Path("audio") / step_str,
        Path("../audio") / step_str,
        Path("project/audio") / step_str,
        Path(f"audio/step{step}.mp3"),
        Path(f"../audio/step{step}.mp3")
    ]
    for p in candidates:
        if p.exists():
            display(Audio(str(p)))
            return
    print(f"⚠️ لم يتم العثور على ملف الصوت: {step_str}")

# مثال: تشغيل شرح الخطوة الأولى
listen(1)
