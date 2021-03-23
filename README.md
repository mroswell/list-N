# list-N
EPA List of COVID-19 Disinfectants 

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


```
$ brew install datasette sqlite-utils
$ cd Projects/Advocacy/list-N/datasette-app/
$ sqlite-utils insert list-N.db listN list-N.csv --csv
    or
$ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

$ datasette listN.db
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
datasette publish vercel listN1.db \
	--project listN \
	--title "Disinfectants Used for Addressing COVID" \
	--source "List N Tool: COVID-19 Disinfectants; Maryland Pesticide Network" \
	--source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" 
```
```
datasette publish vercel listN1.db --project listN --title "Disinfectants Used for Addressing COVID" --source "List N Tool: COVID-19 Disinfectants; Maryland Pesticide Network" --source_url "https://cfpub.epa.gov/giwiz/disinfectants/index.cfm" 
```

http://127.0.0.1:8001/-/patterns
