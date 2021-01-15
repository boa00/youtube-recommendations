import pandas as pd
from random import shuffle
from sending_email import send_email
from model_building import make_recommendations

# randomly select n liked videos and create recommendations based on them 
df = pd.read_csv('liked_videos_transformed.csv')
video_ids = list(df.sample(n=3)['Video_Id'])
print(video_ids)

recommendations = list()
for video_id in video_ids:
	recommendation = make_recommendations(video_id, df)
	recommendations += recommendation

# convert recommendations into a readable string
def recommendations_to_text(recommendations):
	shuffle(recommendations)
	i = 1
	strings = list()
	for recommendation in recommendations:
		URL = 'https://www.youtube.com/watch?v={}'.format(recommendation[0])
		title = recommendation[1]
		# sometimes titles are not in ASCII 
		string = f'\n{i}. {title}: {URL}'.encode('ascii').decode('ascii') 
		strings.append(string)
		i+= 1
	return ''.join(strings)

text = recommendations_to_text(recommendations) 

# send email
send_email(text)