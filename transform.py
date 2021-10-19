# coding=utf-8
import json
import sys

# $ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

toxic_ingredients = ['Ammonium bicarbonate', 'Ammonium carbonate', 'Chlorine dioxide', 'Glutaraldehyde', 'Glycolic acid', 'Hydrochloric acid', 'Hydrogen chloride', 'Hypochlorous acid', 'Iodine', 'Octanoic acid', 'Peroxyacetic acid (Peracetic acid)', 'Peroxyoctanoic acid', 'Phenolic', 'PHMB', 'Potassium peroxymonosulfate', 'Quaternary ammonium', 'Silver', 'Silver ion', 'Sodium chloride', 'Sodium chlorite', 'Sodium dichloroisocyanurate', 'Sodium dichloroisocyanurate dihydrate', 'Sodium hypochlorite', 'Triethylene glycol']
safer_ingredients = ['1,2-Hexanediol', 'Citric acid', 'Dodecylbenzenesulfonic acid', 'Ethanol', 'Ethanol (Ethyl alcohol)', 'Hydrogen peroxide', 'Isopropanol (Isopropyl alcohol)', 'L-Lactic acid', 'Sodium carbonate', 'Sodium carbonate peroxyhydrate', 'Tetraacetyl ethylenediamine', 'Thymol']
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
            if s_ingredient in d["Active_ingredient"]:
                 d["Safer_or_Toxic"] = 'Safer'
                 break
        for t_ingredient in toxic_ingredients:
            if t_ingredient in d["Active_ingredient"]:
                d["Safer_or_Toxic"] = 'Toxic' 
                break
        d["Active_ingredient"] = d["Active_ingredient"].split("; ")
        if d["Formulation_type"] is not None:
            d["Formulation_type"] = d["Formulation_type"].replace(u'®', "").replace(" (Clorox Total 360 system)", "").replace(" (use in conjunction with VHP generator)", "").replace(" CURIS", "").replace(" HaloFogger", "").split("; ")
        d["Surface_type"] = d["Surface_type"].split("; ")
        if d["Use_site"] is not None:
            d["Use_site"] = d["Use_site"].split("; ")
        if d["Date_on_List_N"] is not None:
            date_list = d["Date_on_List_N"].split()
            d["Date_on_List_N"]='{year}-{mon}-{day}'.format(mon=month_dict[date_list[0].split(",")[0]],day=date_list[1],year=date_list[2])
      
        del d["Company_URL"]

        yield d

if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(list(transform(data))))
