import json
import sys

def transform(d):
    columns = d["COLUMNS"]
    data = d["DATA"]
    for row in data:
        d = dict(zip(columns, row))
        d["ACTI_ING"] = d["ACTI_ING"].split("; ")   # Active Ingredient
        d["FORM_TYPE"] = d["FORM_TYPE"].split("; ") # Formulation Type
        d["USE_SURF"] = d["USE_SURF"].split("; ")   # Surface Type
        if d["USE_SITE"] is not None:
            d["USE_SITE"] = d["USE_SITE"].split("; ")   # Use Site
        yield d

if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(list(transform(data))))
