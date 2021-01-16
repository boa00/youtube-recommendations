import pandas as pd
import requests 
import re
import secrets
from youtube_transcript_api import YouTubeTranscriptApi

class RequestTransformation:
    
    columns_to_include = ['Title',
                          'Video_Id',
                          'Channel_Title',
                          'Description',
                          'Tags',
                          ]
    URL = "https://www.googleapis.com/youtube/v3/videos"
    API_key = secrets.API_key
    
    def __init__(self, ids):
        self.ids = ids
        self.data = None
    
    # to store here data later
    def construct_dict(self, columns_to_include):
        data_dictionary = dict()
        for item in columns_to_include:
            data_dictionary[item] = list()
        return data_dictionary
    
    def get_request(self, vidoe_ids):
        video_ids = ",".join(vidoe_ids)
        parameters = {
            "key": self.API_key,
            "id": video_ids,
            "part": "snippet", 
            }
        r = requests.get(self.URL, parameters)
        return r.json()
    
    def retrieve_id_data(self, video_ids, data):
        n = len(video_ids)
        for i in range(0, n+1, 50): # max 50 at a time 
            if n < 50:
                ids = video_ids
            else:
                ids = video_ids[i:i+50]
            request_result = self.get_request(ids)
            # add request data to the dictionary passed as data parameter
            self.extract_request_data(request_result, data)
        return data
    
    def extract_request_data(self, request_result, data):
        for item in request_result['items']:
            # sometimes there are no tags
            if 'tags' in item['snippet'].keys():
                data['Tags'].append(', '.join(item['snippet']['tags']))
            else:
                data['Tags'].append('') 
            data['Title'].append(item['snippet']['title'])
            data['Video_Id'].append(item['id'])
            data['Channel_Title'].append(item['snippet']['channelTitle'])
            data['Description'].append(item['snippet']['description'])               
        
    def get_captions(self, video_ids):
        video_transcripts = list()
        for vidoe_id in video_ids:
            transcript = ''
            try:
                transcript = YouTubeTranscriptApi.get_transcript(vidoe_id)
            except:
                video_transcripts.append(transcript)  
                continue
            lines = list()
            for phrase in transcript:
                lines.append(phrase['text'])
            video_text = ' '.join(lines)
            video_transcripts.append(video_text)
        return video_transcripts

    def transform(self):
        # prepare dictionary for each column for the future df
        columns = self.construct_dict(self.columns_to_include)
        
        # add data from requests by ids to the dictionary created above
        self.data = self.retrieve_id_data(self.ids, columns)
        df = pd.DataFrame(self.data)
        
        # add captions 
        video_ids = list(df['Video_Id'])
        df['Captions'] = self.get_captions(video_ids)

        # concateneate all important string information into one string
        df['Text'] = df['Title'] + df['Channel_Title'] + df['Description'] + df['Tags'] + df['Captions']
        
        # remove symbols from the text
        df['Text'] = df['Text'].apply(lambda x: re.sub(r'[^\w]', ' ', x)) # remove symbols from text
        
        # drop unnecessary columns
        df.drop(['Channel_Title', 'Description', 'Tags', 'Captions'], axis=1, inplace=True)
        
        return df
        
        

        
        
        
        
        
        
        