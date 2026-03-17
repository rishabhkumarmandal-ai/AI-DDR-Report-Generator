AI DDR Report Generator – System Design 
Objective 
Build an AI system that converts raw inspection + thermal reports into a structured DDR 
report. 
Components 
1. Input Layer 
• Accepts PDF files: 
o Inspection Report 
o Thermal Report 
2. Extraction Layer 
• Extract: 
o Text content 
o Images 
• Tools: 
o PyMuPDF / pdfplumber 
3. Preprocessing Layer 
• Clean text 
• Remove duplicates 
• Chunk into sections: 
o Area 
o Observation 
o Temperature data 
4. Intelligence Layer (LLM) 
Tasks: 
• Merge inspection + thermal data 
• Detect conflicts 
• Identify missing data 
• Generate: 
o Root cause 
o Severity 
o Recommendations 
5. Report Generator 
Generate structured DDR: 
1. Summary 
2. Area-wise Observations 
3. Root Cause 
4. Severity 
5. Actions 
6. Notes 
7. Missing Info 
6. Output Layer 
• Format: 
o Markdown / HTML / PDF 
Key Features 
• No hallucination 
• Conflict detection 
• Image mapping 
• Generalizable system 
Scalability 
• Works on any inspection reports 
• Extendable to other domains