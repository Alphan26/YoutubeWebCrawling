from time import sleep
import requests
import json
from googleapiclient.discovery import build
import time
import pandas as pd
from youtube_statistic import YTstats
channel_id = ["UC3yVE_PQBF0jbqkdCVdUkUg"] # Enes Karagülle kanalı
API_KEY = "AIzaSyCMQ1wL_1PEGF7KyQu4zJKx7XrrStBF-VI"
yt = YTstats(API_KEY, channel_id[0])

a = yt.get_channel_video_data()
print(len(a.keys()))
# time.sleep(999)
listOfVideoIds = list(a.keys())
print(listOfVideoIds[0])
# time.sleep(999)


comments_path = r"C:\Users\363860.SIBER\Desktop\YoutTube\JsonFiles"

ytVideoList = ["https://www.youtube.com/watch?v=9UCyRyJyZAo"]
comment_dict = {}
reply_dict = {}
topLevelComments = []
comment_replies = []
comment_replies.append(['Parent Comment ID','Reply ID','Reply','Author Name','Author Image','Author Channel','Reply Like Count','Publish Date'])
topLevelComments.append(['Video ID','Comment','Like Count',' Comment Publish Date','Author Name','Author Image'])

def video_comments():

    global topLevelComments
    youtube = build(f'youtube', 'v3', developerKey=f"{API_KEY}")
    global comment_dict
    global reply_dict    
    a = [] # Bunu kaç tane video geliyo diye denemek için yazdım
    # for video_id in ytVideoList:
    #     video_id = video_id.split("=", -1)
    #     video_id = video_id[-1]
    try:
        ytVideoList = listOfVideoIds
        video_response = youtube.commentThreads().list(
                part=f'snippet,replies',
                videoId=f"{ytVideoList[0]}",
                # Buraya pageToken koyamazsın npt in daha belli değil 
            ).execute()
       
        npt = video_response['nextPageToken']
        
        # print(len(ytVideoList))
        # time.sleep(999)
        for video_id in ytVideoList:
            print(video_id)
            a.append(video_id)
            print(len(a))
            # retrieve youtube video results
            video_response = youtube.commentThreads().list(
                part=f'snippet,replies',
                videoId=f"{video_id}",
                pageToken = npt
                # Buraya pageToken koyamazsın npt in daha belli değil 
            ).execute()
            
            while ('nextPageToken' in video_response.keys()): # We traverse the response as long as there is a next page token
                for item in video_response['items']: # Get the comments in single token
                    print(item)
                    time.sleep(9999) 
                    videoID = item['snippet']['topLevelComment']['snippet']["videoId"]
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    commentId = item['id']
                    # print(commentId)
                    # time.sleep(9999)
                    likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
                    commentPublishDate = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    author_img = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
                    # print(author_name)

                    new_dict ={
                        'videoId' : videoID,
                        'comment' : comment,
                        'likeCount' : likeCount,
                        'commentPublishDate' : commentPublishDate,
                        'author_name' : author_name,
                        'author_img' : author_img
                    }
                    print("Added to dictionary")
                    topLevelComments.append([videoID,comment,likeCount,commentPublishDate,author_name,author_img])
                    comment_dict = {**comment_dict,**new_dict} # We add the new values coming from the item.
                    # print(comment_dict)

                    with open('comments/' + str({commentId}) + '_comments.json',"w",encoding="utf-8") as f:
                        json.dump(comment_dict,f,ensure_ascii = False)
                
                    # print("Comment",comment)
                    comment_parent_id = item['snippet']['topLevelComment']['id']
                
                    replycount = item['snippet']['totalReplyCount']
                    # print("Reply Count",replycount)
                
                    if replycount > 0:
                        video_reply = youtube.comments().list(
                        part = f"id,snippet",
                        maxResults = 100,
                        #pageToken = npt,
                        parentId = comment_parent_id,
                        textFormat = "plainText"
                        ).execute()
                        # print(video_reply)
                        # time.sleep(9999)
                        for rep in video_reply['items']:
                            # print(i)
                            # time.sleep(9999)
                            parent_comment_id = rep['snippet']['parentId']
                            reply_id = rep['id']
                            reply = rep['snippet']['textDisplay']
                            reply_author_name = rep['snippet']['authorDisplayName']
                            author_img_url = rep['snippet']['authorProfileImageUrl']
                            author_channel_id = rep['snippet']['authorChannelUrl']
                            reply_like_count = rep['snippet']['likeCount']
                            reply_publish_date = rep['snippet']['publishedAt']
                            
                            new_reply_dict = {
                                'parent_comment_id' : parent_comment_id,
                                'reply_id' : reply_id,
                                'reply' : reply,
                                'reply_author_name' : reply_author_name,
                                'author_img_url' : author_img_url,
                                'author_channel_id' : author_channel_id,
                                'reply_like_count' : reply_like_count,
                                'reply_publish_date' : reply_publish_date
                            }

                            print("Reply added")
                            comment_replies.append([parent_comment_id,reply_id,reply,reply_author_name,author_img_url,author_channel_id,reply_like_count,reply_publish_date])

                            reply_dict = {**reply_dict, **new_reply_dict}
                            # print(reply_dict)
                            with open('replies/' + str({commentId}) +'_reply.json',"w",encoding="utf-8") as f:
                                json.dump(reply_dict,f,ensure_ascii = False)
                            #time.sleep(9999)
                    npt = video_response['nextPageToken']
                
                # video_response = youtube.commentThreads().list(
                #     part=f'snippet,replies',
                #     videoId=f"{video_id}",
                #     maxResults=100,
                    
                # ).execute() # We update the video response object with adding a new next page token.
    except Exception as e:
        print(str(e))
        

def listToCsv(listToCsv,file_name): # We convert the list to csv such that we can use it for analysis part.
    # print(topLevelComments)
    # print(comment_replies)
    
    print(len(topLevelComments) + len(comment_replies))
    df = pd.DataFrame(listToCsv)
    df.to_csv(file_name , index=False, header=False)
    
# Call function
video_comments()
listToCsv(topLevelComments,'comments.csv')
listToCsv(comment_replies,'replies.csv')
    
# https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/
