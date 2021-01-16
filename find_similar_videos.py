import requests
import secrets

API_key = secrets.API_key
URL = 'https://www.googleapis.com/youtube/v3/search'

def get_relatedToVideoId_request(URL, API_key, video_id):
    parameters = {
        'key': API_key,
        'part': 'snippet',
        'relatedToVideoId': video_id,
        'type': 'video',
        'maxResults': 25,
        }
    r = requests.get(URL, parameters)
    return r.json()

# relatedToVideoId request lacks tags
# so I have to do another request through ids to retrieve them
def get_related_video_ids(video_id):
    related_ids = list()
    data = get_relatedToVideoId_request(URL, API_key, video_id)
    for item in data['items']:
        related_ids.append(item['id']['videoId'])
    return related_ids