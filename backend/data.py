import pandas as pd

'''
def get_track_names():
    # Adjust the file path to where your CSV file is located
    tracks = pd.read_csv("cleaned_data_mil.csv")
    track_names = tracks['track_name'].tolist()  # Adjust the column name if different
    return track_names

# Function to search track names
def search_songs(query):
    track_names = get_track_names()
    return [track for track in track_names if query.lower() in track.lower()]

'''
tracks = pd.read_csv("cleaned_data_f.csv")

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
    
    # Check if the song exists in the dataset
    if song.empty:
        return "0"
    else:
        return "1"
  
