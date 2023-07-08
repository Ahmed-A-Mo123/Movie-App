from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    def add_new_user(self, new_user_dict):
        pass



if __name__ == '__main__':
    pass
