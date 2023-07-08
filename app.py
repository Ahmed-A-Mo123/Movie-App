from flask import Flask, render_template, jsonify, request, url_for, redirect
from datamanager.JsonManager import JsonDataManager

app = Flask(__name__)
data_manager = JsonDataManager('logs\\movie_data.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)  # Temporarily returning users as a string


@app.route('/users/<user_id>')
def list_movies(user_id):
    movies = data_manager.get_user_movies(int(user_id))
    return jsonify(movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        new_user = request.form.get('new_user')
        data_manager.add_new_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


# @app.route('/users/<user_id>/add_movie') ## Post Request
#
#
#
# @app.route('/users/<user_id>/update_movie/<movie_id>') ## Put Request
#
#
#
# @app.route('/users/<user_id>/delete_movie/<movie_id>') ## Delete Request
# def pas
#

app.run()
