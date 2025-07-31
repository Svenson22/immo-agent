import csv
import os

CSV_PATH = "Conversion_Postal_code_Refnis_code_va01012025.csv"

# Bouw mapping van gemeentenaam naar postcodes op basis van lokaal conversie-CSV-bestand
def build_mapping_from_csv():
    mapping = {}
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"❌ CSV-bestand '{CSV_PATH}' niet gevonden in de projectmap.")

    with open(CSV_PATH, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Maak een mapping van genormaliseerde kolomnamen naar originele kolomnamen
        column_map = {name.strip().lower(): name for name in reader.fieldnames}

        postal_key = column_map.get("postal code")
        gemeente_key = column_map.get("gemeentenaam")

        if not postal_key or not gemeente_key:
            raise KeyError("❌ Kon kolommen 'Postal code' of 'Gemeentenaam' niet vinden.")

        for row in reader:
            gemeente = row[gemeente_key].strip().lower()
            postcode = row[postal_key].strip()

            if gemeente not in mapping:
                mapping[gemeente] = []
            if postcode not in mapping[gemeente]:
                mapping[gemeente].append(postcode)

    return mapping

def gemeenten_naar_postcodes(gemeenten):
    mapping = build_mapping_from_csv()
    postcodes = []
    for g in gemeenten:
        key = g.strip().lower()
        if key in mapping:
            postcodes.extend(mapping[key])
        else:
            print(f"⚠️ Geen postcode gevonden voor gemeente: {g}")
    return postcodes

# Test
if __name__ == "__main__":
    test_gemeenten = ["Haaltert", "Erpe-Mere", "Merchtem", "Lennik"]
    print(gemeenten_naar_postcodes(test_gemeenten))