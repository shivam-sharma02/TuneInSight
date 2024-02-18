from django.shortcuts import render
from django.http import HttpResponse
import re  
from .trail import get_playlist_items, get_audio_features
from .ML_model import knn,data
import pandas as pd
from .models import UserPrediction

def extract_playlist_id(playlist):
    # Regular expression pattern to match the playlist ID in the Spotify link
    pattern = r'^https://open\.spotify\.com/playlist/([a-zA-Z0-9]+)'
    
    # Search for the pattern in the playlist link
    match = re.match(pattern, playlist)
    
    if match:
        # Extract the playlist ID from the matched group
        playlist_id = match.group(1)
        return playlist_id
    else:
        # Return None if the pattern is not found
        return None


def process_form(request):
    if request.method == 'POST':
        # Retrieve input values from the request object
        playlist = request.POST.get('link')
        email = request.POST.get('email')
        username = request.POST.get('Username')
        
        print("Playlist Link:", playlist)  # Add this debug statement

        # Extract playlist ID from the Spotify playlist link
        playlist_id = extract_playlist_id(playlist)
        
        if playlist_id:
            # Get playlist items and audio features
            playlist_items = get_playlist_items(playlist_id)
            audio_features = get_audio_features(playlist_items)
            
            # Prepare the test data
            testSet = []
            for features in audio_features:
                # Extracting features in the specified order
                l = [features['danceability'], features['acousticness'], features['energy'],
                     features['instrumentalness'], features['liveness'], features['valence'],
                     features['loudness'], features['speechiness'], features['tempo']]
                testSet += [l]
            testSet_df = pd.DataFrame(testSet)
            # Make predictions using the loaded model
            result_list = []
            for i in range(20):
               test = testSet_df.iloc[i]  # Select test instance from DataFrame
               k = 10 # chosen k value
               result, neigh = knn(data, test, k) 
#               print('\nPredicted class of the datapoint (5) =', result)
               result_list += [result]
            
            # Determine if the user is depressed based on the prediction results
            if (result_list.count("Sad") >= int((0.55)*len(result_list))):
                depressed = True
            else:
                depressed = False
            
            # Prepare data for rendering in template
            playlist_songs = [item['track']['name'] for item in playlist_items]
            sad_percentage = (result_list.count("Sad") / len(result_list)) * 100
            happy_percentage = (result_list.count("Happy") / len(result_list)) * 100
            energetic_percentage = (result_list.count("Energetic") / len(result_list)) * 100
            calm_percentage = (result_list.count("Calm") / len(result_list)) * 100
            
            
            # Render the template with the data
            user_prediction = UserPrediction.objects.create(
                username= username,
                email= email,
                playlist= playlist,
                playlist_songs= playlist_songs,
                sad_percentage= sad_percentage,
                happy_percentage= happy_percentage,
                energetic_percentage=energetic_percentage,
                calm_percentage=calm_percentage,
                depressed= depressed
            )
            context = {
                'username': username,
                'email': email,
                'playlist_link': playlist,
                'playlist_songs': playlist_songs,
                'sad_percentage': sad_percentage,
                'happy_percentage': happy_percentage,
                'energetic_percentage':energetic_percentage,
                'calm_percentage':calm_percentage,
                'depressed': depressed
            }
            return render(request, 'templates_result.html', context)
        else:
            # Return a response indicating invalid playlist link
            return HttpResponse('Invalid Spotify playlist link. Please provide a valid link.')
    else:
        # Handle GET request (e.g., render the form template)
        return render(request, 'index.html')

