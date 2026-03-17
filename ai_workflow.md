AI Workflow 
Step 1: Input 
User uploads: 
• Inspection PDF 
• Thermal PDF 
Step 2: Extract Data 
• Extract text 
• Extract images with coordinates 
Step 3: Structure Data 
Convert into: 
{ 
"area": "", 
"observation": "", 
"temperature": "", 
"image_ref": "" 
} 
Step 4: Merge Data 
• Match areas across both reports 
• Combine insights 
Step 5: LLM Processing 
Tasks: 
• Remove duplicates 
• Detect conflicts 
• Identify missing info 
• Generate structured output 
Step 6: Report Generation 
Convert output JSON → Human-readable DDR 
Step 7: Output 
• Final DDR report with images 
 