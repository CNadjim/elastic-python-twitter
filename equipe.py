import httplib
import json
import time


connection = httplib.HTTPConnection("api.football-data.org")
headers1 = {'X-Auth-Token': 'e6af0ec31e5449ec8e8da2a4c5186188'}
headers2 = {'X-Auth-Token': '27daafb5ac6742b4a7ab34b2ae44e12a'}
competitions = ["2015", "2002", "2014", "2019", "2021"]


def getNameAndPosition():
    name_and_position = []
    for competition in competitions:
        connection.request("GET", "/v2/competitions/"+competition+"/standings", None, headers1)
        response = connection.getresponse()
        jsonResponse = json.loads(response.read())
        print(jsonResponse)
        teams = jsonResponse["standings"][0]["table"]
        for team in teams:
            result = {"name": team["team"]["name"], "position": team["position"]}
            name_and_position.append(result)
        time.sleep(20)
    connection.close()
    return name_and_position


def getName():
    name = []
    for competition in competitions:
        connection.request("GET", "/v2/competitions/"+competition+"/teams", None, headers2)
        response = connection.getresponse()
        jsonResponse = json.loads(response.read())
        teams = jsonResponse["teams"]
        for team in teams:
            print("\n... wait another competition \n")
            time.sleep(10)
            x = {'name': team["shortName"], 'tla': team["tla"]}
            name.append(x)
            print ("fetched "+team["shortName"]+" "+team["tla"])

    connection.close()
    print name
    with open('team.json', 'w') as outfile:
        json.dump(name, outfile)
    return name

