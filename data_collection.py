# =============================================================================
# import json
# import requests
# import pandas as pd
# import re
# 
# 
# history_file_name = "watch-history.json"
# categories_reference_file = "categories_reference.txt"
# API_key = "AIzaSyAqUh3e9DJUowl8FE62FmrgZKykHi0ihEE"
# URL_vidoe = "https://www.googleapis.com/youtube/v3/videos"
# categories_to_include = ['Title',
#                          'Video_Id',
#                          'Category_Id',
#                          'Channel_Title',
#                          'Description',
#                          'Tags',
#                          ]
# 
# #-------- Extracting Data --------
# 
# def get_video_ids(file_name):
#     with open(file_name, encoding="utf8") as f:
#         history = json.load(f)
#     ids = list()
#     for i in range(len(history)):
#         if "titleUrl" in history[i].keys():
#             ids.append(history[i]['titleUrl'][-11:])
#     return ids
# 
# def get_request(URL, API_key, video_ids):
#     video_ids = ",".join(video_ids)
#     parameters = {
#         "key": API_key,
#         "id": video_ids,
#         "part": "snippet,topicDetails,contentDetails", 
#         }
#     r = requests.get(URL, parameters)
#     return r.json()
# 
# def construct_dict(categories):
#     data_dictionary = dict()
#     for item in categories:
#         data_dictionary[item] = list()
#     return data_dictionary
#         
# def extract_categories(request_result, data):
#     for item in request_result['items']:
#         data['Title'].append(item['snippet']['title'])
#         data['Video_Id'].append(item['id'])
#         data['Category_Id'].append(item['snippet']['categoryId'])
#         data['Channel_Title'].append(item['snippet']['channelTitle'])
#         data['Description'].append(item['snippet']['description'])
#             
#         # sometimes there are no tags
#         if 'tags' in item['snippet'].keys():
#             data['Tags'].append(', '.join(item['snippet']['tags']))
#         else:
#             data['Tags'].append('')
#             
# def retrieve_id_data(ids, categories):
#     n = len(ids)
#     data = construct_dict(categories)
#     for i in range(50, n+1, 50): # max 50 at a time 
#         request_result = get_request(URL_vidoe, API_key, ids[i-50:i])
#         extract_categories(request_result, data)
#     return data
# 
# ids = get_video_ids(history_file_name)
# data = retrieve_id_data(ids, categories_to_include)
# df = pd.DataFrame(data)
# 
# #-------- Data Cleaning --------
# 
# # add vidoe categories instead of their ids 
# 
# def get_category_reference(file_name):
#     category_reference = dict()
#     category_reference_file = open(file_name, "r")
#     for category in category_reference_file:
#         pair = category.split()
#         category_reference[pair[0]] = pair[1]
#     return category_reference
# 
# category_reference = get_category_reference(categories_reference_file)
# df['Category'] = df['Category_Id'].apply(lambda x: category_reference[x])
# df.drop(['Category_Id'], axis=1, inplace=True)
# 
# # unite all text categories into one text  and drop no longer relevant columns
# 
# def unite(x):
#     return x['Title'] + x['Channel_Title'] + x['Description'] + x['Tags']
# 
# df['Text'] = df.apply(unite, axis=1)
# df['Text'] = df['Text'].apply(lambda x: re.sub(r'[^\w]', ' ', x)) # remove symbols from text
# print(df['Text'][1])
# 
# 
# df.drop(['Title', 'Channel_Title', 'Description', 'Tags'], axis=1, inplace=True)
# 
# 
# data_test = list()
# for i in range(10, 11, 10):
#     item = get_request(URL_vidoe, API_key, ids[i-10:i])
#     data_test.append(item)
#     
# df.to_csv("history.csv", index=False)
# 
# # 1) Choose categories of vidoe to recommend
# # 2) Upload hostiry data
# # 3) Sort in each category based on preferenced 
# # 4) Display only these categories
# =============================================================================

# =============================================================================
# import json
# from request_transformation import RequestTransformation
# 
# history_file_name = "watch-history.json"
# 
# # retrieve video ids from the history file
# def get_video_ids(file_name):
#     with open(file_name, encoding="utf8") as f:
#         history = json.load(f)
#     ids = list()
#     for i in range(len(history)):
#         if "titleUrl" in history[i].keys():
#             ids.append(history[i]['titleUrl'][-11:])
#     return ids
# 
# video_ids = get_video_ids("watch-history.json")[:150]
# rt = RequestTransformation(video_ids)
# data = rt.transform()
# 
# data.to_csv("history.csv", index=False)
# =============================================================================

import pandas as pd 
from request_transformation import RequestTransformation
from youtube_transcript_api import YouTubeTranscriptApi

df = pd.read_csv('Liked videos.csv')

# csv file is really weird so extracting like this to get ids
video_ids = list(df['Playlist ID'])[2:]

# there are spaces in some ids for whatever reasons, so delete it
video_ids = [x.strip() for x in video_ids]

# get the requests and transform it into df with necessary data
request = RequestTransformation(video_ids)
data = request.transform()

data.to_csv("liked_videos_transformed.csv", index=False)








