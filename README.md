# list-N
EPA List of COVID-19 Disinfectants 

Datasette Session Notes - https://docs.google.com/document/d/1f61st8AXtpXvjeHB3UlmUhSCG1Ddiwih9nr-nO8LTEY/edit

Margie's original notes - https://docs.google.com/document/d/1RHv_Twe7gzUMcfAeHZ-RlVQU-ZwshpEalZ4NmF9-ISk/edit
Simon's original notes - https://docs.google.com/document/d/1Ck4Gopt8ssumGUjH1TeqASvHpFAPBJpTpDE_bvf4bCI/edit

```
$ brew install datasette sqlite-utils

$ cd Projects/Advocacy/list-N/datasette-app/
$ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

$ datasette listN.db
```
