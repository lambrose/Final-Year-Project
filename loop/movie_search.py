from loop import db
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


class MovieSearch:

    def __init__(self, movie_details):
        self.movie_details = movie_details

    genres = [{'action': 'action_movies', 'adventure': 'adventure_movies', 'animation': 'animation_movies',
               'comedy': 'comedy_movies', 'crime': 'crime_movies', 'documentary': 'documentary_movies',
               'drama': 'drama_movies', 'family': 'family_movies', 'fantasy': 'fantasy_movies',
               'history': 'history_movies', 'horror': 'horror_movies', 'music': 'music_movies',
               'mystery': 'mystery_movies', 'romance': 'romance_movies',
               'science_fiction': 'science_fiction_movies', 'tv_movie': 'tv_movie_movies',
               'thriller': 'thriller_movies', 'war': 'war_movies', 'western': 'western_movies'}]

    # getting all of the movies from the specified genre sql views
    def query_db(self, movie_genres):
        all_movies = []
        for sql_view in movie_genres:
            view_results = db.engine.execute('SELECT * FROM ' + sql_view)
            for result in view_results:
                all_movies.append((result.title, result.overview, result.image, result.popularity, result.release_date))
        return all_movies

    # Checking the movie searching and getting all of the genres contained
    # Then  querying the genre sql views and returning a unique set of movies
    def get_data(self):
        movie_genres = []
        for genre_dict in self.genres:
            for genre, sql_view_name in genre_dict.items():
                if getattr(self.movie_details, genre) == 1:
                    movie_genres.append(sql_view_name)
        all_movies = self.query_db(movie_genres)
        return list(set(all_movies))

    def comparisons(self):
        # Converting the list of movies into a data frame of movies
        movie_data_frame = pd.DataFrame(self.get_data(),
                                        columns=['title', 'overview', 'image', 'popularity', 'release_date'])
        # Specifying parameters for the comparison
        tfv = TfidfVectorizer(min_df=1, max_features=None, strip_accents='unicode', analyzer='word',
                              token_pattern=r'\w{1,}', ngram_range=(1, 3), stop_words='english')
        # Specify the column for the comparison
        tfv_matrix = tfv.fit_transform(movie_data_frame['overview'])
        # Form a matrix
        sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
        # Remove duplicate movies and index them
        indices = pd.Series(movie_data_frame.index, index=movie_data_frame['title']).drop_duplicates()
        return movie_data_frame, sig, indices

    def get_recommendation(self):
        values = self.comparisons()
        # Find the position of the searched movie in the data frame
        position = values[2][self.movie_details.title]
        # Get the ordering of the movies when the movie searched is first
        sig_scores = list(enumerate(values[1][position]))
        sig_scores = sorted(sig_scores, key=lambda item: item[1], reverse=True)
        # Return the movie and ten other movies that are the most similar
        sig_scores = sig_scores[:11]
        movies_indices = [score[0] for score in sig_scores]
        movie_df = values[0].iloc[movies_indices]
        return movie_df.values.tolist()
