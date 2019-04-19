from elasticsearch import Elasticsearch
import csv
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
countTeam = [[],[]]

with open('../../best-team.json') as json_file:
    teams = json.load(json_file)
    terms = []
    for team in teams:
        res = es.search(index="tweet",
                        scroll = '2m',
                        size = 1000,
                        body=
                        # search all 'lollapalooza'
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
        countTeam[0].append(team["tla"])
        countTeam[1].append(res['hits']['total'])

f = open('occurence_team.csv', 'w')
with f:
  writer = csv.writer(f)

  for row in countTeam:
    writer.writerow(row)

