from bs4 import BeautifulSoup
import urllib.request
import re


class ImdbMovies:

    my_url = 'https://www.imdb.com/list/ls055386972/'
    uClient = urllib.request.urlopen(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    # get the first fifteen entries
    container = page_soup.find_all("div", {"class": "lister-item mode-detail"})[0:15]

    def get_movies(self):
        movies = []
        for contain in self.container:
            # check if this entry has a name, if so add it to a list
            if contain.h3.a is not None:
                movie_name = contain.h3.a.getText()
                movies.append(movie_name)
        return movies

    def get_movie_details(self):
        drop_down = {}
        # These urls are used to direct the user back to the main page for a specific movie
        start_url = "https://www.imdb.com/"
        end_url = "?ref_=adv_li_tt"

        for contain in self.container:
            details = []
            # check if this movie has a name, if there is no name, then it's invalid
            if contain.h3.a is not None:
                movie_name = contain.h3.a.getText()
                # parsing all the required fields down below
                movie_image_container = contain.find('div', {"class": 'lister-item-image ribbonize'})
                movie_image = movie_image_container.find('img').get('loadlate')
                details.append(movie_image)
                movie_year = contain.h3.find('span', {"class": 'lister-item-year text-muted unbold'}).text
                # remove any punctuation
                movie_year = re.sub(r'[^\w\s]', '', movie_year)
                details.append(movie_year)
                movie_rating = contain.find('span', {"class": 'ipl-rating-star__rating'}).getText()
                details.append(movie_rating)
                middle_url = contain.h3.a.get('href')
                movie_url = start_url + middle_url + end_url
                details.append(movie_url)
                # Storing each movie details in a dictionary with the movie name as the key
                drop_down[movie_name] = details
        return drop_down
