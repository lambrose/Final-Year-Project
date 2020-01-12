import urllib.request
from bs4 import BeautifulSoup


class CinemaMovies:
    def website(self):
        # The cinema link, where the data will be scrapped from
        my_url = 'https://www.eyecinema.ie/'
        uClient = urllib.request.urlopen(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = BeautifulSoup(page_html, "html.parser")
        # Each movie is in a container
        return page_soup.find_all("div", {"class": "c_20"}), my_url

    # Getting all the movies and putting it into a list
    # Movies are referenced by the html h2 tag
    def get_movies(self):
        movies = []
        for contain in self.website()[0]:
            if contain.h2 is not None:
                movie_name = contain.h2.getText()
                movies.append(movie_name)
        return movies

    # Getting the movie times and type of tickets
    def get_movie_details(self):
        # All possible movie times and their different types of tickets
        ticket_types = [{"Normal screening times": " "}, {"Luxury screening times": " orange "},
                        {"3D screening times": " purple "}, {"Sold out": " red "}, {"Last few tickets": " blue "},
                        {"Parents and baby tickets": " pink "}, {"Ad/st screening times": " green "}]
        # Iterating thought the container of movies and returning the times and ticket types
        all_movie_times = {}
        for contain in self.website()[0]:
            ticket_times = []
            if contain.h2 is not None:
                movie_name = contain.h2.getText()
                for ticket_type in ticket_types:
                    for ticket, time_type in ticket_type.items():
                        # "times" is still in a html format
                        times = contain.find_all("div", {"class": "c_100" + time_type + "timer"})
                        # Getting the actual time
                        formatted_time = [index.getText() for index in times]
                        if formatted_time:
                            ticket_times.append({ticket: formatted_time})
                # Getting the movie image and stripping unnecessary data
                img = contain.find('img')
                image = img.get('src')
                if image[:1] == "/":
                    all_movie_times[movie_name] = {}
                all_movie_times[movie_name][image] = ticket_times
        return all_movie_times, self.website()[1]
