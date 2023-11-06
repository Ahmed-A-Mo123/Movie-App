from flask import Flask, render_template, request, url_for, redirect, Blueprint
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datamanager.SQLiteDataManager import SQLiteDataManager
from api import api  # Importing the API blueprint

app = Flask(__name__)
app.secret_key = 'ThisIsAhmedsSecretKey'

data_manager = SQLiteDataManager('movie_database.db')

app.register_blueprint(api, url_prefix='/api')  # Registering the blueprint

# flask_login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user_load = data_manager.get_user_by_id(user_id)
    return user_load


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        new_user_dict = {'name': request.form.get('name'),
                         'username': request.form.get('username'),
                         'password': request.form.get('password')
                         }

        if len(new_user_dict['name']) == 0:
            return redirect('add_user')
        data_manager.add_new_user(new_user_dict)
        return redirect(url_for('list_users'))
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username_input = request.form.get('username')
        password_input = request.form.get('password')
        user = data_manager.get_user_by_username(username_input)
        # check if user exists
        if user:
            # check if password matches with username
            if user.password == password_input:
                login_user(user)
                return redirect(url_for('dash'))
            else:
                return redirect((url_for('login')))
        else:
            print('user doesnt exist')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/dash')
@login_required
def dash():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('user_dashboard.html', name=request.args.get('user'))


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users,)  # Temporarily returning users as a string


@app.route('/users/<user_id>')
def list_movies(user_id):
    movies = data_manager.get_user_movies(int(user_id))
    if movies == 'User ID Not Found':
        return render_template('error_page.html', error=movies)
    return render_template('movies.html', movies=movies, active_user=int(user_id))


@app.route('/users/<user_id>/list_reviews/<movie_id>', methods=['GET', 'POST'])
def list_movie_reviews(user_id, movie_id):
    reviews = data_manager.get_all_movies_reviews(movie_id)
    return render_template('reviews.html', reviews=reviews, user_id=user_id, movie_id=movie_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == "POST":
        new_user = request.form.get('new_user')
        if len(new_user) == 0:
            return redirect('add_user')
        data_manager.add_new_user(new_user)
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])  # Post Request
def add_movie(user_id):
    if request.method == "POST":
        new_movie = request.form.get('new_movie')
        try:
            data_manager.add_movie(user_id, new_movie)
            return redirect(url_for('list_movies', user_id=user_id))
        except ValueError:
            return render_template('error_page.html', error='Movie Not Found')

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/add_review/<movie_id>', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    if request.method == "POST":
        review_content = request.form.get('new_movie_review')
        data_manager.add_review(movie_id, review_content)
        return redirect(url_for('list_movie_reviews', user_id=user_id, movie_id=movie_id))
    return render_template('add_review.html', user_id=user_id, movie_id=movie_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = data_manager.return_one_movie(user_id, movie_id)  # placeholders which populate the input boxes

    if data_manager.check_if_user_exist(int(user_id)):
        return render_template('error_page.html', error='User was not found'), 404

    if request.method == "POST":
        try:
            new_movie_data = {"name": request.form.get('title'),
                              "director": request.form.get('director'),
                              "year": int(request.form.get('year')),
                              "rating": float(request.form.get('rating'))
                              }
            data_manager.update_movie(user_id, movie_id, new_movie_data)
        except ValueError:
            return render_template('update_movie.html', movie=movie, user_id=user_id, movie_id=movie_id,
                                   error='Please fill in all boxes')

        return redirect(url_for('list_movies', user_id=user_id))

    return render_template('update_movie.html', movie=movie, user_id=user_id, movie_id=movie_id)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])  # Delete Request
def delete_movie(user_id, movie_id):
    movie = data_manager.return_one_movie(user_id, movie_id)
    if movie is False:
        return render_template('error_page.html', error="Movie Or User Couldn't Be Found")
    data_manager.delete_movie(int(user_id), int(movie_id))
    return render_template('delete_movie.html', movie=movie, current_user=user_id)


# if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5003)
