import pandas as pd
import pickle

tracks = pd.read_csv("cleaned_data_mil.csv")
track_df = [{'track': track['track_name'], 'artist': track['artists']} for _, track in tracks.iterrows()]

model = pickle.load(open('best_knn_model_mil.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Function to give search bar suggestion by filtering through dataset
def search_songs(query):

    matching_tracks = []
    
    # Iterate through the tracks until we find the top ten matches
    for track in track_df:
        if track['track'].lower().startswith(query.lower()):
            matching_tracks.append(track)
            if len(matching_tracks) == 20:
                break  
    
    return matching_tracks

# Function to get features of a song given its track and artist name
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

# Function for prediction
def predict_genre(track, artist):
    features = get_track_info(track, artist)
    predictions = predict_top_k(model, features, k=3)
    # Convert list of genres to comma-separated string
    predicted_genre_str = ', '.join(predictions)
    
    return predicted_genre_str


  
