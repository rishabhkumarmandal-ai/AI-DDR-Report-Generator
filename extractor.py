from pathlib import Path
from typing import Dict, List, Tuple

import fitz  # PyMuPDF

from utils.file_ops import ensure_dir
from utils.text_processing import clean_text


def _extract_images(page: fitz.Page, images_dir: Path, prefix: str, page_index: int) -> List[Dict]:
    """
    Extract images from a page and save them to disk with stable filenames.
    - De-duplicates by xref to avoid saving the same embedded image multiple times.
    - Uses bbox mapping to keep approximate placement info when available.
    """
    images_meta: List[Dict] = []
    seen_xrefs = set()

    # Backward compatibility for PyMuPDF versions without get_image_bboxlist
    bbox_map = {}
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            bbox_map[xref] = page.get_image_bbox(img)
        except Exception:
            bbox_map[xref] = None

    for img_number, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)

        img_info = page.parent.extract_image(xref)
        ext = img_info.get("ext", "png")
        base_name = f"{prefix}_p{page_index + 1:02d}_img{xref}.{ext}"
        img_path = images_dir / base_name
        img_path.write_bytes(img_info["image"])

        rect = bbox_map.get(xref)
        bbox = None
        if rect:
            bbox = {
                "x0": rect.x0,
                "y0": rect.y0,
                "x1": rect.x1,
                "y1": rect.y1,
                "width": rect.width,
                "height": rect.height,
            }

        images_meta.append(
            {
                "file": str(img_path),
                "page": page_index + 1,
                "bbox": bbox,
                "xref": xref,
            }
        )

    return images_meta


def extract_pdf(pdf_path: Path, images_dir: Path, prefix: str) -> Tuple[str, List[Dict]]:
    """Extract text and images from a PDF."""
    doc = fitz.open(pdf_path)
    all_text = []
    all_images: List[Dict] = []

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        all_text.append(page.get_text("text"))
        all_images.extend(_extract_images(page, images_dir, prefix, page_index))

    doc.close()
    text = clean_text("\n".join(all_text))
    return text, all_images


def extract_reports(inspection_path: Path, thermal_path: Path, images_dir: Path) -> Dict:
    """Run extraction for both reports and return a structured payload."""
    ensure_dir(images_dir)
    inspection_text, inspection_images = extract_pdf(inspection_path, images_dir, "inspection")
    thermal_text, thermal_images = extract_pdf(thermal_path, images_dir, "thermal")

    return {
        "inspection": {"text": inspection_text, "images": inspection_images},
        "thermal": {"text": thermal_text, "images": thermal_images},
    }
