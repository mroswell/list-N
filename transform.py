# coding=utf-8
import json
import sys

# $ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

riskier_ingredients = ['Ammonium bicarbonate', 'Ammonium carbonate', 'Chlorine dioxide', 'Quaternary Ammonium Compounds', 'Glutaraldehyde', 'Glycolic acid', 'Hydrochloric acid', 'Hydrogen chloride', 'Hypochlorous acid', 'Iodine', 'o-Phenylphenol', 'Octanoic acid', 'Peroxyacetic acid (Peracetic acid)', 'Peroxyoctanoic acid', 'Phenolic', 'PHMB', 'Potassium peroxymonosulfate', 'Quaternary ammonium', 'Silver', 'Silver ion', 'Sodium chlorite', 'Sodium dichloroisocyanurate', 'Sodium dichloroisocyanurate dihydrate', 'Sodium hypochlorite', 'Triethylene glycol']
safer_ingredients = ['1,2-Hexanediol', 'Capric acid', 'Citric acid', 'Dodecylbenzenesulfonic acid', 'Ethanol', 'Ethanol (Ethyl alcohol)', 'Hydrogen peroxide', 'Isopropanol (Isopropyl alcohol)', 'L-Lactic acid', 'Sodium carbonate', 'Sodium carbonate peroxyhydrate', 'Tetraacetyl ethylenediamine', 'Thymol', 'Sodium chloride']

date_list = []

month_dict = {"January"   : "01",
              "February"  : "02",
              "March"     : "03",
              "April"     : "04",
              "May"       : "05",
              "June"      : "06",
              "July"      : "07",
              "August"    : "08",
              "September" : "09",
              "October"   : "10",
              "November"  : "11",
              "December"  : "12" }

def transform(d):
    # columns = d["COLUMNS"]
    columns = [
    "ID",
    "EPA_reg_num",
    "Active_ingredient",
    "Product_name",
    "Follow_directions_for_this_virus",
    "Contact_time",
    "Company", 
    "Formulation_type", 
    "Surface_type",
    "Use_site",
    "Why_on_List_N",
    "Date_on_List_N",
    "Company_URL"
  ]

    data = d["DATA"]
    for row in data:
        d = dict(zip(columns, row))
        for s_ingredient in safer_ingredients:
            if s_ingredient.casefold() in d["Active_ingredient"].casefold():
                 d["Risk_level"] = 'Safer'
                 break
        for t_ingredient in riskier_ingredients:
            if t_ingredient.casefold() in d["Active_ingredient"].casefold():
                d["Risk_level"] = 'Increased Risk'
                break
        d["Active_ingredient"] = d["Active_ingredient"].split("; ")
        for i in range(len(d["Active_ingredient"])):
            ing = d["Active_ingredient"][i].casefold()
            if ing == "o-phenylphenol":
                d["Active_ingredient"][i] = "o-Phenylphenol"
            elif ing == "l-lactic acid":
                d["Active_ingredient"][i] = "L-Lactic acid"
            elif ing == "phmb":
                d["Active_ingredient"][i] = "PHMB"
            elif ing == "quaternary ammonium compounds":
                d["Active_ingredient"][i] = "Quaternary ammonium"
            elif ing == "peroxyacetic acid (peracetic acid)":
                d["Active_ingredient"][i] = "Peroxyacetic acid (Peracetic acid)"
            elif ing == "isopropanol (isopropyl alcohol)":
                d["Active_ingredient"][i] = "Isopropanol (Isopropyl alcohol)"
            elif ing in ["ethanol (ethyl alcohol)","ethanol"]:
                d["Active_ingredient"][i] = "Ethanol (Ethyl alcohol)"
            else:
                d["Active_ingredient"][i] = d["Active_ingredient"][i].title()
        if d["Formulation_type"] is not None:
            d["Formulation_type"] = d["Formulation_type"].replace(u'®', "").replace(" (Clorox Total 360 system)", "").replace(" (use in conjunction with VHP generator)", "").replace(" CURIS", "").replace(" HaloFogger", "").split("; ")
        d["Surface_type"] = d["Surface_type"].split("; ")
        if d["Use_site"] is not None:
            d["Use_site"] = d["Use_site"].strip().split("; ")
        if d["Date_on_List_N"] is not None:
            date_list = d["Date_on_List_N"].split()
            d["Date_on_List_N"]='{year}-{mon}-{day}'.format(mon=month_dict[date_list[0].split(",")[0]],day=date_list[1],year=date_list[2])
      
        del d["Company_URL"]

        yield d

if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(list(transform(data))))
