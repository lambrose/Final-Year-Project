# import re
# import unidecode
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_socketio import join_room, leave_room
from loop import socketio
from flask_login import current_user
from loop.algorithm import Algorithms
# from loop.cinema import CinemaMovies
from loop.chat.forms import JoinRoom, CreateRoom
from loop.imdb_movies import ImdbMovies
from loop.main.forms import cinema_list
from collections import defaultdict

chat = Blueprint('chat', __name__)
used_rooms = defaultdict(list)
unrated_movies = defaultdict(list)
joined_users = defaultdict(list)
rated_movies = defaultdict(list)
submissions = defaultdict(list)


@chat.route('/group_chat_options', methods=['GET', 'POST'])
def group_chat_options():
    create_form = CreateRoom()
    join_form = JoinRoom()
    return render_template("group_chat_options.html", create_form=create_form, join_form=join_form)


# @chat.route('/group_chat')
# def group_chat():
#     # get the max number of users that can vote in the group
#     num_people = request.args.get('num_people')
#     # specify the room entering
#     room = request.args.get('room')
#     # username is equal to the current person logged in
#     username = current_user.first_name + " " + current_user.last_name
#     # get current list of movies in the cinema
#     cinema_movies = CinemaMovies()
#     cinema_form = cinema_list(cinema_movies.get_movies())
#
#     # creating a chat room
#     if room is None:
#         # specify the maximum amount of rooms that can be created
#         for index in range(100):
#             index = str(index)
#             # check if this room has not been created, then create it
#             if used_rooms.get(index) is None:
#                 room = index
#                 # store the amount of voters per room
#                 used_rooms[room].append(num_people)
#                 return render_template('group_chat.html', username=username, room=room, render_form=1,
#                                        cinema_form=cinema_form, num_people=num_people)
#         #  all rooms are occupied
#         if room is None:
#             return redirect(url_for('chat.group_chat_options'))
#
#     # enter a chat room with valid room number
#     elif used_rooms.get(room):
#         return render_template('group_chat.html', username=username, room=room, render_form=1,
#                                cinema_form=cinema_form, num_people=used_rooms.get(room)[0])
#     else:
#         return redirect(url_for('chat.group_chat_options'))


@chat.route('/group_chat', methods=['GET', 'POST'])
def group_chat():
    form_request = request.form
    # get the  number of users that can vote in the group
    num_people = form_request.get('voters')
    # specify the room entering
    room = form_request.get('room')
    # username is equal to the current person logged in
    username = current_user.first_name + " " + current_user.last_name
    # get current list of movies in the cinema
    imdb_movies = ImdbMovies()
    cinema_form = cinema_list(imdb_movies.get_movies())

    # creating a chat room
    if room is None:
        # specify the maximum amount of rooms that can be created
        for index in range(1, 101):
            index = str(index)
            # check if this room has not been created, then create it
            if used_rooms.get(index) is None:
                room = index
                # store the amount of voters per room
                used_rooms[room].append(num_people)
                return render_template('group_chat.html', username=username, room=room, render_form=1,
                                       cinema_form=cinema_form, num_people=num_people)
        #  all rooms are occupied
        if room is None:
            flash('There are no available chat rooms. Please try again later.', 'success')
            return redirect(url_for('chat.group_chat_options'))

    # enter a chat room with valid room number
    elif used_rooms.get(room):
        return render_template('group_chat.html', username=username, room=room, render_form=1,
                               cinema_form=cinema_form, num_people=used_rooms.get(room)[0])
    else:
        flash('The room entered has not been created.', 'success')
        return redirect(url_for('chat.group_chat_options'))


@socketio.on('join_room')
def handle_join_room_event(data):
    join_room(data['room'])
    # store all users who entered a specific room
    if data['username']:
        joined_users[data['room']].append(data['username'])
    # the amount of people per room
    data['users_in'] = len(joined_users[data['room']])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('send_message')
def handle_send_message_event(data):
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('send_movies_to_be_rated')
def handle_movies_message_event(data):
    # monitor all movies submitted per room
    unrated_movies[data['room']].append(data['message'])
    # append the the amount of voters, to ensure all users have voted
    data["people"] = used_rooms.get(data['room'])[0]
    # specify submitted movies per room
    movies = unrated_movies.get(data['room'])
    data["movies"] = list(set(movies))
    # check if all voters have submitted a movie
    if len(unrated_movies.get(data['room'])) == int(used_rooms.get(data['room'])[0]):
        # check if there is more than one unique movie
        if len(list(set(movies))) > 1:
            socketio.emit('receive_movies_to_be_rated', data, room=data['room'])
            # reset room space
            unrated_movies[data['room']] = []
        else:
            # users need to specify another movie, i.e. there needs to be at least 2 movies
            data["movies"] = "invalid_amount"
            socketio.emit('receive_movies_to_be_rated', data, room=data['room'])
            unrated_movies[data['room']] = []


@chat.route('/submit_rated_movies', methods=['GET', 'POST'])
def submit_rated_movies():
    room = request.form['room_rec']
    num_people = -1
    username = current_user.first_name + " " + current_user.last_name
    # html form submitted
    for index in range(len(request.form)):
        try:
            # append all the data submitted from a form per room
            rated_movies[room].append(request.form['input_rating_' + str(index)])
        except KeyError:
            break
    if used_rooms.get(room):
        submissions[room].append(1)
        if len(submissions.get(room)) >= int(used_rooms[room][0]):
            num_people = -100

    return render_template('group_chat.html', username=username, room=room, render_form=0, cinema_form=None,
                           num_people=num_people)


# def format_movie_title(movie):
#     # Removing unwanted characters in the movie name except for a hyphen '-'
#     format_title = re.sub(r'[^\w\s-]', '', movie["movie"])
#     unaccented_string = unidecode.unidecode(format_title)
#     # replacing spaces with a "-"
#     return unaccented_string.replace(' ', '-')


# @socketio.on('send_movie_recommendations')
# def handle_send_recommendations_event(data):
#     # get cinema list
#     cinema_movies = CinemaMovies()
#     cinema_details = cinema_movies.get_movie_details()
#     # pass in the list of rated movies into the algorithm class
#     algorithm = Algorithms(rated_movies.get(data['room']))
#     movies = algorithm.run()
#     # filter movies from most recommended to other
#     # top_movie, other_movies = [], []
#     all_movies = []
#     counter = 0
#     for movie in movies:
#         cinema_url = cinema_details[1]
#         movie_url = cinema_url + "movie/" + format_movie_title(movie)
#         for title, movie_details in cinema_details[0].items():
#             if title == movie["movie"]:
#                 for image, times in movie_details.items():
#                     all_movies.append((title, cinema_url + image, movie["score"], movie_url))
#         counter += 1
#     socketio.emit('receive_movie_recommendations', all_movies, room=data['room'])


@socketio.on('send_movie_recommendations')
def handle_send_recommendations_event(data):
    # get imdb list
    imdb_movies = ImdbMovies()
    imdb_details = imdb_movies.get_movie_details()
    # pass in the list of rated movies into the algorithm class
    algorithm = Algorithms(rated_movies.get(data['room']))
    movies = algorithm.run()
    all_movies = []
    for movie in movies:
        for title, details in imdb_details.items():
            # find a movie match before adding the value to a list
            if title == movie["movie"]:
                all_movies.append((title, details[0], details[1], details[2], movie["score"], details[3]))
    socketio.emit('receive_movie_recommendations', all_movies, room=data['room'])
    # reset movie ratings for a room
    rated_movies[data['room']] = []


@socketio.on('leave_room')
def handle_leave_room_event(data):
    leave_room(data['room'])
    # check if user is in the room before removing them from the room
    if data['username'] in joined_users[data['room']]:
        joined_users[data['room']].remove(data['username'])
    # if everyone has left the room, then delete it
    if not joined_users.get(data['room']):
        del joined_users[data['room']]
        try:
            del used_rooms[data['room']]
        except KeyError:
            pass
        try:
            del submissions[data['room']]
        except KeyError:
            pass
    socketio.emit('leave_room_announcement', data, room=data['room'])
