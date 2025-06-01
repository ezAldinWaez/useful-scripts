# Google Photos Tools

**Language:** `python`
**Author:** Ez Aldin Waez
**Last updated:** 2025-06-01

## Purpose

A pair of command-line utilities for **inventorying** and **downloading** your Google Photos library.  
Use **`inventory.py`** to create a JSON catalogue of every photo/video, then **`download.py`** to batch-download originals (or resized variants) based on that catalogue.

## Features

-   OAuth 2.0 authentication stored in a reusable token (no re-login each run).
-   Inventory builder captures filenames, creation dates, URLs, album details …
-   Resume-able downloader with progress tracking (`download_progress.json`).
-   Optional date-range filters and configurable batch sizes to avoid API limits.
-   Automatic folder structure `YYYY/MM/filename` and filename sanitisation.

## Usage

```bash
# Step 1 – build the inventory (one-off or whenever you need a fresh list)
python inventory.py --output google_photos_inventory.json

# Step 2 – download originals in manageable batches
python download.py --inventory google_photos_inventory.json --batch-size 200 --output-dir google_photos_downloads
```

### Key options

| Script         | Flag                          | Default                        | Description                                            |
| -------------- | ----------------------------- | ------------------------------ | ------------------------------------------------------ |
| `inventory.py` | `--page-size`                 | 100                            | Google Photos API page size (max 500)                  |
|                | `--delay`                     | 1 s                            | Delay between API requests                             |
|                | `--output`                    | `google_photos_inventory.json` | Destination for the JSON catalog                       |
| `download.py`  | `--batch-size`                | 200                            | Items to download this run                             |
|                | `--start-index`               | 0                              | Skip the first _n_ items (resume / chunking)           |
|                | `--output-dir`                | `google_photos_downloads`      | Where files are saved                                  |
|                | `--start-date` / `--end-date` | –                              | Limit downloads to a date range (YYYY-MM-DD)           |
|                | `--max-retries`               | 3                              | Network retries per file                               |
|                | `--retry-delay`               | 1 s                            | Delay between retries                                  |
|                | `--params`                    | `=d`                           | URL params (`=d` original, `=w2048-h2048` large, etc.) |

### Example

```bash
# Download only 2024 photos in 500-item chunks
python download.py --inventory google_photos_inventory.json \
                   --start-date 2024-01-01 --end-date 2024-12-31 \
                   --batch-size 500
```

## Exit codes

-   `0` – All requested items processed successfully
-   `1` – One or more downloads failed (see `download_progress.json`)

## Dependencies

-   `google-auth`
-   `google-auth-oauthlib`
-   `google-api-python-client`
-   `requests`

Install with:

```bash
pip install -r requirements.txt
```

## Changelog

| Date       | Notes                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------- |
| 2025-06-01 | Initial version – separated `inventory.py` and `download.py`, shared `auth.py`, argparse CLIs |

---

> **Tip**  
> Place your Google Cloud **`credentials.json`** in this folder before running the scripts.  
> The first run opens a browser window for sign-in; after that, credentials are cached in **`token.pickle`**.
