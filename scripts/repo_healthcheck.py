#!/usr/bin/env python3
from __future__ import annotations
import os, sys, json, compileall
from pathlib import Path

REPO = Path.cwd()

# ====== expected settings ======
EXPECTED_DIRS = [
    "ingest", "config", "data", "data/raw", "logs", "docs",
]
EXPECTED_FILES = [
    "run_ingest.py",
    "ingest/config.py",
    "ingest/gmail_client.py",
    "ingest/extract.py",
    "ingest/storage.py",
]
DOCS_HINTS = ["docs/diagrams", "immo_agent_process_flow_swimlanes.png"]
GITIGNORE_SHOULD_CONTAIN = [
    "config/token.json",
    "config/token.pickle",
    "data/raw/",
    "data/state.json",
    "logs/",
]

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except Exception:
        return str(p)

def find_files(names: list[str]) -> dict[str,list[str]]:
    hits = {n: [] for n in names}
    for root, dirs, files in os.walk(REPO):
        # skip venv/node_modules/.git
        if any(skip in root for skip in ("/.venv", "/node_modules", "/.git")):
            continue
        for f in files:
            if f in names:
                hits[f].append(rel(Path(root)/f))
    return hits

def read_gitignore() -> list[str]:
    gi = REPO / ".gitignore"
    if not gi.exists():
        return []
    return gi.read_text(encoding="utf-8", errors="ignore").splitlines()

def section(title: str):
    print(f"\n== {title} ==")

def main():
    problems = []

    # 1) Basic structure
    section("Structure")
    for d in EXPECTED_DIRS:
        p = REPO / d
        print(f"[{'ok' if p.exists() else 'MISS'}] {d}{' (dir)' if p.exists() else ''}")
        if not p.exists():
            problems.append(f"Missing directory: {d}")
    for f in EXPECTED_FILES:
        p = REPO / f
        print(f"[{'ok' if p.exists() else 'MISS'}] {f}")
        if not p.exists():
            problems.append(f"Missing file: {f}")

    # 2) Docs/diagrams check
    section("Docs & diagrams")
    found_docs = []
    for hint in DOCS_HINTS:
        p = REPO / hint
        if p.exists():
            found_docs.append(hint)
    if found_docs:
        print("[ok] Found:", ", ".join(found_docs))
    else:
        print("[warn] No diagram hints found (check your docs/diagrams/).")

    # 3) Duplicate credentials/tokens
    section("Credentials & tokens")
    hits = find_files(["credentials.json", "token.json", "token.pickle"])
    for name, paths in hits.items():
        if paths:
            print(f"[ok] {name}: {', '.join(paths)}")
    # warnings
    if len(hits["credentials.json"]) > 1:
        problems.append("Multiple credentials.json files found → keep only one (preferably config/credentials.json).")
    if len(hits["token.json"]) > 1:
        problems.append("Multiple token.json files found → clean up (keep config/token.json).")
    if len(hits["token.pickle"]) > 1:
        problems.append("Multiple token.pickle files found → clean up (keep config/token.pickle).")

    # 4) Detect old gmail test files/folders
    section("Old Gmail test files")
    test_hits = []
    for root, dirs, files in os.walk(REPO):
        if any(skip in root for skip in ("/.venv", "/node_modules", "/.git")):
            continue
        for f in files:
            if f in ("test_gmail.py", "gmail_auth.py"):
                test_hits.append(rel(Path(root)/f))
    if test_hits:
        print("[info] Found test files:", ", ".join(test_hits))
        # mark duplicate paths if ingest is now leading
        if any("email_pipeline" in h for h in test_hits):
            print("[warn] Old 'email_pipeline' folder found with Gmail tests. Keep consistency with ingest/ (ok, but document).")

    # 5) .gitignore sanity check
    section(".gitignore")
    gi = read_gitignore()
    if not gi:
        print("[warn] .gitignore missing or empty.")
        problems.append(".gitignore missing or contains no rules.")
    else:
        missing_rules = [r for r in GITIGNORE_SHOULD_CONTAIN if r not in gi]
        if missing_rules:
            print("[warn] Missing rules:", ", ".join(missing_rules))
            problems.append("Add to .gitignore: " + ", ".join(missing_rules))
        else:
            print("[ok] Sensitive paths are ignored.")

    # 6) Python syntax/compile check
    section("Python syntax check")
    ok = compileall.compile_file(str(REPO/"run_ingest.py"), quiet=1)
    ok &= compileall.compile_dir(str(REPO/"ingest"), quiet=1)
    print("[ok] Syntax OK" if ok else "[warn] Syntax issues (check compileall output).")
    if not ok:
        problems.append("Syntax error in ingest/ or run_ingest.py")

    # 7) Ingest-config inspection (without touching Gmail)
    section("Ingest-config")
    try:
        from ingest.config import GMAIL_LABEL_NAME, CREDENTIALS_FILE, TOKEN_FILE, RAW_DIR, STATE_FILE, TIMEZONE
        print("Label:", GMAIL_LABEL_NAME)
        print("Creds path:", CREDENTIALS_FILE, "exists=", CREDENTIALS_FILE.exists())
        print("Token path:", TOKEN_FILE, "exists=", TOKEN_FILE.exists())
        print("Raw dir:", RAW_DIR, "exists=", RAW_DIR.exists())
        print("State file:", STATE_FILE, "exists=", STATE_FILE.exists())
        print("Timezone:", TIMEZONE)
        if not CREDENTIALS_FILE.exists():
            problems.append("config/credentials.json missing (needed for OAuth).")
    except Exception as e:
        print("[warn] Could not import ingest.config:", e)
        problems.append("ingest/config.py import fails")

    # 8) Conclusion
    section("Result")
    if not problems:
        print("✅ Everything looks healthy. You can run:  python run_ingest.py")
        sys.exit(0)
    else:
        print("⚠️  Attention points:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

if __name__ == "__main__":
    main()