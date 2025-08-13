#!/usr/bin/env python3
from __future__ import annotations
import os, sys, json, compileall
from pathlib import Path

REPO = Path.cwd()

# ====== instellingen die we verwachten ======
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

    # 1) Basisstructuur
    section("Structuur")
    for d in EXPECTED_DIRS:
        p = REPO / d
        print(f"[{'ok' if p.exists() else 'MISS'}] {d}{' (dir)' if p.exists() else ''}")
        if not p.exists():
            problems.append(f"Map ontbreekt: {d}")
    for f in EXPECTED_FILES:
        p = REPO / f
        print(f"[{'ok' if p.exists() else 'MISS'}] {f}")
        if not p.exists():
            problems.append(f"Bestand ontbreekt: {f}")

    # 2) Docs/diagrams check
    section("Docs & diagrams")
    found_docs = []
    for hint in DOCS_HINTS:
        p = REPO / hint
        if p.exists():
            found_docs.append(hint)
    if found_docs:
        print("[ok] Gevonden:", ", ".join(found_docs))
    else:
        print("[warn] Geen diagram-hints gevonden (controleer je docs/diagrams/).")

    # 3) Credentials/tokens dubbel
    section("Credentials & tokens")
    hits = find_files(["credentials.json", "token.json", "token.pickle"])
    for name, paths in hits.items():
        if paths:
            print(f"[ok] {name}: {', '.join(paths)}")
    # waarschuwingen
    if len(hits["credentials.json"]) > 1:
        problems.append("Meerdere credentials.json gevonden → hou er één aan (bij voorkeur config/credentials.json).")
    if len(hits["token.json"]) > 1:
        problems.append("Meerdere token.json gevonden → opkuisen (hou config/token.json).")
    if len(hits["token.pickle"]) > 1:
        problems.append("Meerdere token.pickle gevonden → opkuisen (hou config/token.pickle).")

    # 4) Oude gmail-tests/mappen opsporen
    section("Oude Gmail-testbestanden")
    test_hits = []
    for root, dirs, files in os.walk(REPO):
        if any(skip in root for skip in ("/.venv", "/node_modules", "/.git")):
            continue
        for f in files:
            if f in ("test_gmail.py", "gmail_auth.py"):
                test_hits.append(rel(Path(root)/f))
    if test_hits:
        print("[info] Gevonden testbestanden:", ", ".join(test_hits))
        # dubbele paden markeren als je ingest nu leidend is
        if any("email_pipeline" in h for h in test_hits):
            print("[warn] Oude map 'email_pipeline' gevonden met Gmail-tests. Hou consistentie met ingest/ (ok, maar documenteer).")

    # 5) .gitignore sanity
    section(".gitignore")
    gi = read_gitignore()
    if not gi:
        print("[warn] .gitignore ontbreekt of leeg.")
        problems.append(".gitignore ontbreekt of bevat geen regels.")
    else:
        missing_rules = [r for r in GITIGNORE_SHOULD_CONTAIN if r not in gi]
        if missing_rules:
            print("[warn] Ontbrekende regels:", ", ".join(missing_rules))
            problems.append("Vul .gitignore aan met: " + ", ".join(missing_rules))
        else:
            print("[ok] Gevoelige paden worden genegeerd.")

    # 6) Python syntax/compile check
    section("Python syntaxis check")
    ok = compileall.compile_file(str(REPO/"run_ingest.py"), quiet=1)
    ok &= compileall.compile_dir(str(REPO/"ingest"), quiet=1)
    print("[ok] Syntax OK" if ok else "[warn] Syntax issues (bekijk output van compileall).")
    if not ok:
        problems.append("Syntaxfout in ingest/ of run_ingest.py")

    # 7) Ingest-config inspectie (zonder Gmail te raken)
    section("Ingest-config")
    try:
        from ingest.config import GMAIL_LABEL_NAME, CREDENTIALS_FILE, TOKEN_FILE, RAW_DIR, STATE_FILE, TIMEZONE
        print("Label:", GMAIL_LABEL_NAME)
        print("Creds pad:", CREDENTIALS_FILE, "bestaat=", CREDENTIALS_FILE.exists())
        print("Token pad:", TOKEN_FILE, "bestaat=", TOKEN_FILE.exists())
        print("Raw dir:", RAW_DIR, "bestaat=", RAW_DIR.exists())
        print("State file:", STATE_FILE, "bestaat=", STATE_FILE.exists())
        print("Timezone:", TIMEZONE)
        if not CREDENTIALS_FILE.exists():
            problems.append("config/credentials.json ontbreekt (nodig voor OAuth).")
    except Exception as e:
        print("[warn] Kon ingest.config niet importeren:", e)
        problems.append("ingest/config.py import faalt")

    # 8) Conclusie
    section("Resultaat")
    if not problems:
        print("✅ Alles ziet er gezond uit. Je kan runnen:  python run_ingest.py")
        sys.exit(0)
    else:
        print("⚠️  Aandachtspunten:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

if __name__ == "__main__":
    main()