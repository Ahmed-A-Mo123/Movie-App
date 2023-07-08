from logging.manager import DataManagerInterface
import csv


class CsvDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def read_csv_file(self):
        data = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry = next((item for item in data if item["id"] == int(row["id"])), None)
                if entry is None:
                    entry = {
                        "id": int(row["id"]),
                        "name": row["name"],
                        "movies": []
                    }
                    data.append(entry)
                movie = {
                    "id": int(row["movie_id"]),
                    "name": row["movie_name"],
                    "director": row["movie_director"],
                    "year": int(row["movie_year"]),
                    "rating": float(row["movie_rating"])
                }
                entry["movies"].append(movie)
        return data

    def get_all_users(self):
        # Return a list of all users
        return self.read_csv_file()

    def get_user_movies(self, user_id):
        pass
# Return a list of all movies
