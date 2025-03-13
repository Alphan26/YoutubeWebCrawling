import json
import requests
from tqdm import tqdm
#import googleapiclient.discovery
#import google_auth_oauthlib.flow
import time
import schedule
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

class YTstats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.channel_views = None
        self.video_data = None
        self.file_path  = 'subscriber_data.csv'
        self.viewcount_path = "viewcount_path.csv"

    def extract_all(self):
        self.get_channel_statistics()
        self.get_channel_video_data()

    def get_channel_statistics(self): # IT WORKS
        """Extract the channel statistics"""
        print('get channel statistics...')
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)
        
        json_url = requests.get(url)
        data = json.loads(json_url.text)  # We convert the json data to dictionary.
        #print(type(int(data['items'][0]['statistics']['viewCount'])))
        #print(int(data['items'][0]['statistics']['viewCount']))
        #time.sleep(999)
        try:
            data = int(data['items'][0]['statistics']['subscriberCount'])
            view_count = int(data['items'][0]['statistics']['viewCount'])
            print(data)
        except KeyError:
            print('Could not get channel statistics')
            data = {}

        self.channel_statistics = data
        self.channel_views = view_count
        pbar.update()
        pbar.close()
        return data,view_count
    
    def update_subscriber_data(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        subscribers = self.get_channel_statistics()[0]

        if subscribers is not None:
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path)
            else:
                df = pd.DataFrame(columns=['date', 'subscribers'])

            new_data = pd.DataFrame({'date': [today], 'subscribers': [subscribers]})
            
            # Aynı saat ve dakikada tekrar kaydetmeyi önlemek için
            if not any(df['date'].str.startswith(today[:16])):
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(self.file_path, index=False)
                print(f"{today} tarihli abone sayısı ({subscribers}) başarıyla kaydedildi.")
            else:
                print(f"{today} tarihli abone sayısı zaten mevcut.")

    def update_viewcount_data(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        viewCount = self.get_channel_statistics()[-1]

        if viewCount is not None:
            if os.path.exists(self.viewcount_path):
                df = pd.read_csv(self.viewcount_path)
            else:
                df = pd.DataFrame(columns=['date', 'View Count'])

            new_data = pd.DataFrame({'date': [today], 'View Count': [viewCount]})
            
            # Aynı saat ve dakikada tekrar kaydetmeyi önlemek için
            if not any(df['date'].str.startswith(today[:16])):
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(self.file_path, index=False)
                print(f"{today} tarihli abone sayısı ({viewCount}) başarıyla kaydedildi.")
            else:
                print(f"{today} tarihli abone sayısı zaten mevcut.")

    def plot_trend(self):
        df = pd.read_csv(self.file_path)
        if df.empty:
            print("Veri bulunamadı. Lütfen önce veri toplayın.")
            return

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')

        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['subscribers'], marker='o', color='blue', label='Abone Sayısı')

        # Trend çizgisi (Hareketli ortalama)
        df['trend'] = df['subscribers'].rolling(window=3).mean()
        plt.plot(df['date'], df['trend'], color='red', label='Trend (3 günlük ort.)')

        # Veri noktalarının üzerine değerleri yazdırma
        for x, y in zip(df['date'], df['subscribers']):
            plt.text(x, y, f'{y}', fontsize=8, ha='right')

        plt.title('Abone Sayısındaki Değişim (Trend Analizi)')
        plt.xlabel('Tarih')
        plt.ylabel('Abone Sayısı')
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()
        plt.show()


    def get_channel_video_data(self):
        "Extract all video information of the channel"
        print('get video data...')
        channel_videos, channel_playlists = self._get_channel_content(limit=5000)

        parts=["snippet", "statistics","contentDetails"] # We can't get topic details thats why I removed
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)

        self.video_data = channel_videos
        
        return channel_videos

    def _get_single_video_data(self, video_id, part):
        """
        Extract further information for a single video
        parts can be: 'snippet', 'statistics', 'contentDetails', 'topicDetails'
        """

        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        # Muhtemelen burdan bütün veriler gelmiyor o yüzden statistic kısmını göremiyorum.
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data

    def _get_channel_content(self, limit=None, check_all_pages=True):
        """
        Extract all videos and playlists, can check all available search pages
        channel_videos = videoId: title, publishedAt
        channel_playlists = playlistId: title, publishedAt
        return channel_videos, channel_playlists
        """
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
        # Lets say we enter the youtube channel of enes batur.
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        vid, pl, npt = self._get_channel_content_per_page(url)
        idx = 0
        while(check_all_pages and npt is not None and idx < 10):
            # check all pages ın bi yararı yok gibi burda zaten bunu npt ile kontrol ediyosun
            nexturl = url + "&pageToken=" + npt
            next_vid, next_pl, npt = self._get_channel_content_per_page(nexturl)
            vid.update(next_vid)
            pl.update(next_pl)
            idx += 1

        return vid, pl

    def _get_channel_content_per_page(self, url):
        """
        Extract all videos and playlists per page
        return channel_videos, channel_playlists, nextPageToken
        """
        
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        #print(data)
        channel_videos = dict()
        channel_playlists = dict()
        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, channel_videos, None #Niye iki kere yazılmış

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
      
        # request.get diyince bütün bilgiler gelmeli onu bekliyorum.
      
        for item in item_data:
            try:
                kind = item['id']['kind']
                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = {'publishedAt': published_at, 'title': title}
                elif kind == 'youtube#playlist':
                    playlist_id = item['id']['playlistId']
                    channel_playlists[playlist_id] = {'publishedAt': published_at, 'title': title}
            except KeyError as e:
                print('Error! Could not extract data from item:\n', item)
            # like count dislike count vs bunları da eklesem aslında daha iyi olabilir.
        return channel_videos, channel_playlists, nextPageToken

    def dump(self):
        """Dumps channel statistics and video data in a single json file"""
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,"video_data": self.video_data}}

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)
        
        print('file dumped to', filename)


from youtube_statistic import YTstats
import time
API_KEY = "AIzaSyDVl3Bg1s24JstT6hFN07kO5hJrzUVDo0k"
channel_id = ["UCE7DCT5ikgv55I_cxXN1gmA"] 
yt = YTstats(API_KEY, channel_id[0])

schedule.every(2).minutes.do(yt.update_viewcount_data)

while True:
    schedule.run_pending()
    time.sleep(1)  # CPU'yu zorlamamak için 1 saniye bekle

#yt.plot_trend()