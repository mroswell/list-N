import json
import sys

# $ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

toxic_ingredients = ['Ammonium bicarbonate', 'Ammonium carbonate', 'Chlorine dioxide', 'Glutaraldehyde', 'Glycolic acid', 'Hydrochloric acid', 'Hydrogen chloride', 'Hypochlorous acid', 'Iodine', 'Octanoic acid', 'Peroxyacetic acid (Peracetic acid)', 'Peroxyoctanoic acid', 'Phenolic', 'PHMB', 'Potassium peroxymonosulfate', 'Quaternary ammonium', 'Silver', 'Silver ion', 'Sodium chloride', 'Sodium chlorite', 'Sodium dichloroisocyanurate', 'Sodium dichloroisocyanurate dihydrate', 'Sodium hypochlorite', 'Triethylene glycol']


safer_ingredients = ['1,2-Hexanediol', 'Citric acid', 'Dodecylbenzenesulfonic Acid', 'Ethanol (Ethyl alcohol)', 'Hydrogen peroxide', 'Isopropanol (Isopropyl alcohol)', 'L-Lactic acid', 'Sodium carbonate', 'Sodium carbonate peroxyhydrate', 'Tetraacetyl ethylenediamine', 'Thymol']


def transform(d):
    # columns = d["COLUMNS"]
    columns = [
    "ID",
    "Registration number",
    "Active ingredients",
    "Product name",
    "Follow directions for this virus",
    "Contact time",
    "Company", 
    "Formulation type", 
    "Surface type",
    "Use site",
    "Why on List N",
    "Date on List N",
    "Company URL"
  ]

    data = d["DATA"]
    for row in data:
        d = dict(zip(columns, row))
        for s_ingredient in safer_ingredients:
            if s_ingredient in d["Active ingredients"]:
                 d["Safer or Toxic"] = 'Safer'
                 break
        for t_ingredient in toxic_ingredients:
            if t_ingredient in d["Active ingredients"]:
                d["Safer or Toxic"] = 'Toxic' 
                break
        d["Active ingredient"] = d["Active ingredients"].split("; ")   # Active Ingredient
        d["Formulation type"] = d["Formulation type"].split("; ") # Formulation Type
        d["Surface type"] = d["Surface type"].split("; ")   # Surface Type
        if d["Use site"] is not None:
            d["Use site"] = d["Use site"].split("; ")   # Use Site
        del d["Company URL"]
        yield d

if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(list(transform(data))))
