from loop import db


class Genres:
    # executing a select query for the top 25 newest and popular movies , then storing it in a list
    # returning a tuple of dictionaries
    def popular_latest_movies(self):
        latest = list(db.engine.execute('SELECT * FROM latest_movies LIMIT 25'))
        popular = list(db.engine.execute('SELECT * FROM popular_movies LIMIT 25'))
        return {'Newest Movies': latest}, {'Most Popular Movies': popular}

    def movies_genres(self, genre):
        # get the sql view name of the drop down selected value
        # running a select query
        # the values of the keys in the dictionary correspond to a sql view
        movies = {'Action': 'action_movies', 'Adventure': 'adventure_movies', 'Animation': 'animation_movies',
                  'Comedy': 'comedy_movies', 'Crime': 'crime_movies', 'Documentary': 'documentary_movies',
                  'Drama': 'drama_movies', 'Family': 'family_movies', 'Fantasy': 'fantasy_movies',
                  'History': 'history_movies', 'Horror': 'horror_movies', 'Music': 'music_movies',
                  'Mystery': 'mystery_movies', 'Romance': 'romance_movies',
                  'Science Fiction': 'science_fiction_movies', 'TV Movie': 'tv_movie_movies',
                  'Thriller': 'thriller_movies', 'War': 'war_movies', 'Western': 'western_movies'}
        sql_view = movies.get(genre)
        selected_movie = list(db.engine.execute('SELECT * FROM ' + sql_view + ' LIMIT 150'))
        return {genre: selected_movie}
