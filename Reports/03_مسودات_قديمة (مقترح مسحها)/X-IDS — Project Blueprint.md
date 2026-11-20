# X-IDS — Project Blueprint

**Explainable Network Intrusion Detection System على CIC-IDS2017**

نظام لاكتشاف الهجمات السيبرانية باستخدام Machine Learning وExplainable AI، مبني على Dataset واحدة وتجارب تعميم داخلها.

Version 2.0 — November 2026

## 1. الملخص التنفيذي

يقترح هذا المشروع نظام كشف تسلل شبكي (**Network Intrusion Detection System**) يعتمد على **Machine Learning**، ويستخدم Dataset واحدة هي **CIC-IDS2017**. تم اتخاذ قرار عدم الدمج بين أكثر من Dataset لأن توحيد الخصائص (Feature Alignment) هو أصعب وأكثر أجزاء المشروع خطورة منهجيًا، ويستهلك وقتًا يفوق قيمته.

بدلًا من ذلك، يختبر المشروع قدرة النموذج على **التعميم داخل نفس الـ Dataset** عبر سيناريوهات مختلفة: تقسيم زمني، واستبعاد نوع هجوم كامل من التدريب ثم اختباره. وبذلك يحتفظ المشروع بفكرته المميزة بجهد أقل.

المكونات الأساسية:

- **Model Comparison:** مقارنة أربع خوارزميات بمنهجية تقييم موحدة.
- **Generalization Testing:** Chronological Split وLeave-one-attack-out.
- **Explainable AI:** تفسير القرارات باستخدام SHAP.
- **Security Dashboard:** واجهة Streamlit لعرض النتائج.
- **Live Detection (اختياري):** تحليل traffic فعلي باستخدام CICFlowMeter.

**الفكرة التي تميز المشروع:** لا نقيس نجاح النموذج بالـ Accuracy، لأن CIC-IDS2017 يصل فيها بسهولة إلى أكثر من 99%. نقيس هل يكتشف النموذج هجومًا لم يره أثناء التدريب، ولماذا اتخذ قراره.

## 2. اختيار الـ Dataset: ثلاث نسخ مصححة والترشيح النهائي

الترشيح النهائي: **CIC-IDS2017 المصححة (Engelen وآخرون)**، وتُستخدم مباشرة دون تجربة غيرها. الأسباب والتفاصيل أدناه.

النسخ الأصلية من CIC-IDS2017 وCSE-CIC-IDS2018 فيها أخطاء موثقة (أخطاء في بناء الـ Flows وفي الـ Labels، تقارب 6.67% و7.53% على التوالي في دراسة لاحقة)، لذلك اقتصرت المراجعة على النسخ المصححة.

### 2.1 CIC-IDS2017 المصححة (Engelen وآخرون، 2021)

**ما هي:** أُعيد توليد الـ Flows من ملفات PCAP الخمسة الأصلية (ملف لكل يوم من الاثنين إلى الجمعة) بنسخة معدلة من CICFlowMeter، ثم أُعيد تصنيفها بمنطق Labeling منشور. النتيجة أن أكثر من 20% من الـ traces الأصلية أُعيد بناؤها أو تصنيفها.

**المميزات:**

- متاحة للتحميل من صفحة المؤلفين (downloads.distrinet-research.be/WTMC2021) كملفات جاهزة، والكود المستخدم منشور على GitHub.
- نفس سيناريوهات الهجمات الأصلية: Brute Force وDoS وWeb Attacks وInfiltration وBotnet وPortScan وDDoS، بنفس تقسيم الأيام.
- أنظف بكثير من الأصلية، وسُجل عليها أعلى أداء ذُكر لهذه البيانات.
- مراجع كثيرة عن CIC-IDS2017 يمكن الاستناد إليها في الدوكيومنت واللجنة.
- الخصائص من نمط CICFlowMeter، فيبقى مسار Live Detection ممكنًا بنفس الأداة.
- حجم يناسب جهازًا عاديًا مع Sampling للفئة الطبيعية.

**العيوب:**

- بيئة الشبكة أصغر وأبسط من بيئة 2018.
- أنظف وأسهل، فالنتائج تقترب من الكمال في التقسيم العشوائي، لذلك تجارب B وC ضرورية لإظهار القيمة.
- الفئات النادرة (Heartbleed وInfiltration وSQL Injection) غالبًا ما زالت قليلة العدد، وتُدمج أو تُستبعد من Multi-class.
- الأداة المعدلة وكودها "Research code" وليست منتجًا مستقرًا، وهذا مهم عند Live Detection.

### 2.2 CSE-CIC-IDS2018 المصححة (Liu وآخرون، 2022)

**ما هي:** إعادة بناء لـ CSE-CIC-IDS2018 من الـ PCAP الخام، مع Labeling logic مُعاد هندسته ومنشور. الأصلية تغطي حوالي 10 أيام، بشبكة فيها حوالي 50 جهاز مهاجم و420 جهازًا و30 خادمًا، وفيها حوالي 16 مليون Flow و84 خاصية، ونفس أنواع الهجمات تقريبًا مثل 2017.

**المميزات:**

- شبكة أكبر وأنظمة أكثر تنوعًا، فهي أقرب لبيئة حقيقية.
- حجم أكبر يعطي عينات أكثر لكل هجوم.
- منطق التصنيف شفاف ومنشور، ويمكن إعادة إنتاجه.
- متوافقة مع CICFlowMeter.

**العيوب:**

- حجم ضخم يحتاج Sampling وذاكرة وتخزينًا كبيرين.
- قد لا تتوفر كملفات CSV جاهزة، وإعادة التوليد تعني تنزيل الـ PCAP الخام وتشغيل الأداة المعدلة مرة لكل يوم، مع حذف ملف مكرر معروف في يوم الجمعة 02-03-2018، وهذا جهد كبير وعرضة للأخطاء.
- مراجعها أقل من CIC-IDS2017.
- لم أستطع التحقق من رابط تحميل مباشر لملفاتها الجاهزة لأن موقع المصدر يمنع الوصول الآلي.

### 2.3 BCCC-CSE-CIC-IDS2018 (York University، 2025)

**ما هي:** نسخة محسّنة من CSE-CIC-IDS2018 فيها حوالي 46 مليون سجل مصنف و300 خاصية، استُخرجت بأداة جديدة اسمها NTLFlowLyzer بدل CICFlowMeter. صُححت Labels الـ DoS بربطها بعناوين المهاجمين بدل التوقيت، وحُذفت هجمات UDP التي كانت مصنفة خطأ، وأُبقيت الهجمات قليلة العدد دون تحليل.

**المميزات:**

- الأحدث بين الثلاثة، وتصحيحها موثق في ورقة منشورة (2025).
- خصائص غنية جدًا.
- معالجة صريحة لمشاكل الخصائص وبناء الـ Flows.

**العيوب:**

- التحميل بطلب وصول (Request Dataset)، وقد تنتظر موافقة.
- 300 خاصية تجعل SHAP أبطأ وأصعب في الشرح للجنة.
- Live Detection يحتاج NTLFlowLyzer وليس CICFlowMeter، فمسار مختلف تمامًا.
- حجم 46 مليون سجل ثقيل جدًا.
- حذف هجمات UDP يقلل تنوع هجمات DoS.
- مراجع قليلة لأنها حديثة.

### 2.4 الترشيح النهائي

**استخدموا CIC-IDS2017 المصححة.** هي الوحيدة من الثلاثة التي تأكدت أنها متاحة كملفات جاهزة من المؤلفين، وبنيتها (خمسة أيام وسيناريوهات معروفة) تطابق تصميم التجارب في هذا الدوكيومنت دون تعديل، وحجمها مناسب، ومراجعها كثيرة، ومسار Live Detection فيها ممكن بـ CICFlowMeter.

**ملاحظة صريحة:** رشحت سابقًا CSE-CIC-IDS2018 المصححة كخيار أول. غيرت ذلك لأنني لم أستطع التأكد من توفر ملفاتها الجاهزة، وإعادة توليدها جهد كبير قد يضيع وقت المشروع.

**قبل البدء:** تأكد أن الملفات التي حملتها هي النسخة المصححة وليست الأصلية، فكثير من الملفات المتداولة تحمل الـ Labels الأصلية.

المصادر: [Troubleshooting CICIDS2017 (Engelen وآخرون)](https://lirias.kuleuven.be/retrieve/713070) · [Error Prevalence in NIDS datasets (Liu وآخرون)](https://intrusion-detection.distrinet-research.be/CNS2022/index.html) · [كود إعادة بناء 2018](https://www.github.com/GintsEngelen/CNS2022_Code) · [BCCC-CSE-CIC-IDS2018](https://www.yorku.ca/research/bccc/ucs-technical/cybersecurity-datasets-cds/large-scale-intrusion-detection-dataset-bccc-cse-cic-ids2018/) · [طلب BCCC](http://bccc.laps.yorku.ca/BCCC-CSE-CIC-IDS-2018/) · [Network Intrusion Datasets Survey](https://arxiv.org/pdf/2502.06688)

## 3. المشكلة والهدف البحثي

### 3.1 السؤال البحثي

هل يستطيع نموذج Machine Learning مدرب على CIC-IDS2017 اكتشاف هجمات لم يرها أثناء التدريب، والحفاظ على نسبة إنذارات كاذبة منخفضة، مع تفسير قراراته؟

### 3.2 الأهداف

- بناء نموذج **Binary Classification** للتمييز بين Normal وAttack.
- بناء نموذج **Multi-class Classification** لتحديد عائلة الهجوم.
- مقارنة Logistic Regression وDecision Tree وRandom Forest وXGBoost.
- اختبار التعميم عبر Chronological Split وLeave-one-attack-out.
- تفسير القرارات باستخدام SHAP على المستويين العام والمحلي.
- بناء Dashboard تعرض النتائج والتفسيرات.
- تجهيز مسار Live Detection كمرحلة اختيارية.

## 4. نطاق المشروع

| ضمن النطاق الأساسي | خارج النطاق / تطوير لاحق |
| --- | --- |
| تحليل CIC-IDS2017 فقط | دمج أكثر من Dataset |
| Binary وMulti-class Classification | منع الهجمات تلقائيًا |
| مقارنة النماذج وتجارب التعميم | تشغيل دائم على شبكة إنتاجية |
| SHAP وDashboard على ملفات CSV | تكامل كامل مع SIEM/SOC |
| Live Detection تجريبي (اختياري) | استجابة آلية للحوادث |

## 5. وصف الـ Dataset

تحتوي CIC-IDS2017 على traffic لخمسة أيام (من الاثنين إلى الجمعة)، وتوزيع الهجمات كالتالي:

| اليوم | المحتوى |
| --- | --- |
| الاثنين | Normal فقط |
| الثلاثاء | Brute Force (FTP-Patator وSSH-Patator) |
| الأربعاء | DoS (Slowloris وSlowhttptest وHulk وGoldenEye) وHeartbleed |
| الخميس | Web Attacks (Brute Force وXSS وSQL Injection) وInfiltration |
| الجمعة | Botnet وPortScan وDDoS |

### 5.1 مشاكل معروفة يجب معالجتها

- أسماء أعمدة تحتوي مسافات زائدة في بدايتها.
- قيم **NaN** وInfinity في أعمدة مثل Flow Bytes/s وFlow Packets/s.
- صفوف مكررة بأعداد كبيرة.
- عمود مكرر في بعض النسخ (Fwd Header Length).
- فئات نادرة جدًا (Heartbleed وInfiltration وSQL Injection) لا تكفي للتدريب والتقييم المستقل.
- أعمدة تعريفية (Flow ID وSource IP وDestination IP وTimestamp) قد تتحول إلى Shortcuts يتعلم منها النموذج بدل سلوك الهجوم.

### 5.2 قرارات التجهيز

- حذف الأعمدة التعريفية من الـ Features، والاحتفاظ بـ Timestamp فقط لأغراض التقسيم الزمني.
- معالجة NaN وInfinity وحذف التكرار قبل أي تقسيم.
- دمج الفئات النادرة في فئات أكبر (مثل Web Attacks) أو استبعادها من Multi-class مع توثيق ذلك.
- تجربة **Destination Port** مرة بوجوده ومرة بدونه، لأنه قد يسبب اعتمادًا زائدًا على المنفذ بدل سلوك الـ Flow.
- تقليل عدد الـ Benign Flows بـ Downsampling على بيانات التدريب فقط لتسريع التجارب.

## 6. المعمارية المقترحة

| المرحلة | المسؤولية |
| --- | --- |
| 1. Data Source | ملفات CIC-IDS2017 بصيغة CSV |
| 2. Data Preparation | تنظيف الأعمدة، معالجة NaN/Infinity، حذف التكرار، حذف الأعمدة التعريفية |
| 3. Splitting | تقسيم يحترم الزمن أو نوع الهجوم، قبل تعلم أي تحويلات |
| 4. ML Engine | تدريب النماذج وإنتاج Binary وMulti-class Predictions |
| 5. Evaluation | Precision وRecall وF1 وMacro F1 وFPR وPR-AUC وConfusion Matrix |
| 6. Explainability | SHAP العام والمحلي |
| 7. Dashboard | عرض الإحصائيات والتوقعات والمقارنات والتفسيرات |
| 8. Live Detection (اختياري) | CICFlowMeter ثم النموذج ثم التنبيه |

## 7. منهجية التجارب

### 7.1 Experiment A — Baseline (Random Stratified Split)

تقسيم عشوائي متوازن لحساب الأداء المرجعي. هذه التجربة **متفائلة عادة** وتستخدم فقط لإظهار الفرق بينها وبين التجارب الأكثر واقعية.

### 7.2 Experiment B — Chronological Split

داخل كل يوم، يُستخدم أول 70% من الزمن للتدريب وآخر 30% للاختبار، مع فاصل زمني صغير بينهما لمنع التسرب بين الـ Flows المتجاورة. الهدف قياس الأداء عندما لا يرى النموذج المستقبل.

### 7.3 Experiment C — Leave-one-attack-out

يُستبعد نوع هجوم كامل (مثل DoS أو PortScan أو Botnet) من بيانات التدريب، ثم يُختبر النموذج على بيانات تحتوي هذا الهجوم. يُقاس **Recall** على الهجوم غير المرئي، وتُراجع الـ Features التي ساعدت النموذج على اكتشافه باستخدام SHAP. تُكرر التجربة لكل عائلة هجوم رئيسية.

| التجربة | التدريب | الاختبار | الهدف |
| --- | --- | --- | --- |
| A | Random 70% | Random 30% | أداء مرجعي (متفائل) |
| B | أول 70% زمنيًا من كل يوم | آخر 30% زمنيًا | أداء واقعي على المستقبل |
| C | كل الهجمات عدا عائلة واحدة | بيانات تحتوي العائلة المستبعدة | قدرة اكتشاف هجوم جديد |

**أهم تجربة بحثية:** Experiment C، لأنها تختبر هل تعلم النموذج سلوكًا عامًا للهجوم أم حفظ توقيعات الهجمات المعروفة.

## 8. نماذج Machine Learning

| الخوارزمية | دورها |
| --- | --- |
| Logistic Regression | Baseline بسيط وسريع |
| Decision Tree | قابلية الفهم وقواعد واضحة |
| Random Forest | نموذج تجميعي قوي للبيانات الجدولية |
| XGBoost | نموذج متقدم غالبًا الأفضل أداءً |

### 8.1 خطة لتقليل جهد التدريب

- ضبط الـ Hyperparameters على عينة صغيرة (Stratified Sample) ثم التدريب النهائي على البيانات كاملة.
- استخدام `n_jobs=-1` في Random Forest، و`tree_method="hist"` في XGBoost.
- حفظ النماذج المدربة بـ `joblib` لتجنب إعادة التدريب.
- استخدام Pipelines حتى لا تتسرب معلومات الاختبار إلى التدريب.
- يُختار النموذج النهائي بتوازن الأداء والتعميم ومعدل الإنذارات الكاذبة وزمن التنفيذ، وليس بالـ Accuracy وحدها.

## 9. Explainable AI باستخدام SHAP

| نوع التفسير | ما الذي يوضحه |
| --- | --- |
| Global | الخصائص الأكثر تأثيرًا عبر عينة كبيرة |
| Local | سبب تصنيف Flow محدد كهجوم |
| مقارنة بين الهجمات | الخصائص المميزة لكل عائلة هجوم |
| تحليل الأخطاء | سبب False Positive وFalse Negative |

- يُستخدم **TreeExplainer** مع النماذج الشجرية على عينة (5 إلى 10 آلاف Flow) لتقليل الزمن.
- في Experiment C، تُقارن الخصائص المؤثرة في الهجوم المكتشف والهجوم الذي فشل النموذج في اكتشافه.

**حدود التفسير:** SHAP يوضح مساهمة الخصائص في قرار النموذج فقط، ولا يثبت أنها السبب الحقيقي للهجوم.

## 10. التقييم ومقاييس الأداء

| المقياس | أهميته |
| --- | --- |
| Precision | تقليل الإنذارات الكاذبة |
| Recall | تقليل الهجمات الفائتة |
| F1 وMacro F1 | مقارنة متوازنة مع تفاوت أحجام الفئات |
| False Positive Rate | عبء الإنذارات على المحلل |
| PR-AUC | مناسب مع عدم توازن الفئات |
| Confusion Matrix | تحليل الأخطاء بالتفصيل |

الـ Accuracy تُعرض للمرجعية فقط ولا تُستخدم للحكم على النموذج.

### 10.1 منع Data Leakage

- التقسيم قبل تعلم أي تحويلات (Scaling وEncoding وImputation).
- تعلم التحويلات من بيانات التدريب فقط.
- حذف التكرار قبل التقسيم.
- عدم استخدام بيانات الاختبار لاختيار الخصائص أو ضبط Hyperparameters.
- Resampling وClass Weights على التدريب فقط.
- حذف الأعمدة التعريفية من الخصائص.

## 11. تصميم Dashboard

تُبنى باستخدام **Streamlit** من خمس صفحات:

| الصفحة | المحتوى |
| --- | --- |
| Overview | عدد الـ Flows، الطبيعي والهجومي، ونسب التوزيع |
| Traffic Analysis | رفع ملف CSV وعرض التصنيف وتصفية الـ Flows |
| Attack Intelligence | توزيع أنواع الهجمات |
| Model Performance | مقارنة النماذج ونتائج التجارب A وB وC |
| Explainable AI | SHAP العام والمحلي |

نتائج الإصدار الأول ناتجة عن تحليل ملف CSV يرفعه المستخدم، وليست مراقبة مباشرة للشبكة.

## 12. Live Detection (مرحلة اختيارية)

تصبح هذه المرحلة ممكنة لأن CIC-IDS2017 مبنية على CICFlowMeter:

- استخراج Flows من traffic حي أو من ملف PCAP باستخدام CICFlowMeter.
- مطابقة أسماء الخصائص ووحداتها مع بيانات التدريب.
- تمرير الـ Flows للنموذج وعرض التنبيهات في الـ Dashboard.
- **أول اختبار:** إعادة تشغيل ملفات PCAP الأصلية للـ Dataset ومقارنة الخصائص المستخرجة بالـ CSV الأصلي، للتأكد أن الأداة تنتج نفس القيم.

**تحذير:** إصدارات CICFlowMeter تختلف في طريقة حساب بعض الخصائص، فقد ينخفض الأداء الحي رغم نجاحه على الـ CSV. هذه المرحلة تُنفذ فقط بعد اكتمال باقي المشروع.

## 13. التقنيات والأدوات

| المجال | الأدوات |
| --- | --- |
| اللغة | Python |
| معالجة البيانات | Pandas, NumPy |
| الرسوم | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn, XGBoost |
| Explainable AI | SHAP |
| الواجهة | Streamlit |
| Live Detection | CICFlowMeter |

## 14. مراحل التنفيذ

| المرحلة | الاسم | المهام | المخرج |
| --- | --- | --- | --- |
| 1 | Data Preparation | تحميل الملفات، التنظيف، حذف التكرار، قرارات الأعمدة | نسخة نظيفة ووصف للبيانات |
| 2 | EDA | توزيع الفئات والأيام والقيم الشاذة | تقرير EDA |
| 3 | Baseline Models | Experiment A على الأربع نماذج | نتائج مرجعية |
| 4 | Generalization Testing | Experiment B وC | أهم نتائج المشروع |
| 5 | Multi-class | تصنيف عائلات الهجمات بعد دمج الفئات النادرة | نتائج متعددة الفئات |
| 6 | Explainable AI | SHAP العام والمحلي وتحليل الأخطاء | رسوم وتفسيرات |
| 7 | Dashboard | Streamlit بخمس صفحات | تطبيق قابل للعرض |
| 8 | Live Detection (اختياري) | CICFlowMeter واختبار PCAP | نموذج تجريبي |

## 15. المخاطر والتحديات

| التحدي | المشكلة | المعالجة |
| --- | --- | --- |
| Accuracy مبالغ فيها | نتائج 99%+ بسبب تشابه الـ Flows | Chronological Split وLeave-one-attack-out |
| جودة الـ Labels | أخطاء في الـ Labels والـ Flows | توثيق التنظيف أو استخدام نسخة مصححة |
| فئات نادرة | Heartbleed وInfiltration وSQL Injection | دمجها أو استبعادها من Multi-class |
| Shortcut Learning | اعتماد النموذج على Port أو أعمدة تعريفية | حذف الأعمدة التعريفية وتجربة بدون Destination Port |
| حجم البيانات | ملفات ثقيلة وتدريب بطيء | Downsampling للـ Benign على التدريب فقط وحفظ النماذج |
| Feature Mismatch في Live | اختلاف CICFlowMeter عن الـ CSV | اختبار PCAP أولًا |
| False Positives | عبء إنذارات كاذبة | قياس FPR وضبط Threshold |

## 16. معايير نجاح المشروع

- نتائج موثقة وقابلة لإعادة التنفيذ.
- مقارنة عادلة بين أربعة نماذج على الأقل.
- عرض Precision وRecall وF1 وMacro F1 وFPR، وليس Accuracy فقط.
- تنفيذ Experiments A وB وC وتفسير الفرق بينها.
- تحليل SHAP للخصائص المؤثرة، وتفسير حالات False Positive وFalse Negative.
- Dashboard تعمل على ملفات CSV وتعرض النتائج بوضوح.
- توثيق القيود وعدم الادعاء بأن النظام يكتشف كل الهجمات.

## 17. أهم التغييرات عن الإصدار 1.0

| العنصر | الإصدار 1.0 | الإصدار 2.0 |
| --- | --- | --- |
| الـ Datasets | UNSW-NB15 وCIC-IDS2017 | CIC-IDS2017 فقط |
| Feature Alignment | مطلوب | غير مطلوب |
| التعميم | Cross-Dataset | Chronological Split وLeave-one-attack-out |
| عدد التجارب | A وB (اتجاهين) وC | A وB وC (أخف) |
| Live Detection | صعب (خصائص مشتركة قليلة) | ممكن عبر CICFlowMeter |

## 18. الخلاصة والمراجع

يحتفظ X-IDS بالقيمة البحثية للمشروع الأصلي (التعميم والتفسير) دون عبء دمج مجموعتي بيانات. ويُوصى بالتنفيذ تدريجيًا: تنظيف البيانات، ثم النماذج المرجعية، ثم تجارب التعميم، ثم SHAP، ثم الواجهة، وترك Live Detection للنهاية.

- [CIC-IDS2017 — Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html)
- [Network Intrusion Detection: A Comprehensive Analysis of CIC-IDS2017 (ICISSP 2022)](https://scitepress.org/PublishedPapers/2022/107740/pdf/index.html)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
