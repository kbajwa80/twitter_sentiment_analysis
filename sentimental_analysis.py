#/usr/bin/python
import tweepy
import pandas as pd
import plotly.plotly as py
import plotly
import plotly.graph_objs as go

from textblob import TextBlob
from datetime import datetime

targettwitterprofile = 'JustinTrudeau'
#targettwitterprofile = 'realDonaldTrump'
#query = 'realDonaldTrump'

#Plotly account credentials
plotly.tools.set_credentials_file(username='XXXX',api_key='XXXX')

#twitter credentials
consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXXY'
access_token_secret = 'XXXXX'

# attempt authentication 
try: 
	# create OAuthHandler object 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	# set access token and secret 
	auth.set_access_token(access_token, access_token_secret) 
	# create tweepy API object to fetch tweets 
	api = tweepy.API(auth) 
except: 
	print("Error: Authentication Failed") 

#Create Dataframe
df = pd.DataFrame({'Time': [], 'Polarity': []})

#Get tweets
for page in tweepy.Cursor(api.user_timeline, id=targettwitterprofile, count=200).pages(20):
#for page in tweepy.Cursor(api.search, q=query, count=200).pages(20):
    for tweet in page:
        tweetid = tweet.id
        tweetdate = datetime.strptime(str(tweet.created_at)[:10],'%Y-%m-%d').strftime('%d-%m-%Y')
        tweettext = tweet.text
        polarity = round(TextBlob(tweettext).sentiment.polarity,4)
	#append into Dataframe
	df = df.append({'Time':tweetdate,'Polarity':polarity},ignore_index=True)

#print df

data = [go.Scatter( x=df['Time'], y=df['Polarity'] )]
py.plot(data, filename='pandas-time-series')
