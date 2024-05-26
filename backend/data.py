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
def get_track_info():
    # Adjust the file path to where your CSV file is located
    tracks = pd.read_csv("cleaned_data_f.csv")
    track_info = [{'track': track['track_name'], 'artist': track['artists']} for _, track in tracks.iterrows()]
    return track_info

# Function to search track names
def search_songs(query):
    track_info = get_track_info()
    matching_tracks = [track for track in track_info if query.lower() in track['track'].lower()]
    return matching_tracks
