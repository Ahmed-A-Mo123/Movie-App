from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from datamanager.manager import DataManagerInterface
import requests

Base = declarative_base()

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    director = Column(String(255))
    rating = Column(Integer)
    year = Column(Integer)
    poster = Column(String(255))

    # foreign key set up
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref=backref('movies', lazy=True))


class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    review = Column(String(255))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship('Movies', backref=backref('reviews', lazy=True))


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, file_name):
        self.engine = create_engine(f'sqlite:///datamanager//{file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    @staticmethod
    def movie_api(movie_name):
        """ Accesses the movie API to return key information about the movie (helper function) """
        space_replace_title = movie_name.replace(' ', '+')
        response = requests.get(API_URL + space_replace_title)
        if response.json()["Response"] == "False":
            raise ValueError("Cannot divide by zero")
        return response.json()

    def check_if_user_exist(self, user_id):
        """This is a helper function which tells me if a user exists or not"""
        session = self.Session()
        user_search = session.query(Users). \
            filter(and_(Users.id == user_id)). \
            first()
        if user_search is None:
            return True  # User DOESN'T exits
        else:
            return False  # User DOES exits

    def get_all_users(self):
        """ Returns all the users in our Database"""
        session = self.Session()
        all_users = session.query(Users).all()
        session.close()
        return all_users

    def get_user_movies(self, user_id):
        """ Returns a list of all movies for a given user"""
        session = self.Session()

        if self.check_if_user_exist(user_id):
            return 'User ID Not Found'
        else:
            all_movies = session.query(Movies).filter(
                Movies.user_id == user_id).all()  # join to get more info about the user
            session.close()
            return all_movies

    def get_all_movies(self):
        """Returns all movies in the database (Might be useful later down the line)"""
        session = self.Session()
        all_movies = session.query(Movies).all()  # join to get more info about the user
        session.close()
        return all_movies

    def get_all_movies_reviews(self, movie_id):
        """ Returns all the reviews for one specific movie"""
        session = self.Session()
        all_reviews = session.query(Reviews). \
            filter(Reviews.movie_id == movie_id). \
            all()
        session.close()
        return all_reviews

    def return_one_movie(self, user_id, movie_id):
        """Helper function which returns one movie"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie.id == int(movie_id):
                return movie

        return 'User or Movie Not Found!'

    def add_new_user(self, new_user):
        """Adds a new user to the webapp"""
        session = self.Session()
        new_user = Users(name=new_user)
        session.add(new_user)
        session.commit()
        session.close()

    def add_review(self, movie_id, review_content):
        """Adds a review to a specific movie in the users favourite list """
        session = self.Session()
        new_review = Reviews(review=review_content, movie_id=movie_id)
        session.add(new_review)
        session.commit()
        session.close()

    def add_movie(self, user_id, movie_name):
        """Adds a new favourite movie for a user"""
        session = self.Session()
        movie_api_data = self.movie_api(movie_name)

        title = movie_api_data['Title']
        director = movie_api_data['Director']
        rating = movie_api_data['imdbRating']
        year = movie_api_data['Year']
        poster = movie_api_data['Poster']

        new_movie = Movies(title=title, director=director, rating=rating, year=year, poster=poster, user_id=user_id)
        session.add(new_movie)

        session.commit()
        session.close()

    def update_movie(self, user_id, movie_id, new_movie_data):
        """Updates key information about a movie in our database"""
        session = self.Session()
        try:
            movie_to_update = session.query(Movies). \
                filter(and_(Movies.id == movie_id, Movies.user_id == user_id)). \
                one()

            movie_to_update.title = new_movie_data['name']
            movie_to_update.director = new_movie_data['director']
            movie_to_update.year = new_movie_data['year']
            movie_to_update.rating = new_movie_data['rating']
            session.commit()
        except NoResultFound:
            print("Movie Or User Could Not Be Found ")
            session.rollback()  # Roll back the transaction in case of an error
        finally:
            session.close()

    def delete_movie(self, user_id, movie_id):
        """Removes a movie from a users favourite movie database"""
        session = self.Session()

        movie_to_delete = session.query(Movies). \
            filter(and_(Movies.id == movie_id, Movies.user_id == user_id)). \
            first()

        if movie_to_delete:
            session.delete(movie_to_delete)
            session.commit()
            session.close()
            return "Movie deleted successfully."
        else:
            session.close()
            return "Movie not found in the database."
