from time import sleep
import requests
import json
import os
import time
from bs4 import BeautifulSoup

# proxy = 'http://154.17.76.189:21304'

# os.environ['http_proxy'] = proxy 
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

api_key = "AIzaSyCMQ1wL_1PEGF7KyQu4zJKx7XrrStBF-VI"
url     = "https://www.googleapis.com/youtube/v3/search" 


def channel_info_parser(data):
      # We parse the incoming data and get the required parts of code as a dictionary.
      
       channel_json = {
      #    "Bölge_Kodu"                 :data["regionCode"],
         "Type"                       :data["items"][0]["id"]["kind"],
         "Kanal_Oluşturulma_Tarihi"   :data["items"][0]["snippet"]["publishedAt"],
         "Kanal_ID"                   :data["items"][0]["snippet"]["channelId"],  
         "Kanal_Baslıgı"              :data["items"][0]["snippet"]["title"],
         "Kanal_Profil_Foto"          :data["items"][0]["snippet"]["thumbnails"]["high"]["url"],
         "Kanal_Acıklaması"           :data["items"][0]["snippet"]["description"]

       }
       return channel_json


def yt_channel_search(channelList):

      global api_key
      global url
      url = "https://www.youtube.com/c/codebasics/about"
      req = requests.get(url)
      soup = BeautifulSoup(req.text, "lxml")
      print(soup)
      time.sleep(9999)

      for channelName in channelList:
            channelName = channelName.split("/",-1) # The last item is channel name
            channelName = channelName[-1]
            
            parameters = {   
            "part": "snippet",
            "q": channelName,
            "key": api_key,
            "type": "channel",
            "maxResults": 10000,
            "order": "videoCount"}

            channel_resp = requests.get(url, params = parameters) 
            """We can send a request using "request" module and take the required data using
            parameters 
            """
            data               = json.loads(channel_resp.text)
            print(data)
            time.sleep(9999)
            channel_json       = channel_info_parser(data)
            final_channel_json = json.dumps(channel_json,ensure_ascii=False)
            print("\n\n\n\n\n",data,"\n\n\n\n\n")
            print(final_channel_json)
            # with open(channelName + ".json","w", encoding="UTF-8") as f:
            #       f.write(final_channel_json)
            #       print(f"{channelName}'s json is created")
            #       sleep(0.1)
    

yt_channel_search(['https://www.youtube.com/@codebasics'])
