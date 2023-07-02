from logging.JsonManager import JsonDataManager
from logging.CsvManager import CsvDataManager


ahmed = CsvDataManager("logs\\movie_data.csv")

print(ahmed.read_csv_file())