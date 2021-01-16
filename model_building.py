import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from request_transformation import RequestTransformation
from find_similar_videos import get_related_video_ids

def get_cos_sim_matrix(df):
	tfidf = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf.fit_transform(df['Text'])
	cos_sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
	return cos_sim_matrix

def get_n_similar_videos(vidoe_id, df, n_of_recommendations):
	# get index of the video in the df
	index = df.index[df['Video_Id'] == vidoe_id].tolist()[0]

	# index of the similarity vector corresponding to the video is the same as in df 
	cos_sim_matrix = get_cos_sim_matrix(df)
	similarity_vector = cos_sim_matrix[index]

	similarity_vector[index] = -1 # otherwise the video itself would always be recommended 

	# select top n most related videos
	recommendations = np.argpartition(similarity_vector, -n_of_recommendations)[-n_of_recommendations:]
	return recommendations

def make_recommendations(video_id, df):
	# get 3 liked videos that are the most similar to the randomly selected one
	top_similar_liked = get_n_similar_videos(video_id, df, 3)

	# find 25 related videos of the randomly selected liked video and convert into df
	related_videos_ids = get_related_video_ids(video_id)
	rt = RequestTransformation(related_videos_ids)
	related_videos = rt.transform()

	# find most similar video to the each of 5 most similar liked videos among related videos
	recommendation_ids = list()
	for video_index in top_similar_liked:
		row = df.loc[[video_index]]
		new_df = pd.concat([row, related_videos], ignore_index=True)
		video_id = df['Video_Id'][video_index]
		similar = get_n_similar_videos(video_id, new_df, 1)
		recommendation_ids.append(int(similar)-1)
	recommendation_ids = list(set(recommendation_ids)) # remove dublicates
	recommendations = [[related_videos['Video_Id'][x], related_videos['Title'][x]] for x in recommendation_ids]
	#recommendations = ['https://www.youtube.com/watch?v={},{}'.format(related_videos['Video_Id'][x], related_videos['Title'][x]) for x in recommendation_ids]
	return recommendations

