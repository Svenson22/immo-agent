import re
import json
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime
from typing import Dict, Any, List
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode

PRICE_REGEX = re.compile(r"(€|\bEUR\b)\s?[\d\s\.\,]+", re.IGNORECASE)

def _clean_url(u: str) -> str:
    try:
        p = urlparse(u)
        # remove tracking parameters
        qs = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith(("utm_", "mc_", "trk", "fbclid"))]
        return urlunparse((p.scheme, p.netloc, p.path, p.params, urlencode(qs), ""))  # without fragment
    except Exception:
        return u

def parse_message(msg: Dict[str, Any]) -> Dict[str, Any]:
    headers = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
    subject = headers.get("subject", "").strip()
    from_ = headers.get("from", "").strip()
    date_raw = headers.get("date", "")
    dt = parsedate_to_datetime(date_raw) if date_raw else None
    internal_date = int(msg.get("internalDate", "0"))

    # Retrieve body (prefer HTML; fallback to text/plain)
    parts = []
    def walk(p):
        mime = p.get("mimeType", "")
        body = p.get("body", {})
        data = body.get("data")
        if mime.startswith("multipart/"):
            for sp in p.get("parts", []) or []:
                walk(sp)
        else:
            if data:
                # base64url decode
                import base64
                parts.append((mime, base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")))
    walk(msg["payload"])

    html = ""
    text = ""
    for mime, content in parts:
        if mime == "text/html" and not html:
            html = content
        elif mime == "text/plain" and not text:
            text = content

    # Text: if HTML available → convert to plain text
    main_text = text
    links: List[str] = []
    if html:
        soup = BeautifulSoup(html, "lxml")
        # collect links
        for a in soup.find_all("a", href=True):
            links.append(_clean_url(a["href"]))
        # remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()
        main_text = soup.get_text(separator=" ", strip=True)
    main_text = re.sub(r"\s{2,}", " ", main_text or "").strip()

    # Detect prices
    prices = PRICE_REGEX.findall(main_text)
    # PRICE_REGEX with findall returns tuple (symbol,). Get full matches via finditer:
    prices_full = []
    for m in re.finditer(PRICE_REGEX, main_text):
        prices_full.append(m.group(0))

    return {
        "message_id": msg.get("id"),
        "subject": subject,
        "from": from_,
        "date_header": date_raw,
        "internal_date": internal_date,
        "datetime_parsed_iso": dt.isoformat() if dt else None,
        "text": main_text,
        "links": list(dict.fromkeys(links)),   # unique in order
        "prices": prices_full,
        "size_estimate": msg.get("sizeEstimate"),
        "label_ids": msg.get("labelIds", []),
    }