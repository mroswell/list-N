## EPA List of COVID-19 Disinfectants (List N)

### Installation
```
brew install datasette sqlite-utils
pip3 install datasette-publish-vercel 
  or 
datasette install datasette-publish-vercel
```
### Import data
```
cd Projects/Advocacy/list-N/list-N
sqlite-utils insert list-N.db listN list-N.csv --csv
    or
curl "https://cfpub.epa.gov/wizards/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType="

(was: 
curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert disinfectants.db listN - --pk ID
)
```
### Enable Full-Text Search
```
sqlite-utils enable-fts disinfectants.db listN 'Surface_type' 'Active_ingredient' 'Risk_level' 'Date_on_List_N'  'Company' 'Contact_time' 'Use_site' 'Product_name' 'Formulation_type' 'Follow_directions_for_this_virus' 'Why_on_List_N' 'EPA_reg_num' --create-triggers --tokenize=porter
```
### Update column order
```
sqlite-utils transform disinfectants.db listN \
--column-order EPA_reg_num \
--column-order Risk_level \
--column-order Active_ingredient \
--column-order Product_name \
--column-order Company \
--column-order Use_site \
--column-order Surface_type \
--column-order Contact_time \
--column-order Formulation_type \
--column-order Follow_directions_for_this_virus \
--column-order Date_on_List_N \
--column-order Why_on_List_N \
--column-order ID

```
### Publish locally
``` 
datasette disinfectants.db -m metadata.json --setting default_page_size 2000 --setting max_returned_rows 3000 --setting default_facet_size 35 --static static:static/  --template-dir templates/ --plugins-dir plugins -p 8001 -o
```
```
datasette disinfectants.db -m metadata.json \
--setting default_page_size 3000 \
--setting max_returned_rows 3000 \
--setting default_facet_size 35 -o \
--static static:static/ \
--template-dir templates/ \
--plugins-dir plugins
```

### Publish to Vercel

- https://github.com/simonw/datasette-publish-vercel/blob/master/README.md

Visit: https://vercel.com/download to get CLI tool.

Run: `vercel login` to login to Vercel, then you can do this:

```
datasette publish vercel disinfectants.db --project "list-n" --title "Disinfectants Used for Addressing COVID" --source "List N Tool COVID-19 Disinfectants" --source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" --install datasette-vega --static static:static/ --metadata metadata.json --setting default_page_size 3000 --setting max_returned_rows 3000 --setting default_facet_size 35 --template-dir templates --plugins-dir plugins
```
```
datasette publish vercel disinfectants.db \
--project "list-n" \
--title "Disinfectants Used for Addressing COVID" \
--source "List N Tool COVID-19 Disinfectants" \
--source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" \
--install datasette-vega \ 
--setting default_page_size 3000 \
--setting max_returned_rows 3000 \
--setting default_facet_size 35 \
--static static:static/ \
--template-dir templates/
--plugins-dir plugins/
--metadata metadata.json \
```

### Utilities and Miscellaneous
```
sqlite-utils tables disinfectants.db --counts --columns
sqlite-utils analyze-tables disinfectants.db listN
sqlite-utils disable-fts disinfectants.db listN
open /Applications/DB\ Browser\ for\ SQLite.app disinfectants.db
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
   [Risk_level] TEXT,
   [Date_on_List_N] TEXT,
   [Company] TEXT,
   [Contact_time] FLOAT,
   [Use_site] TEXT,
   [Product_name] TEXT,
   [Active_ingredient] TEXT,
   [Formulation_type] TEXT,
   [Follow_directions_for_this_virus] TEXT,
   [Why_on_List_N] TEXT,
   [ID] INTEGER PRIMARY KEY,
   [EPA_reg_num] TEXT
);

```

### Special URLs
- http://127.0.0.1:8001/-/actor
- http://127.0.0.1:8001/-/config
- http://127.0.0.1:8001/-/databases
- http://127.0.0.1:8001/-/messages
- http://127.0.0.1:8001/-/metadata
- http://127.0.0.1:8001/-/patterns
- http://127.0.0.1:8001/-/plugins
- http://127.0.0.1:8001/-/threads
- http://127.0.0.1:8001/-/versions

### Key documentation 
- https://docs.datasette.io/en/latest/json_api.html#special-table-arguments
- https://docs.datasette.io/en/latest/custom_templates.html
- https://docs.datasette.io/en/latest/performance.html
- http://datasette.readthedocs.io/en/latest/sql_queries.html
- http://datasette.readthedocs.io/en/latest/facets.html
- http://datasette.readthedocs.io/en/latest/full_text_search.html
- https://docs.datasette.io/en/latest/pages.html
