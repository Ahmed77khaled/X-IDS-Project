import os
import sys
import asyncio

# Prevent Windows Proactor event loop issues on Python 3.8 Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import edge_tts

OUTPUT_DIR = r"D:\HIE\AI\05 - ملخصات ومشاريع (Summaries & Labs)\project\audio\samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Egyptian Script (Colloquial Egyptian with 100% Arabic Phonetics)
SCRIPT_EG = (
    "أهلاً بيك. في الخطوة الأولى من المشروع، بنجهز بيئة العمل ونستدعي التلات مكتبات الأساسية "
    "اللي هنعتمد عليهم في معالجة البيانات وبناء النموذج. "
    "أول مكتبة هي مكتبة بانداس، بالاسم المختصر بي دي، ودي المسؤولة عن قراءة ملفات البيانات سي إس في "
    "والتعامل مع الجداول والداتا فريم. "
    "تاني مكتبة هي مكتبة نمباي، بالاسم المختصر إن بي، ودي بتعمل العمليات الرياضية السريعة "
    "وإدارة المصفوفات ومعالجة القيم المفقودة. "
    "تالت مكتبة هي مكتبة مات بلوت ليب دوت باي بلوت، بالاسم المختصر بي إل تي، "
    "ودي بنستخدمها لتجهيز ورسم المخططات البيانية لاكتشاف البيانات. "
    "في الكود، بنكتب أمر إمبورت لكل مكتبة، وبعدها أمر الطباعة برنت عشان نتأكد إن الاستدعاء تم بنجاح. "
    "دلوقتي دورك: اكتب كود الاستدعاء في الخلية، واضغط شيفت مع إنتر عشان نتنقل للخطوة اللي بعدها."
)

# Modern Standard Arabic Script (Fusha with 100% Arabic Phonetics)
SCRIPT_FUSHA = (
    "مرحباً بكم. في الخطوة الأولى من المشروع، نبدأ بتجهيز بيئة العمل واستدعاء المكتبات البرمجية الأساسية "
    "التي سنعتمد عليها في معالجة البيانات وبناء النموذج الذكي. "
    "المكتبة الأولى هي مكتبة بانداس، بالاسم المختصر بي دي، وهي المسؤولة عن قراءة ملفات البيانات سي إس في "
    "والتعامل مع الجداول والداتا فريم. "
    "المكتبة الثانية هي مكتبة نمباي، بالاسم المختصر إن بي، وتُستخدم لإجراء العمليات الحسابية السريعة "
    "وإدارة المصفوفات ومعالجة القيم المفقودة. "
    "المكتبة الثالثة هي مكتبة مات بلوت ليب دوت باي بلوت، بالاسم المختصر بي إل تي، "
    "وهي المسؤولة عن إنشاء الرسوم البيانية والمخططات الإحصائية لاستكشاف البيانات. "
    "في الكود، نستخدم أمر الاستيراد إمبورت لكل مكتبة، متبوعاً بأمر الطباعة برنت للتأكد من نجاح التحميل. "
    "الآن جاء دورك: اكتب كود الاستدعاء، ثم اضغط شيفت مع إنتر للانتقال إلى الخطوة التالية."
)

SAMPLES = [
    {
        "filename": "sample_eg_salma.mp3",
        "voice": "ar-EG-SalmaNeural",
        "script": SCRIPT_EG,
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Egyptian Female (Salma) - Conversational, warm educational"
    },
    {
        "filename": "sample_eg_shakir_tuned.mp3",
        "voice": "ar-EG-ShakirNeural",
        "script": SCRIPT_EG,
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Egyptian Male (Shakir) - Phonetically smoothed, professional technical"
    },
    {
        "filename": "sample_fusha_hamed.mp3",
        "voice": "ar-SA-HamedNeural",
        "script": SCRIPT_FUSHA,
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Modern Standard Arabic Male (Hamed) - Academic, authoritative documentary"
    },
    {
        "filename": "sample_fusha_zariyah.mp3",
        "voice": "ar-SA-ZariyahNeural",
        "script": SCRIPT_FUSHA,
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Modern Standard Arabic Female (Zariyah) - Crisp educational, clear standard"
    }
]

async def generate_sample(sample):
    out_path = os.path.join(OUTPUT_DIR, sample["filename"])
    print(f"Generating {sample['filename']} using {sample['voice']}...")
    communicate = edge_tts.Communicate(
        text=sample["script"],
        voice=sample["voice"],
        rate=sample["rate"],
        pitch=sample["pitch"]
    )
    await communicate.save(out_path)
    size = os.path.getsize(out_path)
    print(f"✅ Generated {sample['filename']}: {size:,} bytes")
    return {
        "filename": sample["filename"],
        "voice": sample["voice"],
        "desc": sample["desc"],
        "size": size,
        "path": out_path
    }

async def main():
    results = []
    for s in SAMPLES:
        res = await generate_sample(s)
        results.append(res)
    print("\nAll samples generated successfully!")
    for r in results:
        print(f"- {r['filename']} ({r['voice']}): {r['size']:,} bytes")

if __name__ == "__main__":
    asyncio.run(main())
