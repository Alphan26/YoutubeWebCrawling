from time import sleep
import requests
import json
from googleapiclient.discovery import build
import time

comments_path = r"C:\Users\363860.SIBER\Desktop\YoutTube\JsonFiles\comments"
API_KEY = "AIzaSyCMQ1wL_1PEGF7KyQu4zJKx7XrrStBF-VI "
ytVideoList = ["https://www.youtube.com/watch?v=-0NwrcZOKhQ&t=645s"]
# "https://www.youtube.com/watch?v=4XVfmGE1F_w","https://www.youtube.com/watch?v=rkyUubl4Wo0",


def comment_crawler():
    commentList= list()
    youtube = build(f'youtube', 'v3', developerKey=f"{API_KEY}")

    for video in ytVideoList:
        video_id = video.split("=", -1)
        video_id = video_id[1][0:-2]  # Get the last item

      
        

    # if video_response['nextPageToken'] is not None:
    #           video_response = youtube.commentThreads().list(
    #                 part = 'snippet,replies',
    #                 videoId = video_id
    #             ).execute()
    # else:
    #     break
        video_response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=f"{video_id}",
            maxResults=100
        ).execute()
        count = 0
       
        while (video_response['nextPageToken'] is not None):
            if(video_response['nextPageToken'] is None):
                print("You get all of the page tokens")
                break

            npt = video_response['nextPageToken']
            print(npt)
            print(count)
            count += 1
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=npt
            ).execute()

            json_item_count = 0
            for item in video_response['items']:
                json_item_count += 1
                print(json_item_count)
                videoId = item['snippet']['videoId']
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                commentList.append(comment)
                print(len(commentList))
        

    time.sleep(9999)

        # finalcomment = json.dumps(comment,ensure_ascii=False)
        # with open(comments_path+f"/{json_item_count}_Comment_of_{videoId}.json","w", encoding="utf-8") as f:
        #     f.write(finalcomment)
        #     print(f"{json_item_count}. comment's json is okey")


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
