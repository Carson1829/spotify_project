import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the dataset and the model
tracks = pd.read_csv("cleaned_data_mil.csv")

# Load pickled files
model = pickle.load(open('best_knn_model_mil.pkl', 'rb'))
encoder = pickle.load(open('encoder.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
# Function to get track features given the track and artist name
def get_track_info(track, artist): 
    # Find the song in the dataset
    song = tracks[(tracks['track_name'] == track) & (tracks['artists'] == artist)]

    # Extract the features for the song
    features = song[['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 
                     'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
                     'time_signature']]
    
    features_scaled = scaler.transform(features)
    return features_scaled

# Function to predict the genre of a song given its track and artist name
def predict_genre(track, artist):
    # Get the features of the track
    features = get_track_info(track, artist)
    
    if features is None:
        return "Track or artist not found in the dataset"
    
    # Make the prediction using the KNN model
    encoded_prediction = model.predict(features)
    
    # Reverse the label encoding to get the original genre
    genre_prediction = encoder.inverse_transform(encoded_prediction)
    
    # Return the predicted genre
    return genre_prediction[0]

# Function to predict top k genres
def predict_top_k(knn, X, k=3, n_neighbors=50):
    neighbors = knn.kneighbors(X, n_neighbors=n_neighbors, return_distance=False)
    
    neighbor_labels = tracks.iloc[neighbors[0]]["genre"]
    top_k = neighbor_labels.value_counts().head(k).index.tolist()

    predicted_genre_str = ', '.join(top_k)
    
    return predicted_genre_str

# Example usage of predict_genre
predicted_genre = predict_genre("Arabella", "Arctic Monkeys")
print(f"The predicted genre is: {predicted_genre}")

# prediction top 3 genres
features = get_track_info("Love Story", "Taylor Swift")
if features is not None:
    top_k_predictions = predict_top_k(model, features, k=3)
    print(f"Top k predicted genres: {top_k_predictions}")
else:
    print("Track or artist not found in the dataset")


