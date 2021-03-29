## EPA List of COVID-19 Disinfectants (List N)


```
$ brew install datasette sqlite-utils
$ pip3 install datasette-publish-vercel
$ cd Projects/Advocacy/list-N/list-N
$ sqlite-utils insert list-N.db listN list-N.csv --csv
    or
$ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID
$ # sqlite-utils enable-fts listN.db listN 'Active_ingredients' 'Product_name' Company 'Formulation_type' 'Surface_type' 'Use_site' 'Why_on_List N' 'Safer_or_Toxic' 'Follow_directions_for_this_virus' 'Registration_number'

$ sqlite-utils enable-fts listN.db listN 'Surface_type' 'Active_ingredient' 'Safer_or_Toxic' 'Date_on_List_N'  'Company' 'Contact_time' 'Use_site' 'Product_name'  'Active_ingredients' 'Formulation_type' 'Follow_directions_for_this_virus' 'Why_on_List_N' 'Registration_number'

$ datasette listN.db -m metadata.json --setting default_page_size 210 -o 
$ datasette publish  vercel listN.db --project "list-n" --title "Disinfectants Used for Addressing COVID" --source "List N Tool COVID-19 Disinfectants" --source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" --install=datasette-vega
$ datasette publish vercel listN.db \
--project "list-n" \
--title "Disinfectants Used for Addressing COVID" \
--source "List N Tool COVID-19 Disinfectants" \
--source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" \
--install datasette-vega

$ sqlite-utils tables listN.db --counts --columns
```


Datasette Session Notes - https://docs.google.com/document/d/1f61st8AXtpXvjeHB3UlmUhSCG1Ddiwih9nr-nO8LTEY/edit

Margie's original notes - https://docs.google.com/document/d/1RHv_Twe7gzUMcfAeHZ-RlVQU-ZwshpEalZ4NmF9-ISk/edit
Simon's original notes - https://docs.google.com/document/d/1Ck4Gopt8ssumGUjH1TeqASvHpFAPBJpTpDE_bvf4bCI/edit



```
sqlite> .schema listN
CREATE TABLE [listN] (
   [EMER_PATH] TEXT,
   [REGI_NUM] TEXT,
   [INST_VIRUS] TEXT,
   [COMPANY] TEXT,
   [USE_SITE] TEXT,
   [CONT_TIME] FLOAT,
   [ACTI_ING] TEXT,
   [USE_SURF] TEXT,
   [COMPANY_URL] TEXT,
   [DATE_ON_LIST_N] TEXT,
   [FORM_TYPE] TEXT,
   [ID] INTEGER PRIMARY KEY,
   [PROD_NAME] TEXT
);
```
Now:
```
CREATE TABLE [listN] (
   [Surface_type] TEXT,
   [Active_ingredient] TEXT,
   [Safer_or_Toxic] TEXT,
   [Date_on_List_N] TEXT,
   [Company] TEXT,
   [Contact_time] FLOAT,
   [Use_site] TEXT,
   [Product_name] TEXT,
   [Active_ingredients] TEXT,
   [Formulation_type] TEXT,
   [Follow_directions_for_this_virus] TEXT,
   [Why_on_List_N] TEXT,
   [ID] INTEGER PRIMARY KEY,
   [Registration_number] TEXT
);


```





```
$ open /Applications/DB\ Browser\ for\ SQLite.app listN.db
```
#### Publish to Vercel
- https://github.com/simonw/datasette-publish-vercel/blob/master/README.md

$ `datasette install datasette-publish-vercel`

Visit: https://vercel.com/download to get CLI tool.

Run: `vercel login` to login to Vercel, then you can do this:

```
datasette publish vercel listN.db \
	--project listN \
	--title "Disinfectants Used for Addressing COVID" \
	--source "List N Tool: COVID-19 Disinfectants; Maryland Pesticide Network" \
	--source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" 
```
```
datasette publish vercel listN.db --project listN --title "Disinfectants Used for Addressing COVID" --source "List N Tool: COVID-19 Disinfectants; Maryland Pesticide Network" --source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" 
```
Special URLs
- http://127.0.0.1:8001/-/actor
- http://127.0.0.1:8001/-/config
- http://127.0.0.1:8001/-/databases
- http://127.0.0.1:8001/-/messages
- http://127.0.0.1:8001/-/metadata
- http://127.0.0.1:8001/-/patterns
- http://127.0.0.1:8001/-/plugins
- http://127.0.0.1:8001/-/threads
- http://127.0.0.1:8001/-/versions

Key documentation 
- https://docs.datasette.io/en/latest/json_api.html#special-table-arguments
- https://docs.datasette.io/en/latest/custom_templates.html
- https://docs.datasette.io/en/latest/performance.html
- http://datasette.readthedocs.io/en/latest/sql_queries.html
- http://datasette.readthedocs.io/en/latest/facets.html
- http://datasette.readthedocs.io/en/latest/full_text_search.html
- https://docs.datasette.io/en/latest/pages.html
