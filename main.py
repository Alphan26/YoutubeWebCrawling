from youtube_statistic import YTstats
import time
API_KEY = "AIzaSyDVl3Bg1s24JstT6hFN07kO5hJrzUVDo0k"
channel_id = ["UCE7DCT5ikgv55I_cxXN1gmA"] 
#UCDdqJTIKWAaCbROLnKZZHZQ => atahan youtube channel
#"UCE7DCT5ikgv55I_cxXN1gmA" => deha 


yt = YTstats(API_KEY, channel_id[0])
#yt.get_channel_video_data()
yt.get_channel_statistics()
# print(type(yt.get_channel_video_data()))
# a = yt.get_channel_video_data()
# print("-----------------------")
# print(a.keys())
# print(len(a))
# yt.dump()  # dumps to .json
