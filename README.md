# 🚀 AI DDR Report Generator

An end-to-end AI-powered pipeline that converts raw inspection and thermal reports into a structured, client-ready DDR (Detailed Diagnostic Report).

---

## 📌 Overview

This project automates the process of analyzing technical inspection documents and generating a professional report using AI.

It performs:
- 📄 PDF text extraction
- 🖼️ Image extraction & handling
- 🤖 AI-based structured JSON generation
- 📝 Markdown & PDF report generation

---

## ⚙️ Features

- Automated inspection + thermal report analysis  
- Clean structured DDR JSON output  
- Professional report generation (Markdown + PDF)  
- Image extraction from PDFs  
- Fully modular pipeline (easy to extend)  

---

## 🧠 Tech Stack

- Python  
- PyMuPDF (PDF processing)  
- ReportLab (PDF generation)  
- OpenAI API (LLM processing)  
- Streamlit (for web UI - optional)  

---

## 📁 Project Structure

AI-DDR Report Generator/
│
├── main.py
├── extractor.py
├── llm.py
├── report_generator.py
│
├── data/
│ ├── inspection_report.pdf
│ └── thermal_report.pdf
│
├── prompts/
│ └── master_prompt.txt
│
├── config/
│ └── json_schema.json
│
├── images/
├── output/


---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-DDR-Report-Generator.git
cd AI-DDR-Report-Generator
2. Install Dependencies
pip install -r requirements.txt

If requirements.txt is missing:

pip install openai pymupdf reportlab streamlit
3. Set API Key
Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"
4. Run the Pipeline
python main.py \
--inspection "data/inspection_report.pdf" \
--thermal "data/thermal_report.pdf" \
--output-dir "./output"
📊 Output

Generated inside /output folder:

final_report.md → Human-readable report

final_report.pdf → Client-ready document

ddr_output.json → Structured AI output

🌐 Optional: Run as Web App
streamlit run app.py

Upload PDFs and generate reports directly from browser.

⚠️ Common Errors & Fixes
❌ ModuleNotFoundError
pip install <missing-module>
❌ API Key Error

Make sure:

echo $env:OPENAI_API_KEY
❌ PyMuPDF Error

Ensure compatibility fix is applied in extractor.py

🔐 Security Note

Never expose your API key publicly.
Use environment variables or .env file.

🧠 How It Works

Extract text + images from PDFs

Combine and structure data

Send to LLM with schema + prompt

Generate structured DDR JSON

Convert into readable report

💡 Future Improvements

Web dashboard with analytics

Multi-report comparison

API version for SaaS

Better UI/UX

🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first.

📬 Contact

For collaboration or queries, reach out via GitHub.

⭐ If you like this project

Give it a star ⭐ and share it!


---

# 🔥 BONUS (HIGH IMPACT)

README ke top me ye line add kar sakta hai:

```markdown
> ⚡ Built as an AI-powered automation system for real-world inspection report generation.
