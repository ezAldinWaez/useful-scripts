"""
Bulk-compress images to a maximum dimension and file-size budget.

- Converts PNGs with transparency to RGB JPEGs (alpha removed).
- Preserves aspect ratio.
- Skips files that are already small enough.
- Offers a dry-run mode so you can see what would happen first.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def compress_image(
    src: Path,
    dst: Path,
    max_dim: int,
    max_bytes: int,
    quality: int,
) -> bool:
    """
    Compress *src* and write to *dst*.

    Returns True if the output file meets the size budget, False otherwise.
    """
    with Image.open(src) as img:
        # Strip alpha early to avoid “cannot write mode RGBA as JPEG”
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.thumbnail((max_dim, max_dim))

        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, "JPEG", quality=quality)

    if dst.stat().st_size > max_bytes:
        dst.unlink()  # Remove oversize file so users don't keep the mistake
        return False
    return True


def iter_images(folder: Path) -> list[Path]:
    return [
        p
        for ext in (".jpg", ".jpeg", ".png")
        for p in folder.glob(f"*{ext}")
        if p.is_file()
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resize & compress images into a given size budget.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input_dir",
        type=Path,
        help="Folder containing PNG/JPEG images.",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Destination folder for compressed images.",
    )
    parser.add_argument(
        "-d",
        "--max-dim",
        type=int,
        default=800,
        help="Maximum width/height (pixels).",
    )
    parser.add_argument(
        "-s",
        "--max-size",
        type=int,
        default=150,
        metavar="KB",
        help="Maximum file size (KB).",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=85,
        help="JPEG quality (1-95; Pillow default is 75).",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    in_dir: Path = args.input_dir
    out_dir: Path = args.output_dir

    max_bytes = args.max_size * 1024

    failures = []

    for img_path in iter_images(in_dir):
        relative = img_path.relative_to(in_dir)
        target = (out_dir / relative).with_suffix(".jpg")

        if args.dry_run:
            print(f"[DRY-RUN] Would process {img_path} → {target}")
            continue

        ok = compress_image(
            src=img_path,
            dst=target,
            max_dim=args.max_dim,
            max_bytes=max_bytes,
            quality=args.quality,
        )
        status = "✓" if ok else "✗ (too large, skipped)"
        print(f"{img_path.name}: {status}")

        if not ok:
            failures.append(img_path.name)

    if failures:
        print(
            f"\n{len(failures)} image(s) could not be squeezed under "
            f"{args.max_size} KB; consider lowering --quality or --max-dim.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("Done ✨")


if __name__ == "__main__":
    main()
