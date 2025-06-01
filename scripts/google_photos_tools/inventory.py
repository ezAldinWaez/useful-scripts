"""
Scan your Google Photos library, build a JSON inventory and save it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path

from auth import get_service

DEFAULT_OUTPUT = Path("google_photos_inventory.json")


def fetch_albums(svc, delay: float) -> dict[str, dict]:
    albums = {}
    page_token = None
    while True:
        res = (
            svc.albums()
            .list(pageSize=50, pageToken=page_token)
            .execute()
        )
        for alb in res.get("albums", []):
            albums[alb["id"]] = {
                "title": alb.get("title", "Untitled"),
                "itemCount": alb.get("mediaItemsCount", 0),
            }
        page_token = res.get("nextPageToken")
        if not page_token:
            break
        time.sleep(delay)
    return albums


def fetch_media_items(svc, page_size: int, delay: float) -> list[dict]:
    items, page_token = [], None
    while True:
        res = (
            svc.mediaItems()
            .list(pageSize=page_size, pageToken=page_token)
            .execute()
        )
        batch = res.get("mediaItems", [])
        if not batch:
            break
        items.extend(batch)
        page_token = res.get("nextPageToken")
        if not page_token:
            break
        time.sleep(delay)
    return items


def build_inventory(page_size: int, delay: float, output: Path):
    svc = get_service()
    print("Fetching albums …")
    albums = fetch_albums(svc, delay)
    print(f"Found {len(albums)} albums.")

    print("Fetching media …")
    raw_items = fetch_media_items(svc, page_size, delay)
    print(f"Retrieved {len(raw_items)} media items.")

    # retain only useful keys and add simple estimates
    clean = []
    for it in raw_items:
        meta = it.get("mediaMetadata", {})
        clean.append(
            {
                "id": it["id"],
                "filename": it["filename"],
                "mimeType": it["mimeType"],
                "creationTime": meta.get("creationTime", ""),
                "baseUrl": it.get("baseUrl", ""),
                "productUrl": it.get("productUrl", ""),
                "width": meta.get("width"),
                "height": meta.get("height"),
                "type": "video" if "video" in meta else "photo",
            }
        )

    out = {
        "scan_date": dt.datetime.now().isoformat(),
        "total_items": len(clean),
        "albums": albums,
        "media_items": clean,
    }
    output.write_text(json.dumps(out, indent=2))
    print(f"Inventory written to {output.resolve()}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Build Google Photos inventory JSON.")
    p.add_argument("--page-size", type=int, default=100, help="API page size (max 500).")
    p.add_argument("--delay", type=float, default=1.0, help="Seconds between calls.")
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = p.parse_args(argv)
    build_inventory(args.page_size, args.delay, args.output)


if __name__ == "__main__":
    main()
