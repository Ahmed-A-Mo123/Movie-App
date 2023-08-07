from flask import Blueprint, jsonify, request
from datamanager.SQLiteDataManager import SQLiteDataManager

api = Blueprint('api', __name__)
data_manager = SQLiteDataManager('movie_database.db')


@api.route('/users', methods=['GET'])
def get_users():
    users_data = data_manager.get_all_users()
    users = [{"name": user.name} for user in users_data]
    return jsonify(users)


@api.route('users/<user_id>/movies', methods=['GET', 'POST'])
def get_user_movies_and_add(user_id):
    if request.method == "POST": # Body request should have a dictionary with key named title (Postman Tested)
        data = request.json
        data_manager.add_movie(user_id, data['title'])
        user_data = data_manager.get_user_movies(user_id)
        user_movies = [{'title': user_movie.title} for user_movie in user_data]
        return jsonify(user_movies)

    user_data = data_manager.get_user_movies(user_id)
    user_movies = [{'title': user_movie.title} for user_movie in user_data]
    return jsonify(user_movies)




