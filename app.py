import streamlit as st
import os

st.title("AI DDR Report Generator")

inspection = st.file_uploader("Upload Inspection Report", type="pdf")
thermal = st.file_uploader("Upload Thermal Report", type="pdf")

if st.button("Generate Report"):
    if inspection and thermal:
        with open("data/inspection_report.pdf", "wb") as f:
            f.write(inspection.read())

        with open("data/thermal_report.pdf", "wb") as f:
            f.write(thermal.read())

        os.system(
            'python main.py --inspection "data/inspection_report.pdf" '
            '--thermal "data/thermal_report.pdf" --output-dir "./output"'
        )

        st.success("Report Generated!")

        if os.path.exists("output/final_report.md"):
            with open("output/final_report.md") as f:
                st.download_button("Download Report", f.read(), "report.md")

    else:
        st.error("Upload both files!")