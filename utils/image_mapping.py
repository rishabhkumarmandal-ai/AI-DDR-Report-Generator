from typing import Dict, List


def map_images_to_observations(ddr_json: Dict, images: List[Dict]) -> Dict:
    """
    Attach image file references to observations that are missing them.
    Mapping is naive: assign images sequentially across observations.
    """
    obs = ddr_json.get("area_wise_observations", [])
    if not obs or not images:
        return ddr_json

    img_iter = iter(images)
    for item in obs:
        ref = item.get("image_reference")
        if not ref or ref == "Not Available":
            try:
                img = next(img_iter)
                item["image_reference"] = img.get("file", "Not Available")
            except StopIteration:
                break
    return ddr_json
