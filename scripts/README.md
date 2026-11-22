# 🛠️ X-IDS Developer Scripts & Maintenance Tools

This directory contains internal developer utilities, data processors, pipeline engines, and report generators for the **X-IDS (Explainable AI Network Intrusion Detection System)** project.

---

## 📋 Catalog of Scripts

| Script | Purpose & Description |
| :--- | :--- |
| **`setup_dataset.py`** | Intelligent 4-scenario dataset resolver & auto-downloader called by launchers. |
| **`launch_vscode.py`** | Multi-path deep detector (Registry, Program Files, AppData) for VS Code. |
| **`download_data.py`** | CLI verification tool for dataset integrity, schema checks, and zip extraction. |
| **`x_ids_pipeline.py`** | Complete end-to-end ML pipeline (preprocessing, leak-prevention, XGBoost, SHAP). |
| **`generate_sample_dataset.py`** | Generates a lightweight synthetic dataset (`data/cic_ids2017_sample.csv`). |
| **`generate_report_evidence.py`** | Runs milestone data cleaning and exports screenshots and tables for reports. |
| **`build_guided_notebook.py`** | Template compiler that builds the student notebook with audio/cards. |
| **`build_word_and_ppt_reports.py`** | Automated builder for formal academic Word (`.docx`) and PowerPoint (`.pptx`) reports. |
| **`generate_voice_samples.py`** | ElevenLabs / Edge-TTS audio generator for Felho voice guides. |
| **`fix_rtl_notebook.py`** | Formats and injects RTL styling into Jupyter notebook cells. |
| **`update_notebook.py`** | Applies updates and improvements to notebook templates. |
| **`reset_student_notebook.py`** | Resets `my_model_training.ipynb` to clean initial milestone state. |
| **`requirements-audio.txt`** | Maintainer-only dependencies for edge-tts and elevenlabs. |

---

## 🚀 Running from Project Root

All scripts automatically resolve the project root and work properly whether run from the project root:
```bash
python scripts/setup_dataset.py
python scripts/download_data.py --info
```
or directly from inside the `scripts/` directory:
```bash
cd scripts
python setup_dataset.py
```
