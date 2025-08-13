from __future__ import annotations
import argparse, glob, os, sys, collections
from typing import List, Dict, Any, Iterable
from src.common.jsonl import read_jsonl, write_jsonl
from src.split.extractors import extract_listing_candidates

def process_file(in_path: str, out_dir: str) -> int:
    base = os.path.basename(in_path)
    out_path = os.path.join(out_dir, base.replace(".jsonl", ".split.jsonl"))
    counts = collections.Counter()
    rows_out: List[Dict[str, Any]] = []

    for mail in read_jsonl(in_path):
        cands = extract_listing_candidates(mail)
        rows_out.extend(cands)
        for c in cands:
            counts[c["source"]] += 1
        counts["emails_seen"] += 1

    n = write_jsonl(out_path, rows_out)
    print(f"[split-3a] {in_path} → {out_path} | emails={counts['emails_seen']} "
          f"| zimmo={counts['zimmo']} immoweb={counts['immoweb']} immoscoop={counts['immoscoop']} "
          f"| candidates_total={n}")
    return n

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Step 3a: split mails → listing candidates")
    ap.add_argument("--in", dest="inp", required=True, help="input file/glob, e.g. data/raw/2025-08-13.jsonl or 'data/raw/*.jsonl'")
    ap.add_argument("--out-dir", default="data/staged/split", help="output directory (default: data/staged/split)")
    args = ap.parse_args(argv)

    paths: List[str] = sorted(glob.glob(args.inp))
    if not paths:
        print(f"No input matched: {args.inp}", file=sys.stderr)
        return 1

    os.makedirs(args.out_dir, exist_ok=True)
    total = 0
    for p in paths:
        total += process_file(p, args.out_dir)

    print(f"[split-3a] DONE | total_candidates={total} | files={len(paths)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))