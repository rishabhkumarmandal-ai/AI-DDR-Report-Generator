from pathlib import Path
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from utils.file_ops import dump_json_file


def _build_area_table(area_items: List[Dict]) -> str:
    rows = ["| Area | Observation | Thermal Insight | Image |", "| --- | --- | --- | --- |"]
    for item in area_items:
        rows.append(
            f"| {item.get('area','Not Available')} | {item.get('observation','Not Available')} | "
            f"{item.get('thermal_insight','Not Available')} | {item.get('image_reference','Not Available')} |"
        )
    return "\n".join(rows)


def build_markdown_report(ddr_json: Dict, markdown_path: Path) -> None:
    """Create a markdown report from DDR JSON."""
    lines = [
        "# Detailed Diagnostic Report",
        "",
        f"**Property Issue Summary:** {ddr_json.get('property_issue_summary','Not Available')}",
        "",
        "## Area-wise Observations",
        _build_area_table(ddr_json.get("area_wise_observations", [])),
        "",
        "## Probable Root Cause",
        ddr_json.get("probable_root_cause", "Not Available"),
        "",
        "## Severity Assessment",
        f"- Level: {ddr_json.get('severity_assessment', {}).get('level','Not Available')}",
        f"- Reason: {ddr_json.get('severity_assessment', {}).get('reason','Not Available')}",
        "",
        "## Recommended Actions",
    ]

    actions = ddr_json.get("recommended_actions", [])
    if actions:
        lines.extend([f"- {action}" for action in actions])
    else:
        lines.append("- Not Available")

    lines.extend(
        [
            "",
            "## Additional Notes",
            ddr_json.get("additional_notes", "Not Available"),
            "",
            "## Missing Information",
        ]
    )

    missing = ddr_json.get("missing_information", [])
    if missing:
        lines.extend([f"- {item}" for item in missing])
    else:
        lines.append("- None")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")


def _paragraph(text: str, style) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def build_pdf_report(ddr_json: Dict, pdf_path: Path, images_base: Optional[Path] = None) -> None:
    """Render a simple PDF version of the DDR using reportlab."""
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading1Bold", parent=styles["Heading1"], spaceAfter=12))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], spaceAfter=10, leading=14))

    story = [
        _paragraph("Detailed Diagnostic Report", styles["Heading1Bold"]),
        _paragraph(f"<b>Property Issue Summary:</b> {ddr_json.get('property_issue_summary','Not Available')}", styles["Body"]),
        Spacer(1, 12),
        _paragraph("Area-wise Observations", styles["Heading2"]),
    ]

    table_data = [["Area", "Observation", "Thermal Insight", "Image"]]
    for item in ddr_json.get("area_wise_observations", []):
        table_data.append(
            [
                item.get("area", "Not Available"),
                item.get("observation", "Not Available"),
                item.get("thermal_insight", "Not Available"),
                item.get("image_reference", "Not Available"),
            ]
        )

    table = Table(table_data, colWidths=[1.3 * inch, 2.2 * inch, 2.2 * inch, 1.6 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.extend([table, Spacer(1, 12)])

    story.append(_paragraph("Probable Root Cause", styles["Heading2"]))
    story.append(_paragraph(ddr_json.get("probable_root_cause", "Not Available"), styles["Body"]))

    story.append(_paragraph("Severity Assessment", styles["Heading2"]))
    sev = ddr_json.get("severity_assessment", {})
    story.append(_paragraph(f"Level: {sev.get('level','Not Available')}<br/>Reason: {sev.get('reason','Not Available')}", styles["Body"]))

    story.append(_paragraph("Recommended Actions", styles["Heading2"]))
    actions = ddr_json.get("recommended_actions", [])
    if actions:
        list_flow = ListFlowable([ListItem(_paragraph(a, styles["Body"])) for a in actions], bulletType="bullet")
        story.append(list_flow)
    else:
        story.append(_paragraph("Not Available", styles["Body"]))

    story.append(_paragraph("Additional Notes", styles["Heading2"]))
    story.append(_paragraph(ddr_json.get("additional_notes", "Not Available"), styles["Body"]))

    story.append(_paragraph("Missing Information", styles["Heading2"]))
    missing = ddr_json.get("missing_information", [])
    if missing:
        story.append(ListFlowable([ListItem(_paragraph(m, styles["Body"])) for m in missing], bulletType="bullet"))
    else:
        story.append(_paragraph("None", styles["Body"]))

    # Embed images that are referenced and exist
    story.append(Spacer(1, 16))
    story.append(_paragraph("Referenced Images", styles["Heading2"]))
    any_image = False
    for item in ddr_json.get("area_wise_observations", []):
        ref = item.get("image_reference")
        if not ref:
            continue
        img_path = Path(ref)
        if images_base and not img_path.is_absolute():
            img_path = images_base / img_path
        if img_path.exists():
            any_image = True
            story.append(_paragraph(f"{item.get('area','Area')} - {img_path.name}", styles["Body"]))
            story.append(Image(str(img_path), width=3 * inch, preserveAspectRatio=True, height=3 * inch))
            story.append(Spacer(1, 8))

    if not any_image:
        story.append(_paragraph("No image references available.", styles["Body"]))

    doc.build(story)


def save_ddr_json(ddr_json: Dict, output_path: Path) -> None:
    dump_json_file(output_path, ddr_json)
