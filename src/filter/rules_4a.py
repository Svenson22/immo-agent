

from __future__ import annotations
import re
import hashlib
from urllib.parse import urlparse, urlunparse
from typing import Dict, Any, Optional

# ---- URL-normalisatie --------------------------------------------------------

def _strip_tracking(query: str) -> str:
    if not query:
        return ""
    # verwijder de meest voorkomende trackingparams
    bad_params = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"}
    params = []
    for pair in query.split("&"):
        if not pair:
            continue
        k = pair.split("=", 1)[0]
        if k not in bad_params:
            params.append(pair)
    return "&".join(params)

def normalize_url(url: Optional[str]) -> Optional[str]:
    if not url or not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url.strip())
        # forceer lowercase host, verwijder fragment, strip tracking
        netloc = parsed.netloc.lower()
        query = _strip_tracking(parsed.query)
        # soms staan er dubbele slashes of trailing slashes
        path = re.sub(r"/{2,}", "/", parsed.path or "/").rstrip("/") or "/"
        norm = urlunparse((parsed.scheme.lower() or "https", netloc, path, "", query, ""))
        return norm
    except Exception:
        return url

# ---- Dedupe-key --------------------------------------------------------------

def compute_dedupe_key(rec: Dict[str, Any]) -> str:
    """
    Bepaal een stabiele sleutel om duplicates te detecteren.
    Voorkeur: normalized URL -> anders op basis van (title, price, location).
    """
    url = normalize_url(rec.get("url") or rec.get("link"))
    if url:
        return f"url::{url}"
    title = (rec.get("title") or "").strip().lower()
    price = str(rec.get("price") or rec.get("prijs") or "").strip().lower()
    loc = (rec.get("location") or rec.get("locatie") or "").strip().lower()
    base = "|".join([title, price, loc])
    return "sig::" + hashlib.sha1(base.encode("utf-8")).hexdigest()

# ---- Minimale kwaliteitscontrole --------------------------------------------

def has_minimal_fields(rec: Dict[str, Any]) -> bool:
    """
    Technische uitsluiting:
    - Heeft (link/url)
    - Heeft prijs (mag straks verfijnd worden)
    """
    url = rec.get("url") or rec.get("link")
    if not url:
        return False

    # prijs: accepteer int/float of parseerbare string. 0 is toegestaan (soms 'prijs op aanvraag').
    price = rec.get("price") or rec.get("prijs")
    if price is None or (isinstance(price, str) and not price.strip()):
        return False

    return True

# ---- (Optioneel) taalcontrole ------------------------------------------------
# NB: default laten we alles door; indien gewenst kan je allowed_langs=['nl','fr'] activeren
try:
    from langdetect import detect
except Exception:
    detect = None

def detect_lang(text: str) -> Optional[str]:
    if detect is None:
        return None
    try:
        return detect(text)
    except Exception:
        return None

def language_ok(rec: Dict[str, Any], allowed_langs: Optional[list[str]]) -> bool:
    if not allowed_langs:
        return True
    title = (rec.get("title") or rec.get("titel") or "")
    desc = (rec.get("description") or rec.get("beschrijving") or "")
    sample = " ".join([title, desc]).strip()
    if not sample:
        return True  # niet blokkeren bij gebrek aan tekst
    lang = detect_lang(sample)
    if not lang:
        return True  # niet blokkeren als we niet kunnen detecteren
    return lang in set(allowed_langs)