from bs4 import BeautifulSoup
import urllib.request


class CinemaMovies:

    my_url = 'https://www.eyecinema.ie/'
    uClient = urllib.request.urlopen(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    container = page_soup.find_all("div", {"class": "c_20"})

    def get_list_of_movies(self):
        movies = []
        for contain in self.container:
            if contain.h2 is not None:
                movie_name = contain.h2.getText()
                movies.append(movie_name)
        return movies

    def get_movie_and_details(self):
        drop_down = {}
        for contain in self.container:
            details = []
            if contain.h2 is not None:
                movie_name = contain.h2.getText()
                movie_time_container = contain.find_all("div", {"class": "c_100 timer"})
                luxury_movie_time_container = contain.find_all("div", {"class": "c_100 orange timer"})
                three_d_movie_time_container = contain.find_all("div", {"class": "c_100 purple timer"})
                sold_out_movie_time_container = contain.find_all("div", {"class": "c_100 red timer"})
                last_few_tickets_movie_time_container = contain.find_all("div", {"class": "c_100 blue timer"})
                parent_baby_time_container = contain.find_all("div", {"class": "c_100 pink timer"})
                ad_st_time_container = contain.find_all("div", {"class": "c_100 green timer"})

                movie_times = [index.getText() for index in movie_time_container]
                if movie_times:
                    details.append({"Normal": movie_times})

                luxury_movie_time = [index.getText() for index in luxury_movie_time_container]
                if luxury_movie_time:
                    details.append({"Luxury screening": luxury_movie_time})

                three_d_movie_time = [index.getText() for index in three_d_movie_time_container]
                if three_d_movie_time:
                    details.append({"3D": three_d_movie_time})

                sold_out_movie_time = [index.getText() for index in sold_out_movie_time_container]
                if sold_out_movie_time:
                    details.append({"Sold out": sold_out_movie_time})

                last_few_tickets_movie_time = [index.getText() for index in last_few_tickets_movie_time_container]
                if last_few_tickets_movie_time:
                    details.append({"Last few tickets": last_few_tickets_movie_time})

                parent_baby_time = [index.getText() for index in parent_baby_time_container]
                if parent_baby_time:
                    details.append({"Parents and baby": parent_baby_time})

                ad_st_time = [index.getText() for index in ad_st_time_container]
                if ad_st_time:
                    details.append({"Ad/st": ad_st_time})

                drop_down[movie_name] = details
        return drop_down
