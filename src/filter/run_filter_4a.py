

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Dict, Any, Iterable
from src.common.io_utils import load_jsonl, write_jsonl, ensure_dir
from src.filter.rules_4a import compute_dedupe_key, has_minimal_fields, language_ok

def iter_split_files(in_dir: Path) -> Iterable[Path]:
    # verwacht bestanden als *.split.jsonl
    yield from sorted(in_dir.glob("*.split.jsonl"))

def process_file(in_path: Path, out_dir: Path, allowed_langs: list[str] | None) -> Dict[str, Any]:
    seen = set()
    kept = []
    stats = {
        "in_file": str(in_path),
        "records_read": 0,
        "dedup_skipped": 0,
        "invalid_skipped": 0,
        "lang_skipped": 0,
        "kept": 0,
        "out_file": ""
    }

    for rec in load_jsonl(in_path):
        stats["records_read"] += 1
        key = compute_dedupe_key(rec)
        if key in seen:
            stats["dedup_skipped"] += 1
            continue
        seen.add(key)

        if not has_minimal_fields(rec):
            stats["invalid_skipped"] += 1
            continue

        if not language_ok(rec, allowed_langs):
            stats["lang_skipped"] += 1
            continue

        kept.append(rec)

    out_path = out_dir / in_path.name.replace(".split.jsonl", ".filtered.jsonl")
    write_jsonl(out_path, kept)
    stats["kept"] = len(kept)
    stats["out_file"] = str(out_path)
    return stats

def main():
    ap = argparse.ArgumentParser(description="Step 4A: technische filter op gesplitste zoekertjes")
    ap.add_argument("--in-dir", default="data/staged/split", help="Directory met *.split.jsonl")
    ap.add_argument("--out-dir", default="data/staged/filtered", help="Directory voor *.filtered.jsonl")
    ap.add_argument("--allowed-langs", default="", help="Komma-gescheiden lijst (bv. 'nl,fr'). Leeg = geen taalfilter.")
    args = ap.parse_args()

    in_dir = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)

    allowed_langs = [s.strip() for s in args.allowed_langs.split(",") if s.strip()] or None

    files = list(iter_split_files(in_dir))
    if not files:
        print(f"[filter-4a] Geen inputbestanden gevonden in {in_dir} (verwacht *.split.jsonl)")
        return

    total = {
        "records_read": 0,
        "dedup_skipped": 0,
        "invalid_skipped": 0,
        "lang_skipped": 0,
        "kept": 0,
        "files": 0
    }

    for f in files:
        stats = process_file(f, out_dir, allowed_langs)
        total["records_read"] += stats["records_read"]
        total["dedup_skipped"] += stats["dedup_skipped"]
        total["invalid_skipped"] += stats["invalid_skipped"]
        total["lang_skipped"] += stats["lang_skipped"]
        total["kept"] += stats["kept"]
        total["files"] += 1
        print(f"[filter-4a] {stats['in_file']} → {stats['out_file']} | "
              f"read={stats['records_read']} kept={stats['kept']} "
              f"dedup={stats['dedup_skipped']} invalid={stats['invalid_skipped']} lang={stats['lang_skipped']}")

    print(f"[filter-4a] DONE | files={total['files']} | read={total['records_read']} | "
          f"kept={total['kept']} | dedup={total['dedup_skipped']} | invalid={total['invalid_skipped']} | lang={total['lang_skipped']}")

if __name__ == "__main__":
    main()