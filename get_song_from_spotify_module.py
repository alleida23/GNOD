def get_song_from_spotify(song_searched, spotify_data):
    
    """
    The function searches for a song in the Spotify database by taking in a song name 
    and a dataframe spotify_data. If the song is not in spotify_data, it searches for
    the song in the Spotify API and extracts information such as URI and features
    of the selected song. This information is converted to a DataFrame and appended to
    spotify_data. The updated dataframe is returned, and if the song is not found,
    it returns None.
    """
    
    # If song is NOT in spotify data:
    if song_searched not in spotify_data['title'].values:
        
        # Search song
        track_id = sp.search(q='track:' + song_searched, type='track')  # song info

        # If multiple versions of song played by different artists are found:
        if len(track_id['tracks']['items']) > 1:
            # Print list of artists who played the song
            print("Multiple versions of the song '{}' were found:".format(song_searched))
            for i, item in enumerate(track_id['tracks']['items']):
                print("{}: {}".format(i+1, item['album']['artists'][0]['name']))
                
            # Ask user to select the desired version of the song
            while True:
                try:
                    selection = int(input("Please enter the NUMBER of the version you are looking for: "))
                    if selection < 1 or selection > len(track_id['tracks']['items']):
                        print("Invalid selection. Please enter a NUMBER between 1 and {}.".format(len(track_id['tracks']['items'])))
                    else:
                        break
                except ValueError:
                    print("Invalid selection. Please enter a NUMBER between 1 and {}.".format(len(track_id['tracks']['items'])))
            
            # Use the selected version of the song
            item = track_id['tracks']['items'][selection-1]
        
        else:
            # Use the only version of the song found
            item = track_id['tracks']['items'][0]
        
        # Extracting info of new song
        song_uri = item['uri']  # uri
        features = sp.audio_features(song_uri)[0]

        # New dict retrieving values of 'title', 'artist' and 'uri'
        track = {
            'title': item['name'],
            'artist': item['album']['artists'][0]['name'],
            'uri': song_uri,
        }

        # For each feature (song uri) add in track dict
        # new key (column name) and the value
        for feature_key, feature_value in features.items():
            track[feature_key] = feature_value

        # Append new songs to spotify_data
        new_song_df = pd.DataFrame([track])
        spotify_data = pd.concat([spotify_data, new_song_df], axis=0)#, ignore_index=True)
        spotify_data = spotify_data.drop_duplicates()
        #spotify_data = spotify_data.drop(['Unnamed: 0'], axis=1)
        spotify_data = spotify_data.reset_index(drop=True)
        #spotify_data.to_csv('spotify_data.csv')
        
        # Return the results as a DataFrame
        print("{} was not in spotify_data database".format(song_searched))
        return spotify_data
    
    else:
        
        print("{} was already in spotify_data database".format(song_searched))
        return spotify_data

    
        # track_name = track_id['tracks']['items'][0]['name'] # title
       # track_id['tracks']['items'][0]['album']['artists'][0]['name'] # artist band
       # song_uri = track_id['tracks']['items'][0]['uri'] # uri
       # features = sp.audio_features(song_uri)[0]
   
   