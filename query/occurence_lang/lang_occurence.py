from elasticsearch import Elasticsearch
import csv
import json


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

with open('../../best-team.json') as json_file:
    teams = json.load(json_file)
    terms = []
    for team in teams:
        countlang = [[],[]]
        res = es.search(index="tweet",
                        scroll = '2m',
                        size = 1000,
                        body=
                        {
                            "query":{
                                "match" : {
                                    "text" : {
                                        "query": team["name"] + " " +team["tla"],
                                        "operator": "or"
                                    }
                                }
                            }
                        }
                      )
        countEn = 0
        countFr = 0
        countEs = 0
        countNl = 0
        countPt = 0
        countKo = 0

        for item in res['hits']['hits']:
            if item['_source']["user"]["lang"] == "en" or item['_source']["user"]["lang"] == "en-gb":
                countEn += 1

            if item['_source']["user"]["lang"] == "fr":
                countFr += 1

            if item['_source']["user"]["lang"] == "es":
                countEs += 1

            if item['_source']["user"]["lang"] == "nl":
                countNl += 1

            if item['_source']["user"]["lang"] == "pt":
                countPt += 1


        countlang[0].append("Anglais")
        countlang[1].append(countEn)

        countlang[0].append("Francais")
        countlang[1].append(countFr)

        countlang[0].append("Espagnol")
        countlang[1].append(countEs)

        countlang[0].append("Netherlands")
        countlang[1].append(countNl)

        countlang[0].append("Portuguais")
        countlang[1].append(countPt)
        fichier = 'lang_'+team['tla']+'.csv'
        f = open(fichier, 'w')
        with f:
            writer = csv.writer(f)

            for row in countlang:
                writer.writerow(row)
