from datamanager.manager import DataManagerInterface
import json
import os
import requests

API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=e9c4608d&t='


class JsonDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        """ Helper Function Which Only Reads The Contents Of The File Given"""
        with open(self.filename, 'r') as fileobj:
            data = json.load(fileobj)
            return data

    def write_file(self, data):
        """ Helper Function Which Only Writes The Contents Of The File Given"""
        with open(self.filename, 'w') as fileobj:
            json.dump(data, fileobj)

    @staticmethod
    def movie_api(movie_name):
        space_replace_title = movie_name.replace(' ', '+')
        response = requests.get(API_URL + space_replace_title)
        if response.json()["Response"] == "False":
            raise ValueError("Cannot divide by zero")
        return response.json()

    def check_if_user_exist(self, user_id):
        data = self.read_file()
        if user_id > len(data) or user_id == 0:
            return True
        else:
            return False


    def get_all_users(self):
        """Returns a list of all users"""
        data = self.read_file()
        return data

    def get_user_movies(self, user_id):
        """ Returns a list of all movies for a given user"""
        users = self.read_file()
        for user in users:
            if user['id'] == int(user_id):
                return user['movies']
        return "User ID Not Found"

    def return_one_movie(self, user_id, movie_id):
        """Helper function which returns one movie"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == int(movie_id):
                return movie

        return 'User or Movie Not Found!'

    def return_movie_name(self, user_id, movie_id):
        """This function returns a movie title queried by its movie id"""
        user_movies = self.get_user_movies(user_id)
        if user_movies == "User ID Not Found":
            return False
        for movie in user_movies:
            if int(movie['id']) == int(movie_id):
                return movie['name']
        return False

    def add_new_user(self, name):
        """Adds a new user to the webapp"""
        data = self.read_file()
        new_user_dict = {
            "id": data[-1]['id'] + 1,
            "name": name,
            "movies": []
        }
        data.append(new_user_dict)
        self.write_file(data)

    def add_movie(self, user_id, movie_name):
        """Adds a new favourite movie for a user"""
        data = self.read_file()
        movie_api_data = self.movie_api(movie_name)

        for user in data:
            if user['id'] == int(user_id):

                if not user['movies']:
                    id_num = 1

                else:
                    id_num = user['movies'][-1]['id'] + 1

                new_movie_dict = {
                    "id": id_num,
                    "name": movie_api_data['Title'],
                    "director": movie_api_data['Director'],
                    "year": movie_api_data['Year'],
                    "rating": movie_api_data['imdbRating'],
                    "poster": movie_api_data['Poster'],
                    "plot": movie_api_data['Plot']
                }
                user['movies'].append(new_movie_dict)
        self.write_file(data)

    def update_movie(self, user_id, movie_id, new_movie_data):
        """Updates key information about a movie"""
        data = self.read_file()
        for user in data:
            if user['id'] == int(user_id):
                #finds which movie to update by using the movie_id to find the index
                for movie in user['movies']:
                    if movie['id'] == int(movie_id):

                        movie['name'] = new_movie_data['name']
                        movie['director'] = new_movie_data['director']
                        movie['rating'] = new_movie_data['rating']
        self.write_file(data)

    def delete_movie(self, user_id, movie_id):
        """Removes a movie from a users favourite movie list"""
        data = self.read_file()
        for user in data:
            if user['id'] == int(user_id):
                for movie in user['movies']:
                    if movie['id'] == int(movie_id):
                        movie_index = user['movies'].index(movie)
                        user['movies'].pop(movie_index)
        self.write_file(data)


if __name__ == '__main__':

    i = JsonDataManager('C:\\Users\\aamoh\\PycharmProjects\\MainProject\\Movie-project-v2\\logs\\movie_data.json')

    movie = i.movie_api('the dark knight')
    print(movie)
