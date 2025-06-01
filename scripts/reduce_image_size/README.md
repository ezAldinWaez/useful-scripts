# Reduce Image Size

**Language:** `python`
**Author:** Ez Aldin Waez
**Last updated:** 2025-06-01

## Purpose

Quickly shrink a folder of JPEG/PNG images so each file is no larger than a chosen size budget (default 150 KB) while keeping aspect ratio intact. Ideal for prepping screenshots or blog assets before committing them to a repo.

## Features

-   Converts transparent PNGs to regular RGB JPEGs automatically.
-   Preserves aspect ratio (uses Pillow’s `thumbnail`).
-   Enforces a strict size budget – files that remain too large are discarded and reported.
-   Straight-forward CLI flags for max dimension, quality and a dry-run preview.

## Usage

```bash
python reduce_image_size.py INPUT_DIR OUTPUT_DIR [options]
```

### Key options

| Flag               | Default | Description                        |
| ------------------ | ------- | ---------------------------------- |
| `-d`, `--max-dim`  | 800     | Maximum width/height in pixels     |
| `-s`, `--max-size` | 150 KB  | File-size ceiling                  |
| `-q`, `--quality`  | 85      | JPEG quality (1–95)                |
| `-n`, `--dry-run`  | –       | List actions without writing files |

### Example

Shrink everything in `raw_photos/` into `compressed/`, limiting each image to 100 KB:

```bash
python reduce_image_size.py raw_photos compressed -s 100
```

Preview first, then actually write:

```bash
python reduce_image_size.py raw_photos compressed -n      # preview
python reduce_image_size.py raw_photos compressed         # execute
```

## Exit codes

-   `0` – All images compressed within budget
-   `1` – One or more images could not be squeezed small enough

## Dependencies

-   [Pillow](https://pypi.org/project/Pillow/) ≥ 10.0

Install with:

```bash
pip install pillow
```

## Changelog

| Date       | Notes                                                               |
| ---------- | ------------------------------------------------------------------- |
| 2025-06-01 | Initial refactor: argparse CLI, dry-run mode, better error handling |
