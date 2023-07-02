from logging.manager import DataManagerInterface
import csv


class CsvDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename


    def read_csv_file(self):
        """Reads the file and turns the csv file into a dictionary by going row by row and creating a dictionary out of
        it"""
        movies_dict = {}
        outer_movie_list = []
        movie_list = []
        list_of_ids = []
        with open(self.filename, 'r') as fileobj:
            csv_reader = csv.DictReader(fileobj)
            for row in csv_reader:
                list_of_ids.append(row['id'])
                if row['id'] not in list_of_ids:
                    outer_movie_dict = {'id': 'asdfasdf', 'name': row['name']}
                    outer_movie_list.append(outer_movie_dict)
                inner_movie_dict = {'movie_id': int(row["movie_id"]),
                                    'movie_name': row['movie_name'],
                                    'movie_director': row['movie_director'],
                                    'movie_year': int(row['movie_year']),
                                    'movie_rating': float(row['movie_rating'])
                                    }

            return outer_movie_list

    def get_all_users(self):
        # Return a list of all users
        pass

    def get_user_movies(self, user_id):
        pass
# Return a list of all movies
