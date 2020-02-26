import requests
from loop.models import Movies
from loop import db
from sqlalchemy import exc


class UpdateMovieDatabase:

    api_key = "dbe1e3a942b4315f2b55624246f41956"
    base_url = "https://api.tmdb.org/3/discover/movie/?api_key=" + api_key

    # Truncate table, reset table entries
    def truncate_table(self):
        db.engine.execution_options(autocommit=True).execute("TRUNCATE TABLE movies")

    def insert_movies(self):
        self.truncate_table()

        # All possible genre ids with an initial value of zero
        genre_ids = {28: 0, 12: 0, 16: 0, 35: 0, 80: 0, 99: 0, 18: 0, 10751: 0, 14: 0, 36: 0, 27: 0, 10402: 0, 9648: 0,
                     10749: 0, 878: 0, 10770: 0, 53: 0, 10752: 0, 37: 0}

        is_valid = True
        # There are 500 pages
        for i in range(1, 150):
            # sending get request and saving the response as response object
            r = requests.get(url=self.base_url, params={'page': i})
            # getting the data in json format
            data = r.json()
            for movie in data["results"]:
                # checking if keys have empty values
                if not movie.get('title'):
                    is_valid = False
                if not movie.get('overview'):
                    is_valid = False
                if not movie.get('poster_path'):
                    is_valid = False
                if not movie.get('genre_ids'):
                    is_valid = False
                else:
                    # Specifying what genres are related to the movie by assigning the the dict value 1
                    for genre_id in movie.get('genre_ids'):
                        genre_ids[genre_id] = 1
                if not movie.get('popularity'):
                    is_valid = False
                if not movie.get('release_date'):
                    is_valid = False

                # If all params have a value that is not none, the add the entry to the database
                if is_valid:
                    entry = Movies(title=movie['title'], overview=movie['overview'],
                                   image="https://image.tmdb.org/t/p/w500/" + movie['poster_path'],
                                   action=genre_ids[28], adventure=genre_ids[12], animation=genre_ids[16],
                                   comedy=genre_ids[35], crime=genre_ids[80], documentary=genre_ids[99],
                                   drama=genre_ids[18], family=genre_ids[10751], fantasy=genre_ids[14],
                                   history=genre_ids[36], horror=genre_ids[27], music=genre_ids[10402],
                                   mystery=genre_ids[9648], romance=genre_ids[10749], science_fiction=genre_ids[878],
                                   tv_movie=genre_ids[10770], thriller=genre_ids[53], war=genre_ids[10752],
                                   western=genre_ids[37], popularity=movie['popularity'],
                                   release_date=movie['release_date'])
                    db.session.add(entry)
                    try:
                        db.session.commit()
                        genre_ids = {key: 0 for key in genre_ids}
                    except exc.SQLAlchemyError:
                        print(movie)
                # reset boolean value
                is_valid = True
