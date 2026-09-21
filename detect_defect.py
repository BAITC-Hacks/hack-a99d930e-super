from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def is_red_pixel(red: int, green: int, blue: int) -> bool:
    return red > 150 and red > green * 1.4 and red > blue * 1.4


def classify_image(image_path: Path, threshold: float = 0.08) -> str:
    try:
        with Image.open(image_path) as image:
            rgb_image = image.convert("RGB")
            pixel_bytes = rgb_image.tobytes()
            total_pixels = rgb_image.width * rgb_image.height
            red_pixels = sum(
                1
                for index in range(0, len(pixel_bytes), 3)
                if is_red_pixel(pixel_bytes[index], pixel_bytes[index + 1], pixel_bytes[index + 2])
            )
    except UnidentifiedImageError:
        raise SystemExit(f"Not an image: {image_path}")

    red_ratio = red_pixels / total_pixels
    return "DEFECT" if red_ratio >= threshold else "OK"


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect a simple red-color defect in an image.")
    parser.add_argument("image", type=Path, help="Path to an image file")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.08,
        help="Minimum red pixel ratio for DEFECT, default: 0.08",
    )
    args = parser.parse_args()

    if not args.image.exists():
        raise SystemExit(f"File not found: {args.image}")

    print(classify_image(args.image, args.threshold))


if __name__ == "__main__":
    main()
