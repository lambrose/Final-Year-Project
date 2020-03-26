from loop import db


class Genres:
    
    def get_genres(self, entries):
        genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
                  'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War',
                  'Western']
        matches = []
        for entry in entries:
            index = 0
            genre_string = ""
            # enter the id, title, description, image, popularity, date
            match = [entry[0], entry[1], entry[2], entry[3], entry[-2], entry[-1]]
            for genre in entry[4:-2]:
                # only keep the genres are actually in the movie
                if genre == 1:
                    genre_string += genres[index] + ", "
                index += 1
            # remove the last characters from te string - a space and comma
            match.append(genre_string[:-2])
            matches.append(match)
        return matches
        
    # executing a select query for the top 25 newest and popular movies , then storing it in a list
    # returning a tuple of dictionaries
    def popular_latest_movies(self):
        latest_data = list(db.engine.execute('SELECT * FROM latest_movies LIMIT 25'))
        latest = self.get_genres(latest_data)
        popular_data = list(db.engine.execute('SELECT * FROM popular_movies LIMIT 25'))
        popular = self.get_genres(popular_data)
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
