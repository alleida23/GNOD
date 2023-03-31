
def song_recommender(topsongs, spotify_data, song_searched):
    
    # Converting both input value and 'title' in lower case
    song_searched = song_searched.lower() 
    topsongs['title'] = topsongs['title'].str.lower()
    
    # ------------------IF song in the input IS IN TOPSONGS ---------------------------
    if song_searched in topsongs['title'].values:
        # While song in input IS different from the recommended (output)
        while True:
            # Generating a random number to select another song from the list
            random_num = random.randint(0, len(topsongs)-1)
            # Picking the song 'title' with random_num index
            song_recommended_title = topsongs.iloc[random_num]['title']
            # Getting also the artist name 
            song_recommended_artist = topsongs.iloc[random_num]['artist']
            # If recommended song IS NOT the same as the searched one, stop the while
            if song_recommended_title != song_searched:
                break
        # Capitalizing first letters of 'title' (.title())
        song_recommended_title = song_recommended_title.title()
        # Joinning song and artist to display in the output
        song_recommended = f"{song_recommended_title} by {song_recommended_artist}"
        # Displaying output with both 'title' and 'artist' bigger and bolt style.
        display(Markdown(f"You should listen to: **{song_recommended}**!"))
    
    # ------------------If song in the input IS NOT IN TOPSONGS--------------------------
    else:
        # All numerical columns AFTER 'uri' are the features to be taken
        features = spotify_data.select_dtypes(np.number)
    
        # Select X, but no target yet
        X = features

        # Scaling Data
        X_prep = StandardScaler().fit_transform(X)

        # Creating 8 clusters/segments (Kmeans)
        kmeans = KMeans(n_clusters=8, random_state=1234)
        kmeans.fit(X_prep)
    
        # Predicting / assigning the clusters:
        clusters = kmeans.predict(X_prep)
    
        # Converting both searched song and 'title' in spotify_data to lower case
        song_searched = song_searched.lower() 
        spotify_data['title'] = spotify_data['title'].str.lower()

        # ------------------Checking if the input song IS IN the Spotify data ------------
        if song_searched in spotify_data['title'].values:
        
            # Extracting the features for the input song 
            # (filtering through boolean mask and selecting first row of filtered)
            song_features = features.loc[spotify_data['title']==song_searched].iloc[0]
    
    
            # Predicting/assigning a cluster for song_searched:
    
            # Solving dimensional issue and need for array:   
            # Convert target_song to a numpy array and reshape to be a 2-dimensional array with one row
            song_features_arr = np.array(song_features).reshape(1, -1)
    
            # Scaling target_song values using the same X_prep scaler used for X data
            song_features_prep = StandardScaler().fit(X_prep).transform(song_features_arr)
    
            # Predicting / assigning the cluster using the same Kmeans fitted before:
            song_cluster = kmeans.predict(song_features_prep)
    
        
            # Recommending the most similar song from that cluster:
        
            # Selecting all songs from the same cluster as song_searched (song_cluster)
            songs_in_cluster = spotify_data[kmeans.labels_ == song_cluster[0]]
        
                    ## Note(I)
    
            # Comparing song_searched with songs in same cluster using cosine_similarity
            from sklearn.metrics.pairwise import cosine_similarity
        
                    ## Note (II)
    
            # Calculating cosine similarity between searched song and songs in cluster
            similarities = cosine_similarity(song_features_prep, songs_in_cluster.select_dtypes(np.number))
    
            # Finding the most similar song in the cluster
            most_similar_song_idx = np.argmax(similarities)
        
                    ## Note (III)
    
            # Retrieving the most similar song from the cluster
            most_similar_song = songs_in_cluster.iloc[most_similar_song_idx]['title']
    
    
            # Recommending another random song from that cluster:
        
            # Selecting a random song from that cluster
            random_song_idx = np.random.choice(np.where(kmeans.labels_ == song_cluster)[0])

            # Check random_song and most_similar_sonog are not the same. If so, repeat random choice.
            while spotify_data.iloc[random_song_idx]['title'] == most_similar_song:
                random_song_idx = np.random.choice(np.where(kmeans.labels_ == song_cluster)[0])

            # Getting title of random song
            random_song = spotify_data.iloc[random_song_idx]['title']

    
            display(Markdown(f"The song '**{song_searched.capitalize()}**' belongs to cluster '**{song_cluster[0]}**'.\n\n"
                  f"The most similar song in the cluster is '**{most_similar_song.capitalize()}**'.\n\n"
                  f"Here's a random song from the same cluster: '**{random_song.capitalize()}**'."))

 
    
        else:
    
            return f"The song '**{song_searched}**' is not in our data."