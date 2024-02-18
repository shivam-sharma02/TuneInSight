import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .ML_model import knn, data
import pandas as pd

client_id = 'f3cd5e7636654e2d9fa96e37fa1ec6dc'
client_secret = 'acab96ca22a0406289372be2d825b182'
Depressed = False

def get_playlist_items(playlist_id):
    # Initialize Spotipy with your credentials
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Get the playlist tracks
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    
    # Spotify paginates the results, so we need to loop through until all tracks are retrieved
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def get_audio_features(tracks):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Get audio features for each track
    audio_features = []
    for track in tracks:
        track_id = track['track']['id']
        if track_id:
            features = sp.audio_features(track_id)
            if features:
                audio_features.append(features[0])
    
    return audio_features

# # Example usage:
# playlist_id = '41sfGuPPtIZHGPMyHN6y2G'
# playlist_items = get_playlist_items(playlist_id)
# audio_features = get_audio_features(playlist_items)

# testSet = []
# for features in audio_features:
#     # Extracting features in the specified order
#     l = [features['danceability'], features['acousticness'], features['energy'], features['instrumentalness'], features['liveness'], features['valence'], features['loudness'], features['speechiness'], features['tempo']]
#     # testSet = [[0.063819, 0.000009, 0.089448, 0.000012, 0.019381, 0.079786, -0.028829, 0.040249, 0.058942], [0.05518, 0.001079, 0.057774, 0, 0.031516, 0.05568, -0.025444, 0.018343, 0.047111], [0.066519, 0.070958, 0.018763, 0.07414, 0.021615, 0.010127, -0.062838, 0.029031, 0.065932], [0.081421, 0.001859, 0.07468, 0.006605, 0.051369, 0.127342, -0.031939, 0.027894, 0.062684], [0.038227, 0.000024, 0.091213, 0.000032, 0.050625, 0.025416, -0.013444, 0.127341, 0.067778], [0.056584, 0.001489, 0.085361, 0.000008, 0.032509, 0.111097, -0.024457, 0.033048, 0.041453], [0.065331, 0.075656, 0.02963, 0.000259, 0.028787, 0.035766, -0.04839, 0.023194, 0.051669], [0.070514, 0.000775, 0.084247, 0.089668, 0.084871, 0.031181, -0.02611, 0.083378, 0.06038], [0.036607, 0.093645, 0.01319, 0.09951, 0.021019, 0.015852, -0.096021, 0.031532, 0.051847], [0.083364, 0.049071, 0.023779, 0.000669, 0.035735, 0.046771, -0.037963, 0.036459, 0.056053], [0.080881, 0.006736, 0.064927, 0.00021, 0.018935, 0.122495, -0.058236, 0.028121, 0.060768], [0.017062, 0.096443, 0.008945, 0.011482, 0.018662, 0.005175, -0.080969, 0.030168, 0.033477], [0.063711, 0.027684, 0.076909, 0.000001, 0.02154, 0.083323, -0.0279, 0.033275, 0.052494], [0.059716, 0.086149, 0.022292, 0.103447, 0.023129, 0.021486, -0.086731, 0.023043, 0.060807], [0.065007, 0.009914, 0.086011, 0.00491, 0.059807, 0.0752, -0.007197, 0.067991, 0.047149], [0.070298, 0.019888, 0.046721, 0.070422, 0.019381, 0.073104, -0.048453, 0.024483, 0.06272], [0.022785, 0.090247, 0.001365, 0.102244, 0.084871, 0.008738, -0.102023, 0.034564, 0.080094], [0.061767, 0.000018, 0.091956, 0.000032, 0.029283, 0.052011, -0.00885, 0.050027, 0.050401], [0.034555, 0.063962, 0.023779, 0.094261, 0.027794, 0.025023, -0.079881, 0.03373, 0.054219], [0.047945, 0.044874, 0.046164, 0.078952, 0.020101, 0.032753, -0.055983, 0.029031, 0.046715]]
#     # print(l)
#     testSet += [l]
# # print(testSet)
# testSet_df = pd.DataFrame(testSet)  # Convert testSet to DataFrame
# result_list = []
# for i in range(20):
#     test = testSet_df.iloc[i]  # Select test instance from DataFrame
#     k = 10 # chosen k value
#     result, neigh = knn(data, test, k) 
#     print('\nPredicted class of the datapoint (5) =', result)
#     result_list += [result]
# print(result_list)

# if (result_list.count("Sad") >= int((0.55)*len(result_list))):
#     Depressed = True

# print("Depressed : ", Depressed)