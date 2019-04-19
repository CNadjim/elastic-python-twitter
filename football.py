import tweepy
import sys
import json
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch

consumer_key = "IzoLF82wVRoCinEvJIH40hzpp"
consumer_secret = "kPBeCQHNRmoknVDKCKqnpD7HCRm9O9XGIdJ17eatHgigN3EFu9"
access_token = "1108762221805481984-GinqHeokvFNBoytVyfSsASPYQuZcD7"
access_token_secret = "Y5hAOjGyOMKBYERH1HXyLP7pgIKUsFMSyghTcQQqhatX2"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='tweet', ignore=400)


class StreamApi(tweepy.StreamListener):
  status_wrapper = TextWrapper(width=60, initial_indent='   ', subsequent_indent='    ')

  def on_status(self, status):
    json_data = status._json
    print "[ID] : ["+str(json_data['id'])+"] [tweet]: [" +json_data['text']+"] \n"
    es.index(index="tweet",
              doc_type="twitter",
              id=json_data['id'],
              body=json_data,
              ignore = 400
            )


streamer = tweepy.Stream(auth=auth, listener=StreamApi())

with open('best-team.json') as json_file:
    teams = json.load(json_file)
    terms = []
    for team in teams:
        terms.append("#"+team["tla"])
        terms.append(team["name"])

streamer.filter(None, terms)
