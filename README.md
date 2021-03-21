# list-N
EPA List of COVID-19 Disinfectants 


```
$ brew install sqlite-utils
$ brew install datasette

$ cd Projects/Advocacy/list-N/datasette-app/
$ curl 'https://cfpub.epa.gov/giwiz/disinfectants/includes/queries.cfc?method=getDisData&Keyword=&RegNum=&ActiveIng=All&ContactTime=&UseSite=&SurfType=' | python transform.py | jq . | sqlite-utils insert listN.db listN - --pk ID

$ datasette listN.db
```
