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
        data = self.website()
        for contain in data[0]:
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
        return all_movie_times, data[1]

#****************************************************
# This html code below is for the cinema recommendation
# Due to the coronavirus, the cinemas are closed, so there are no movies to scrape from the cinema website
#****************************************************
# {% extends "layout.html" %}
# {% block content %}
# <div class="col-md-8">
#     <div class="text-center">
#         <H1 class="article-content">Recommended Movie:</H1>
#         <h2 class="article-content">{{ top_movie[0] }}</h2>
#         <img src="{{ top_movie[1] }}" class="img-fluid img-thumbnail" width="300" height="400">
#         {% for ticket in top_movie[2] %}
#             {% for ticket, times in ticket.items() %}
#                     <select class="form-control form-control-lg">
#                         <option value="{{ticket}}">{{ticket}}</option>
#                       {% for time in times %}
#                         <option value="{{time}}">{{time}}</option>
#                       {% endfor %}
#                     </select>
#             {% endfor %}
#         {% endfor %}
#
#         <h4 class="article-content">Recommendation score: {{ top_movie[3] }}</h4>
#         <h4> For more info:
#             <a href="{{ top_movie[4] }}"><button class="btn btn-info">Eye cinema</button></a>
#         </h4>
#     </div>
# </div>
#
# <div class="col-md-4">
#     <div class="sidebar-section">
#         {% if other_movies %}
#             {% if other_movies|count > 1%}
#             <H3 class="article-content border-bottom mb-4">Other Movies:</H3>
#             {% else %}
#                 <H3 class="article-content border-bottom mb-4">Other Movie:</H3>
#             {% endif %}
#
#             {% for movie in other_movies %}
#             <div class="text-center">
#                 <button type="button" class="collapsible_movies">{{ movie[0] }}</button>
#                 <div class="collapsible_movies_content">
#                 <img src="{{ movie[1] }}" class="img-fluid img-thumbnail">
#                 {% for ticket in movie[2] %}
#                     {% for ticket, times in ticket.items() %}
#                         <select class="form-control form-control-lg">
#                                 <option value="{{ticket}}">{{ticket}}</option>
#                               {% for time in times %}
#                                 <option value="{{time}}">{{time}}</option>
#                               {% endfor %}
#                             </select>
#                     {% endfor %}
#                 {% endfor %}
#                 <p class="article-content"><b>Recommendation score: {{ movie[3] }}</b></p>
#                 <p> For more info:
#                     <a href="{{ movie[4] }}"><button class="btn btn-info">Eye cinema</button></a>
#                 </p>
#                 </div>
#             </div>
#             {% endfor %}
#         {% else %}
#             <h4> There are no other movies</h4>
#         {% endif %}
#     </div>
#
#     <script>
#     var movies = document.getElementsByClassName("collapsible_movies");
#     var index;
#
#     // loop through all the nested movies
#     for (index = 0; index < movies.length; index++) {
#         // action listener to determine which movie has been pressed
#       movies[index].addEventListener("click", function() {
#         this.classList.toggle("active");
#         // if pressed and  open then close else open and display content
#         var movie_content = this.nextElementSibling;
#         if (movie_content.style.display === "block") {
#           movie_content.style.display = "none";
#         } else {
#           movie_content.style.display = "block";
#         }
#       });
#     }
#     </script>
# </div>
# {% endblock content %}
