from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_database.db'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))



class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    director = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    poster = db.Column(db.String(255))

    # foreign key set up
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref=db.backref('movies', lazy=True))


db.create_all()
new_user = Users(name='Ahmed')
db.session.add(new_user)
new_movie = \
    Movies(title='Interstellar', director='Christopher Nolan', rating=8, poster='data:', user_id=1)

db.session.add(new_movie)
db.session.commit()

# movies = db.session.query(Movies).all()
# for movie in movies:
#     print(movie.rating)

# app.run()
