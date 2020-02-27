import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
from loop.models import Movies


class MovieSearch:

    def __init__(self, movie_details):
        self.movie_details = movie_details

    def compare_data(self):
        # getting all movies that are animated or not depending on the movie searched
        data = Movies.query.filter_by(animation=self.movie_details.animation)
        # Converting the list of SQLalchemy movies objects into a data frame of movies
        movie_data_frame = pd.DataFrame([(d.title, d.overview, d.image, d.popularity, d.release_date) for d in data],
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
        values = self.compare_data()
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
