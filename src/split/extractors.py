from __future__ import annotations
from typing import Dict, Any, List
from urllib.parse import urlparse
import re
import datetime as dt

_ZIMMO_PATTERNS = (
    "/te-koop/",
    "/te-huur/",
    "/nieuwbouwproject/",
    "/appartement/",
    "/huis/",
    "/garage/",
    "/bouwgrond/",
)
_IMMOWEB_CLASSIFIED = "/zoekertje/"
_IMMOSCOOP_TRACK = "contact.immoscoop.be/ls/click"

def _norm_dt(iso: str | None) -> str | None:
    if not iso:
        return None
    try:
        return dt.datetime.fromisoformat(iso.replace("Z","+00:00")).isoformat()
    except Exception:
        return iso

def _looks_like_zimmo_listing(u: str) -> bool:
    if "zimmo.be" not in u:
        return False
    p = urlparse(u)
    path = p.path or ""
    if any(seg in path for seg in _ZIMMO_PATTERNS):
        return True
    # Also accept short code pages like /LCABC/
    return bool(re.search(r"/LC[A-Z0-9]+/?$", path))

def _looks_like_immoweb_listing(u: str) -> bool:
    return "immoweb.be" in u and _IMMOWEB_CLASSIFIED in u

def _looks_like_immoscoop_tracked(u: str) -> bool:
    return _IMMOSCOOP_TRACK in u

def extract_listing_candidates(mail: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Zet 1 e-mailrecord om naar 0..N 'listing candidates'.
    We filteren links per bron en geven altijd de herkomst mee.
    """
    out: List[Dict[str, Any]] = []
    links: List[str] = mail.get("links") or []
    src_from = (mail.get("from") or "").lower()
    message_id = mail.get("message_id")
    sent_iso = _norm_dt(mail.get("datetime_parsed_iso"))

    for url in links:
        url_l = url.lower()
        source = None
        kind = "link"

        if _looks_like_zimmo_listing(url_l):
            source = "zimmo"
        elif _looks_like_immoweb_listing(url_l):
            source = "immoweb"
        elif _looks_like_immoscoop_tracked(url_l):
            source = "immoscoop"
            kind = "tracked_link"

        if not source:
            continue

        out.append({
            "source": source,
            "message_id": message_id,
            "email_subject": mail.get("subject"),
            "email_from": mail.get("from"),
            "email_date_iso": sent_iso,
            "url": url,
            "candidate_kind": kind,
            "needs_resolve": True if source == "immoscoop" else False,
            "raw_prices": mail.get("prices") or None,
            "raw_text_len": len(mail.get("text") or ""),
        })

    return out