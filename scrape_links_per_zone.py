import json
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.immoweb.be/nl/zoeken/huis/te-koop/"

# Laad zones en gemeenten vanuit extern JSON-bestand
def load_zones(json_path="zones.json"):
    with open(json_path, "r") as f:
        return json.load(f)

def get_listing_urls(search_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        try:
            page.wait_for_selector("a[data-testid='listing-card-link']", timeout=5000)
            links = page.query_selector_all("a[data-testid='listing-card-link']")
        except:
            print(f"Geen zoekresultaten gevonden voor {search_url}")
            browser.close()
            return []

        urls = []
        for link in links:
            href = link.get_attribute('href')
            if href:
                if href.startswith("/"):
                    href = "https://www.immoweb.be" + href
                urls.append(href)

        browser.close()
        return urls

if __name__ == "__main__":
    zones = load_zones()

    for zone_name, gemeenten in zones.items():
        print(f"\n### {zone_name} ###")
        for gemeente in gemeenten:
            search_url = BASE_URL + gemeente
            print(f"\nGemeente: {gemeente}")
            links = get_listing_urls(search_url)

            if links:
                for url in links:
                    print(" -", url)
            else:
                print("Geen zoekertjes gevonden.")