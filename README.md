# Alternative YouTube Recommendation System

<p align="center"><img src="https://i.ibb.co/mTL0svz/You-Tube-logo.jpg" width="357" height="291"></p>

I don’t like YouTube recommendation system. The reason is that you lack the control over things you get recommended: if you watch just one video on politics, then your whole feed is filled with other stupid videos about politics. My program allows to choose playlist with videos you really like, and then the recommendations are built **ONLY** on this playlist. Thus you can precisely choose what kinds of videos to get recommended

For that purpose, I downloaded my own playlist with liked videos from YouTube and used official YouTube API to get information about videos (description, tags, etc.). Then, I used TF-IDF algorithm for selecting recommendations

# Algorithm

Recommendations are built with a help of relatedToVideoId search of YouTube API: this method returns up to 25 videos similar to a selected one. My program improves these recommendations by selecting among relatedToVideoId search results the most relevant videos considering your preference from the playlist using TF-IDF

I came up with a simple algorithm to create recommendations, here are the steps:

1. Randomly select one video from the playlist 
2. Get 3 liked videos that are the most similar to the randomly selected one using TF-IDF
3. Find 25 related videos using relatedToVideoId for each of the 3 videos selected in the step above
4. Iterate over selected 3 liked videos. For each of them, using TF-IDF, find among 25 videos from relatedToVideoId one video which is most similar to the selected one and add them to array
5. Remove duplicates from the array. As a result, we have 1-3 recommendations (on average 2.5) for each randomly selected video

Repeat the process above for as many videos as you want, depending on how many recommended videos at once you wish to receive (I chose n = 3, so I get 7-10 recommendations per time, on average). In general, the choice numbers above is quite arbitrary, but I find this combination the most convenient. 
After that, these videos are sent in one email with links which looks like that: 

<p align="center"><img src=https://i.ibb.co/4FkZRcw/Untitled.png"></p>

# Data Collection and Processing 
TF-IDF algorithm finds most similar text documents among each other, so I had to convert videos into text, somehow. I used 5 features: Video Tittle, Channel Tittle, Video Description, Tags and Subtitles. 

To get subtitles, I used YouTubeTranscriptApi, while the other parameters I got from requests to the official YouTube API

Then, I concatenated everything into one big string and used TF-IDF algorithm to make recommendations. I had to transform API response into data frame with these strings two times: while converting videos from the playlist and while converting relatedToVideoId search results. As both transformations are identical, I created a separate class RequestTransformation in order to handle that

# References
- Official YouTube API: https://developers.google.com/youtube/v3
- YouTubeTranscriptApi for parsing video subtitles: https://github.com/jdepoix/youtube-transcript-api 
