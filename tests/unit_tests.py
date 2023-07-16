from datamanager.JsonManager import JsonDataManager
import pytest
import os

data_manager = JsonDataManager(r'C:\Users\aamoh\PycharmProjects\MainProject\Movie-project-v2\logs\movie_data.json')


def test_if_user_exist():
    assert data_manager.check_if_user_exist(0) is True


def test_movie_api_returning_false():
    with pytest.raises(ValueError):
        data_manager.movie_api('Upgfghf')  # If the Api returns empty it shout raise a ValueError.


def test_get_user_movies():
    assert data_manager.get_user_movies(-1) == 'User ID Not Found'


def test_return_movie_name():
    assert data_manager.return_movie_name(-1,2) is False




