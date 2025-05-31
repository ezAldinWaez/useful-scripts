"""
Download media referenced in a JSON inventory.
Resumes automatically via download_progress.json.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path

import requests
from auth import get_service

PROGRESS_FILE = Path("download_progress.json")
PARAM_ORIG = "=d"


def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def parse_date(txt: str | None):
    if not txt:
        return None
    return dt.datetime.strptime(txt, "%Y-%m-%d").date()


def within_range(created: str, start, end) -> bool:
    d = parse_date(created.split("T")[0])
    if not d:
        return False
    if start and d < start:
        return False
    if end and d > end:
        return False
    return True


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def download(url: str, dest: Path, retries: int, delay: float) -> bool:
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, stream=True, timeout=60)
            r.raise_for_status()
            ensure_dir(dest.parent)
            with open(dest, "wb") as fh:
                for chunk in r.iter_content(8192):
                    fh.write(chunk)
            if dest.stat().st_size > 0:
                return True
            dest.unlink(missing_ok=True)
        except Exception as exc:
            print(f"Error ({attempt}/{retries}): {exc}")
            if attempt < retries:
                time.sleep(delay)
    return False


def get_fresh_url(item_id: str):
    svc = get_service()
    try:
        res = svc.mediaItems().get(mediaItemId=item_id).execute()
        return res.get("baseUrl")
    except Exception as exc:
        print(f"Cannot refresh URL for {item_id}: {exc}")
        return None


def run_download(
    inv_path: Path,
    out_dir: Path,
    batch: int,
    start: int,
    start_date,
    end_date,
    retries,
    delay,
    params,
):
    data = json.loads(inv_path.read_text())
    items = data["media_items"]

    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)
    if start_dt or end_dt:
        items = [
            it
            for it in items
            if within_range(it["creationTime"], start_dt, end_dt)
        ]

    # progress bookkeeping
    prog = (
        json.loads(PROGRESS_FILE.read_text())
        if PROGRESS_FILE.exists() and start == 0
        else {"last": start - 1, "done": 0, "failed": []}
    )

    end = min(len(items), prog["last"] + batch + 1)
    print(f"Processing items {prog['last']+1}‒{end-1} of {len(items)}")

    for idx in range(prog["last"] + 1, end):
        it = items[idx]
        fname = sanitize(it["filename"])
        date_part = it["creationTime"].split("T")[0]
        y, m, *_ = date_part.split("-")
        dest = out_dir / y / m / fname

        if dest.exists() and dest.stat().st_size > 0:
            prog["done"] += 1
            prog["last"] = idx
            continue

        url = (it.get("baseUrl") or "") + params
        if not url.startswith("http"):
            url = (get_fresh_url(it["id"]) or "") + params

        ok = download(url, dest, retries, delay)
        if ok:
            prog["done"] += 1
        else:
            prog["failed"].append({"id": it["id"], "filename": fname})
        prog["last"] = idx

        # update progress after each item
        PROGRESS_FILE.write_text(json.dumps(prog, indent=2))

    print(f"Downloaded {prog['done']} / {len(items)}")
    if prog["failed"]:
        print(f"Failed: {len(prog['failed'])} items – see {PROGRESS_FILE}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Download media from inventory JSON.")
    p.add_argument("--inventory", type=Path, default="google_photos_inventory.json")
    p.add_argument("--output-dir", type=Path, default="google_photos_downloads")
    p.add_argument("--batch-size", type=int, default=200)
    p.add_argument("--start-index", type=int, default=0)
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--max-retries", type=int, default=3)
    p.add_argument("--retry-delay", type=float, default=1)
    p.add_argument("--params", default=PARAM_ORIG)
    args = p.parse_args(argv)

    run_download(
        args.inventory,
        args.output_dir,
        args.batch_size,
        args.start_index,
        args.start_date,
        args.end_date,
        args.max_retries,
        args.retry_delay,
        args.params,
    )


if __name__ == "__main__":
    main()
