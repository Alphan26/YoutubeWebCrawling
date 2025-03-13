from time import sleep
import requests
import json
from googleapiclient.discovery import build
import time

comments_path = r"comments"
#API_KEY = "AIzaSyCMQ1wL_1PEGF7KyQu4zJKx7XrrStBF-VI "
ytVideoList = ["https://www.youtube.com/watch?v=-0NwrcZOKhQ&t=645s"]
# "https://www.youtube.com/watch?v=4XVfmGE1F_w","https://www.youtube.com/watch?v=rkyUubl4Wo0",


from time import sleep
import json
from googleapiclient.discovery import build
import re
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
ytVideoList = ["https://www.youtube.com/watch?v=-0NwrcZOKhQ"]

def get_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    if match:
        return match.group(1)
    return None

def comment_crawler():
    commentList = []
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    for video in ytVideoList:
        video_id = get_video_id(video)
        if not video_id:
            print(f"Invalid video URL: {video}")
            continue

        video_response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100
        ).execute()

        while 'nextPageToken' in video_response:
            for item in video_response['items']:
                # Ana yorumları al
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                commentList.append(comment)

                # Alt yorumları al
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_text = reply['snippet']['textDisplay']
                        commentList.append(reply_text)

            # Bir sonraki sayfayı getir
            next_page_token = video_response.get('nextPageToken')
            if not next_page_token:
                break

            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=next_page_token,
                maxResults=100
            ).execute()

        # Yorumları JSON dosyasına yazdır
        final_comments = json.dumps(commentList, ensure_ascii=False, indent=4)
        with open(f"{comments_path}\comments_{video_id}.json", "w", encoding="utf-8") as f:
            f.write(final_comments)

        print(f"Yorumlar {video_id}.json dosyasına kaydedildi.")

comment_crawler()



""""
ASLA SILME

 for comment in request2["items"]:
                AuthorID                = ["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                VideoID                 = ["snippet"]["topLevelComment"]["snippet"]["videoId"]
                CommentID               = ["id"]
                Message                 = ["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                AuthorChnURL            = ["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
                AuthorChnID             = ["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
                CreateDate              = ["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                UpdateDate              = ["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                LikeCount               = str(["snippet"]["topLevelComment"]["snippet"]["likeCount"])
                AuthorProfileImageURL   = ["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"]




"""
