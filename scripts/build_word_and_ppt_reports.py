"""
build_word_and_ppt_reports.py
ينشئ التقرير المكتوب بصيغة Word (.docx) وعرض الشرائح PowerPoint (.pptx)
باللغة العربية الاحترافية وفقاً لمتطلبات وتاسكات المشرفة/الدكتورة.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pptx import Presentation
from pptx.util import Inches as PptxInches, Pt as PptxPt
from pptx.dml.color import RGBColor as PptxRGBColor
from pptx.enum.text import PP_ALIGN

# ==============================================================================
# 1. إنشاء تقرير Word الاحترافي (.docx)
# ==============================================================================
print("Generating Word Document Report (.docx)...")
doc = Document()

# ضبط هوامش الصفحة
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# دالة مساعدة لتنسيق الفقرات
def add_p(text, bold=False, size=12, color=RGBColor(30, 41, 59), align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "Arial"
    run.font.color.rgb = color
    return p

# دالة لإضافة العناوين الرئيسية
def add_heading(text, level=1):
    colors = {
        1: RGBColor(15, 23, 42),   # كحلي غامق
        2: RGBColor(2, 132, 199),  # أزرق سماوي
        3: RGBColor(51, 65, 85)
    }
    sizes = {1: 18, 2: 14, 3: 12}
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(sizes.get(level, 12))
    run.font.name = "Arial"
    run.font.color.rgb = colors.get(level, RGBColor(0, 0, 0))
    return p

# --- صفحة الغلاف / رأس التقرير ---
add_p("بسم الله الرحمن الرحيم", bold=True, size=14, color=RGBColor(100, 116, 139), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(4)
r = title_p.add_run("تقرير المرحلة الأولى: اختيار وتجهيز بيانات مشروع الذكاء الاصطناعي")
r.bold = True
r.font.size = Pt(20)
r.font.color.rgb = RGBColor(15, 23, 42)

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_p.paragraph_format.space_after = Pt(18)
r2 = sub_p.add_run("نظام ذكي لكشف اختراقات الشبكة وتفسير القرارات (X-IDS)")
r2.bold = True
r2.font.size = Pt(15)
r2.font.color.rgb = RGBColor(2, 132, 199)

# خط فاصل
add_p("______________________________________________________________________", size=10, color=RGBColor(203, 213, 225), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

# معلومات الطالب والتسليم
add_p("المشروع: Explainable Network Intrusion Detection System (X-IDS)", bold=True, size=11, color=RGBColor(71, 85, 105))
add_p("تاريخ التسليم: نوفمبر 2026", bold=False, size=11, color=RGBColor(71, 85, 105))
add_p("البيئة البرمجية: Python 3.8 / Visual Studio Code / Scikit-Learn / Pandas", bold=False, size=11, color=RGBColor(71, 85, 105), space_after=18)

# --- 1. اختيار المشروع (Task 1) ---
add_heading("1. اختيار فكرة المشروع ونطاق العمل (Project Selection)", level=1)
add_p("تم اختيار مشروع نظام كشف اختراقات الشبكة القائم على الذكاء الاصطناعي القابل للتفسير (Explainable Network Intrusion Detection System - X-IDS). يهدف المشروع إلى حماية الشبكات من الهجمات السيبرانية الحديثة من خلال فحص تدفقات البيانات (Network Flows) واكتشاف السلوكيات المشبوهة، مع تقديم تفسير دقيق لسبب اعتبار اتصال معين هجوماً بدلاً من العمل كصندوق أسود (Black-box).")
add_p("تم اختيار مجموعة بيانات CIC-IDS2017 Improved الصادرة عن معهد كندا للأمن السيبراني والمصححة علمياً بواسطة جامعة لوفين (Engelen et al.) لضمان دقة النتائج وخلوها من أخطاء الـ Flows والتوقيتات.")

# --- 2. تحديد نوع التعلم الآلي (Task 2) ---
add_heading("2. تحديد نوع التعلم الآلي المستخدم (Classification vs Regression)", level=1)
add_p("طبيعة المشكلة تتطلب اتخاذ قرار حاسم بشأن كل اتصال يمر في الشبكة، لذا فإن النوع المعتمد هو: التعلم الخاضع للإشراف - مهام التصنيف (Supervised Machine Learning – Classification)، ولا نستخدم Regression لأن الهدف ليس توقع كميات مستمرة، بل تصنيف الحالات.")
add_p("ينقسم التصنيف في هذا المشروع إلى مستويين متكاملين:", bold=True)
add_p("• التصنيف الثنائي (Binary Classification): تصنيف الاتصال إلى طبيعي (Normal / BENIGN = 0) أو هجومي (Attack = 1)، وهو الأساس لاكتشاف الهجمات المجهولة والـ Zero-Day.")
add_p("• التصنيف المتعدد (Multiclass Classification): تحديد النوع الدقيق للهجوم (مثل: DoS Hulk, DoS Slowloris, PortScan, Brute Force) لتسهيل اتخاذ الإجراء الأمني المناسب.")

# --- 3. تحديد المدخلات والمخرجات (Tasks 3 & 4) ---
add_heading("3. تحديد المدخلات والهدف (Features vs Target)", level=1)
add_p("• المخرجات / الهدف (Output / Target): هو عمود [Label] الذي يمثل الحقيقة الميدانية (Ground Truth) لكل تدفق شبكي، وتوضح الإحصائيات توزيع الفئات التالية في عينة يوم الأربعاء (Wednesday):")

if os.path.exists("Reports/screenshots/target_distribution.png"):
    doc.add_picture("Reports/screenshots/target_distribution.png", width=Inches(5.5))
    p_img = doc.paragraphs[-1]
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_p("• المدخلات / الخصائص (Inputs / Features): يحتوي كل تدفق على 90 خاصية إحصائية وفيزيائية مستخرجة من حزم البيانات، من أهمها:")
add_p("  1. زمن التدفق الكلي (Flow Duration)")
add_p("  2. إجمالي الحزم المرسلة والمستقبلة (Total Fwd Packet, Total Bwd Packets)")
add_p("  3. معدلات النقل بالبايتات والحزم في الثانية (Flow Bytes/s, Flow Packets/s)")
add_p("  4. الخصائص الإحصائية لأطوال الحزم (Packet Length Max, Min, Mean, Std)")
add_p("  5. أعلام وبروتوكولات الشبكة (SYN, FIN, RST, ACK, PSH Flags)")

# --- 4. استعراض أول 5 سطور وآخر 5 سطور ---
add_heading("4. استعراض عينات من البيانات الحية (head & tail)", level=1)
add_p("تم فحص بنية البيانات عملياً من خلال قراءة الملف واستعراض أطرافه للتأكد من سلامة تحميل الأعمدة وتناسق السجلات:")

add_p("أولاً: أول 5 سجلات من البيانات (df.head()):", bold=True)
if os.path.exists("Reports/screenshots/head_table.png"):
    doc.add_picture("Reports/screenshots/head_table.png", width=Inches(6.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

add_p("ثانياً: آخر 5 سجلات من البيانات (df.tail()):", bold=True)
if os.path.exists("Reports/screenshots/tail_table.png"):
    doc.add_picture("Reports/screenshots/tail_table.png", width=Inches(6.0))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# --- 5. معالجة القيم الفارغة (Tasks 5 & 6) ---
add_heading("5. المعالجة العملية للبيانات المفقودة واللانهائية (dropna vs fillna)", level=1)
add_p("في حركة مرور الشبكات، يؤدي قسمة عدد البايتات على زمن تدفق يساوي صفراً إلى ظهور قيم لانهائية (Infinity)، والتي يجب استبدالها برمجياً بقيم فارغة (NaN) قبل المعالجة.")
add_p("تم تطبيق الأسلوبين المطلوبين ومقارنة النتائج:", bold=True)
add_p("1. أسلوب الحذف (dropna): يقوم بحذف أي سجل يحتوي على قيم غير صالحة. هذا الأسلوب يضمن بيانات نقية 100% لكنه قد يؤدي لخسارة سجلات نادرة إذا كانت العينة صغيرة.")
add_p("2. أسلوب التعويض (fillna): يقوم بملء القيم الفارغة. تم اعتماد التعويض بالوسيط الحسابي (Median) لكل خاصية بدلاً من المتوسط الحسابي، نظراً لأن حركة المرور تحتوي على قيم متطرفة (Outliers) حادة تجعل المتوسط مضللاً.")

if os.path.exists("Reports/screenshots/dropna_vs_fillna.png"):
    doc.add_picture("Reports/screenshots/dropna_vs_fillna.png", width=Inches(4.8))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

# --- 6. الإضافات الاحترافية المنفذة في المشروع (Bonus) ---
add_heading("6. الإضافات الاحترافية المعتمدة لضمان جودة النموذج", level=1)
add_p("• معالجة تصنيفات Attempted: محاولات الهجوم التي لم تسفر عن اختراق مكتمل تم دمجها مع الفئات الطبيعية وفقاً للمنهجية الأكاديمية لباحثي الداتا سيت.")
add_p("• منع الـ Data Leakage: تم إقصاء أعمدة الـ Sockets والوقت (مثل IP العميل، IP الخادم، التوقيت، ورقم البورت) حتى لا يحفظ الموديل أرقام أجهزة معمل الاختبار بدلاً من تعلم سلوك الهجوم.")

# حفظ التقرير
doc_path = "Reports/تقرير_المرحلة_الأولى_مشروع_X-IDS.docx"
doc.save(doc_path)
print(f"[OK] Word document saved to: {doc_path}")


# ==============================================================================
# 2. إنشاء عرض الشرائح التقديمي (.pptx)
# ==============================================================================
print("\nGenerating Presentation Slides (.pptx)...")
prs = Presentation()
prs.slide_width = PptxInches(13.333) # 16:9 Widescreen
prs.slide_height = PptxInches(7.5)

# دالة لإنشاء شريحة بتصميم أنيق
def create_slide(title_text, subtitle_text=""):
    slide_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(slide_layout)

    # شريط علوي ملون
    top_bar = slide.shapes.add_shape(1, 0, 0, PptxInches(13.333), PptxInches(1.2)) # msoShapeRectangle = 1
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = PptxRGBColor(15, 23, 42) # كحلي داكن
    top_bar.line.color.rgb = PptxRGBColor(15, 23, 42)

    # خط أزرق مميز تحت الشريط
    accent_bar = slide.shapes.add_shape(1, 0, PptxInches(1.2), PptxInches(13.333), PptxInches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = PptxRGBColor(2, 132, 199) # سماوي
    accent_bar.line.color.rgb = PptxRGBColor(2, 132, 199)

    # عنوان الشريحة
    tx_box = slide.shapes.add_textbox(PptxInches(0.8), PptxInches(0.18), PptxInches(11.7), PptxInches(0.85))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = PptxPt(26)
    p.font.bold = True
    p.font.color.rgb = PptxRGBColor(255, 255, 255)
    p.font.name = "Arial"
    p.alignment = PP_ALIGN.RIGHT
    return slide

# --- الشريحة 1: شريحة الغلاف ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
bg = slide1.shapes.add_shape(1, 0, 0, PptxInches(13.333), PptxInches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = PptxRGBColor(15, 23, 42)
bg.line.color.rgb = PptxRGBColor(15, 23, 42)

tb = slide1.shapes.add_textbox(PptxInches(1.0), PptxInches(2.0), PptxInches(11.333), PptxInches(3.5))
tf = tb.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "مشروع X-IDS: كشف اختراقات الشبكة بالذكاء الاصطناعي"
p1.font.size = PptxPt(36)
p1.font.bold = True
p1.font.color.rgb = PptxRGBColor(255, 255, 255)
p1.font.name = "Arial"
p1.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "Explainable Network Intrusion Detection System"
p2.font.size = PptxPt(22)
p2.font.color.rgb = PptxRGBColor(56, 189, 248)
p2.font.name = "Arial"
p2.alignment = PP_ALIGN.CENTER

p3 = tf.add_paragraph()
p3.text = "\nالمرحلة الأولى: استكشاف البيانات والتحضير الأولي (Data Preparation & Inspection)\nنوفمبر 2026"
p3.font.size = PptxPt(16)
p3.font.color.rgb = PptxRGBColor(203, 213, 225)
p3.font.name = "Arial"
p3.alignment = PP_ALIGN.CENTER

# --- الشريحة 2: اختيار المشروع (Task 1) ---
slide2 = create_slide("1. فكرة واختيار المشروع (Project Overview)")
tb2 = slide2.shapes.add_textbox(PptxInches(1.0), PptxInches(1.8), PptxInches(11.3), PptxInches(5.0))
tf2 = tb2.text_frame
tf2.word_wrap = True

def add_bullet(tf, title, body):
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.RIGHT
    p.space_after = PptxPt(14)
    r1 = p.add_run()
    r1.text = f"• {title}: "
    r1.font.bold = True
    r1.font.size = PptxPt(18)
    r1.font.color.rgb = PptxRGBColor(15, 23, 42)
    r1.font.name = "Arial"
    
    r2 = p.add_run()
    r2.text = body
    r2.font.size = PptxPt(16)
    r2.font.color.rgb = PptxRGBColor(51, 65, 85)
    r2.font.name = "Arial"

add_bullet(tf2, "اسم المشروع", "نظام ذكي لكشف اختراقات الشبكة وتفسير القرارات (X-IDS).")
add_bullet(tf2, "المشكلة الأمنية", "الأنظمة التقليدية تكتشف الهجمات دون تقديم أسباب مفهومة لفرق الأمن السيبراني (Black-box problem).")
add_bullet(tf2, "الحل المبتكر", "دمج التعلم الآلي مع الذكاء الاصطناعي القابل للتفسير (XAI / SHAP) لتفسير أسباب تصنيف كل تدفق.")
add_bullet(tf2, "مجموعة البيانات", "النسخة المحسنة من CIC-IDS2017 لتجنب أخطاء التدفقات والتوقيتات غير الدقيقة.")

# --- الشريحة 3: نوع التعلم الآلي (Task 2) ---
slide3 = create_slide("2. تحديد نوع التعلم الآلي (Classification vs Regression)")
tb3 = slide3.shapes.add_textbox(PptxInches(1.0), PptxInches(1.8), PptxInches(11.3), PptxInches(5.0))
tf3 = tb3.text_frame
tf3.word_wrap = True

add_bullet(tf3, "النوع المعتمد", "Supervised Machine Learning – Classification (تصنيف تحت إشراف).")
add_bullet(tf3, "سبب عدم استخدام Regression", "المطلوب أمنياً هو اتخاذ قرار حاسم بنوع الاتصال (هجوم أم طبيعي) وليس توقع قيم رقمية مستمرة.")
add_bullet(tf3, "التصنيف الثنائي (Binary)", "تصنيف الاتصال كـ (Normal = 0) مقابل (Attack = 1) لتمكين اكتشاف الهجمات المستجدة (Zero-Day).")
add_bullet(tf3, "التصنيف المتعدد (Multiclass)", "تحديد نوع الهجوم بدقة (DoS, PortScan, Brute Force) لتفعيل الاستجابة المناسبة.")

# --- الشريحة 4: المدخلات والمخرجات (Tasks 3 & 4) ---
slide4 = create_slide("3. تحديد المدخلات والهدف (Inputs vs Outputs)")
tb4 = slide4.shapes.add_textbox(PptxInches(6.8), PptxInches(1.8), PptxInches(5.8), PptxInches(5.0))
tf4 = tb4.text_frame
tf4.word_wrap = True

add_bullet(tf4, "المخرجات (Target / Label)", "عمود Label الذي يمثل نوع الاتصال الفعلي (BENIGN أو DoS Hulk أو Slowloris).")
add_bullet(tf4, "المدخلات (Features / Inputs)", "أكثر من 80 خاصية رقمية تصف سلوك الشبكة (زمن التدفق، حجم الحزم، معدل النقل، الأعلام).")

if os.path.exists("Reports/screenshots/target_distribution.png"):
    slide4.shapes.add_picture("Reports/screenshots/target_distribution.png", PptxInches(0.8), PptxInches(2.0), width=PptxInches(5.6))

# --- الشريحة 5: استعراض أول 5 وآخر 5 سطور ---
slide5 = create_slide("4. استعراض عينات من البيانات الحية (head & tail)")
tb5 = slide5.shapes.add_textbox(PptxInches(1.0), PptxInches(1.4), PptxInches(11.3), PptxInches(0.6))
p5 = tb5.text_frame.paragraphs[0]
p5.text = "استعراض السجلات الحية داخل البيئة البرمجية للتحقق من قراءة الـ 90 عموداً وتناسق القيم:"
p5.alignment = PP_ALIGN.RIGHT
p5.font.size = PptxPt(14)
p5.font.name = "Arial"

if os.path.exists("Reports/screenshots/head_table.png"):
    slide5.shapes.add_picture("Reports/screenshots/head_table.png", PptxInches(1.0), PptxInches(2.1), width=PptxInches(11.3))

if os.path.exists("Reports/screenshots/tail_table.png"):
    slide5.shapes.add_picture("Reports/screenshots/tail_table.png", PptxInches(1.0), PptxInches(4.8), width=PptxInches(11.3))

# --- الشريحة 6: معالجة القيم الفارغة (Tasks 5 & 6) ---
slide6 = create_slide("5. معالجة القيم الفارغة (dropna vs fillna)")
tb6 = slide6.shapes.add_textbox(PptxInches(6.5), PptxInches(1.8), PptxInches(6.0), PptxInches(5.0))
tf6 = tb6.text_frame
tf6.word_wrap = True

add_bullet(tf6, "تحدي الـ Infinity", "قسمة البايتات على صفر تسبب قيم Inf، ويتم تحويلها لـ NaN أولاً.")
add_bullet(tf6, "تطبيق dropna()", "حذف السجلات المعطوبة بالكامل لضمان نقاء التدريب.")
add_bullet(tf6, "تطبيق fillna()", "التعويض بالوسيط الحسابي (Median) لحماية البيانات من تأثير القيم المتطرفة (Outliers).")

if os.path.exists("Reports/screenshots/dropna_vs_fillna.png"):
    slide6.shapes.add_picture("Reports/screenshots/dropna_vs_fillna.png", PptxInches(0.8), PptxInches(2.2), width=PptxInches(5.3))

# --- الشريحة 7: الإضافات وخطة الأسبوع القادم ---
slide7 = create_slide("6. التميز العلمي وخطة الأسبوع القادم")
tb7 = slide7.shapes.add_textbox(PptxInches(1.0), PptxInches(1.8), PptxInches(11.3), PptxInches(5.0))
tf7 = tb7.text_frame
tf7.word_wrap = True

add_bullet(tf7, "حماية النموذج من الـ Leakage", "حذف معرّفات الـ Sockets والـ IPs حتى لا يحفظ الموديل أجهزة المعمل.")
add_bullet(tf7, "معالجة حالات Attempted", "إعادة تصنيف محاولات الاختراق غير الناجحة كـ Benign طبقاً للبحث المعتمد.")
add_bullet(tf7, "المرحلة القادمة", "تجهيز الـ Features وتقسيم البيانات (Train/Test Split) وتدريب النماذج الأساسية (Random Forest & XGBoost).")

# حفظ البريزنتيشن
ppt_path = "Reports/عرض_تقديمي_المرحلة_الأولى_X-IDS.pptx"
prs.save(ppt_path)
print(f"[OK] PowerPoint presentation saved to: {ppt_path}")
