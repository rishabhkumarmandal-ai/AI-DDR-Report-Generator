import argparse
from pathlib import Path

from extractor import extract_reports
from llm import generate_ddr_json
from report_generator import build_markdown_report, build_pdf_report, save_ddr_json
from utils.file_ops import ensure_dir
from utils.image_mapping import map_images_to_observations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI DDR Report Generator")
    parser.add_argument("--inspection", required=True, help="Path to inspection_report.pdf")
    parser.add_argument("--thermal", required=True, help="Path to thermal_report.pdf")
    parser.add_argument("--master-prompt", default="master_prompt.txt", help="Path to master prompt file")
    parser.add_argument("--schema", default="json_schema.json", help="Path to JSON schema file")
    parser.add_argument("--output-dir", default=".", help="Directory for generated outputs")
    parser.add_argument("--images-dir", default="images", help="Directory to store extracted images")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name")
    parser.add_argument("--final-md", default="final_report.md", help="Output markdown report file name")
    parser.add_argument("--final-pdf", default="final_report.pdf", help="Output PDF report file name")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    inspection_path = Path(args.inspection).expanduser().resolve()
    thermal_path = Path(args.thermal).expanduser().resolve()
    master_prompt_path = Path(args.master_prompt).expanduser().resolve()
    schema_path = Path(args.schema).expanduser().resolve()

    for path, label in [
        (inspection_path, "Inspection PDF"),
        (thermal_path, "Thermal PDF"),
        (master_prompt_path, "Master prompt"),
        (schema_path, "JSON schema"),
    ]:
        if not path.exists():
            raise FileNotFoundError(f"{label} not found at {path}")

    output_dir = ensure_dir(Path(args.output_dir).expanduser().resolve())
    images_dir = ensure_dir(output_dir / args.images_dir)

    # 1. Extract
    extracted = extract_reports(inspection_path, thermal_path, images_dir)

    # 2. LLM generate DDR JSON
    ddr_json = generate_ddr_json(master_prompt_path, schema_path, extracted, model=args.model)

    # 2b. Map extracted images to observations if image_reference is missing
    all_images = extracted["inspection"]["images"] + extracted["thermal"]["images"]
    ddr_json = map_images_to_observations(ddr_json, all_images)

    # 3. Persist JSON
    json_out = output_dir / "ddr_output.json"
    save_ddr_json(ddr_json, json_out)

    # 4. Build reports
    md_path = output_dir / args.final_md
    pdf_path = output_dir / args.final_pdf

    build_markdown_report(ddr_json, md_path)
    build_pdf_report(ddr_json, pdf_path, images_base=images_dir)

    print(f"DDR JSON saved to: {json_out}")
    print(f"Markdown report saved to: {md_path}")
    print(f"PDF report saved to: {pdf_path}")
    print(f"Images extracted to: {images_dir}")


if __name__ == "__main__":
    main()
