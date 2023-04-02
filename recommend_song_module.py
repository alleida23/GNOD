def recommend_song(song_searched, spotify_data, topsongs):
    """
    This function takes in a song name and a dataframe spotify_data.
    It first checks if the song is in topsongs, and if so, recommends a song from topsongs.
    If the song is not in spotify_data, the function uses Spotipy to search for the song 
    and gather information about it.
    If the song is in spotify_data or its information has already been collected,
    the function creates clusters to recommend a song from the same cluster
    as the selected song..
    """
    song_searched = song_searched.lower().strip()

    # Check if the song is in top songs:
    if song_searched in topsongs['title'].str.lower().str.strip().values:
        recommended_song = topsongs.loc[topsongs['title'].str.lower().str.strip() != song_searched].sample(n=1)
        display(Markdown(f"Based on your selection of '**{song_searched.capitalize()}**', we recommend the *hot* song '**{recommended_song['title'].iloc[0]}**' by **{recommended_song['artist'].iloc[0]}**."))
        return recommended_song#, spotify_data
    
    # Nested get_song_from_spotify function:
    spotify_data = get_song_from_spotify(song_searched, spotify_data)

    X_features = spotify_data.select_dtypes(np.number)

    # Scaling Data
    scaler = StandardScaler()
    X_prep = scaler.fit_transform(X_features)

    # KMeans : 8 clusters
    kmeans = KMeans(n_clusters=8, random_state=1234)
    kmeans.fit(X_prep)

    # Finding the index of the selected song:
    spotify_data['title'] = spotify_data['title'].str.lower().str.strip()
    song_index = spotify_data.index[spotify_data['title'] == song_searched]
    
    if len(song_index) == 0:
        print(f"No matching song found for {song_searched}")
        return None, spotify_data
    
    song_index = song_index[0]

    # Predicting cluster for the selected song:
    song_cluster = kmeans.predict(X_prep[song_index].reshape(1, -1))[0]

    # Selecting a random song from the same cluster:
    cluster_songs = spotify_data[kmeans.labels_ == song_cluster]
    recommended_song = cluster_songs.sample(n=1)

    # Print recommendation:    
    display(Markdown(f"Based on your selection of '**{song_searched.capitalize()}**', we recommend the song **'{recommended_song['title'].iloc[0].upper()}'** by **'{recommended_song['artist'].iloc[0].upper()}'**."))

    return recommended_song, spotify_data
