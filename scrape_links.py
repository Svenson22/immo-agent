from playwright.sync_api import sync_playwright
from gemeente_to_postcode import gemeenten_naar_postcodes

# 👇 Manuele testzone
GEMEENTEN = [
    "Haaltert", "Erpe-Mere", "Denderleeuw", "Liedekerke",
    "Lennik", "Tessenderlo-Ham"
]

def genereer_url(postcodes):
    postcode_params = ",".join([f"BE-{pc}" for pc in postcodes])
    return f"https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&postalCodes={postcode_params}"

def scrape_links(vanaf_url):
    print(f"🔗 Scraping vanuit: {vanaf_url}")
    links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(vanaf_url, timeout=60000)

        try:
            page.wait_for_selector("a.card--result__body", timeout=10000)
        except:
            print("⚠️ Geen zoekertjes geladen na 10 seconden.")
            page.screenshot(path="screenshot.png", full_page=True)
            print("📸 Screenshot opgeslagen als 'screenshot.png'")
            browser.close()
            return []

        anchors = page.locator("a.card--result__body")
        count = anchors.count()
        print(f"🔍 Aantal zoekertjes gevonden in DOM: {count}")

        for i in range(count):
            href = anchors.nth(i).get_attribute("href")
            if href and href.startswith("/nl/"):
                full_url = f"https://www.immoweb.be{href}"
                links.append(full_url)

        browser.close()
    return links

if __name__ == "__main__":
    postcodes = gemeenten_naar_postcodes(GEMEENTEN)
    if not postcodes:
        print("⚠️ Geen postcodes gevonden. Stoppen.")
    else:
        url = genereer_url(postcodes)
        zoekertjes = scrape_links(url)

        if zoekertjes:
            print("\n📄 Gevonden zoekertjes:")
            for link in zoekertjes:
                print(link)
        else:
            print("Geen zoekertjes gevonden.")