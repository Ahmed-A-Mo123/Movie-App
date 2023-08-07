from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def check_if_user_exist(self, user_id):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_new_user(self, new_user_dict):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_name):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, new_movie_data):
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        pass

if __name__ == '__main__':
    pass
