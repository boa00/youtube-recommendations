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








