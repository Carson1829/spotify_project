import pandas as pd
import pickle

tracks = pd.read_csv("cleaned_data_f.csv")
model = pickle.load(open('best_knn_model_mil.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

def get_tracks():
    # Adjust the file path to where your CSV file is located
    track_df = [{'track': track['track_name'], 'artist': track['artists']} for _, track in tracks.iterrows()]
    return track_df

# Function to search track names
def search_songs(query):
    track_df = get_tracks()
    matching_tracks = [track for track in track_df if query.lower() in track['track'].lower()]
    return matching_tracks

# Function to predict the genre of a song given its track and artist name
def get_track_info(track, artist):
    # Find the song in the dataset
    song = tracks[(tracks['track_name'] == track) & (tracks['artists'] == artist)]
    
    # Extract the features for the song
    features = song[['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 
                     'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
                     'time_signature']]

    features_scaled = scaler.transform(features)

    return features_scaled

# Function to predict top k genres
def predict_top_k(knn, X, k=3, n_neighbors=50):
    neighbors = knn.kneighbors(X, n_neighbors=n_neighbors, return_distance=False)
    
    neighbor_labels = tracks.iloc[neighbors[0]]["genre"]
    top_k = neighbor_labels.value_counts().head(k).index.tolist()
    return top_k

# function to predict the genre
def predict_genre(track, artist):
    features = get_track_info(track, artist)
    top_k_predictions = predict_top_k(model, features, k=3)
    
    return "rock"


  
