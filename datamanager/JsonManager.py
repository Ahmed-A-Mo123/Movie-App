from datamanager.manager import DataManagerInterface
import json
import os


class JsonDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        """ Helper Function Which Only Reads The Contents Of The File Given"""
        with open(self.filename, 'r') as fileobj:
            data = json.load(fileobj)
            return data

    def get_all_users(self):
        """Return a list of all users and the movies they watch"""
        data = self.read_file()
        return data

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        users = self.read_file()
        for user in users:
            if user['id'] == int(user_id):
                return user['movies']
        return "User ID Not Found"

    def add_new_user(self, name):
        data = self.read_file()
        new_user_dict = {
            "id": data[-1]['id'] + 1,
            "name": name,
            "movies": []
        }
        data.append(new_user_dict)
        with open(self.filename, 'w') as fileobj:
            json.dump(data, fileobj)




