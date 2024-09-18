import os
import pandas as pd
from settings import BASE_DIR
class DataLoader:
    def __init__(self):
        self.input_files_folder = os.path.join(BASE_DIR, "input_files")

    def load_urls(self, filename: str = "urls.txt") -> list:
        file_path = os.path.join(self.input_files_folder, filename)
        with open(file_path, "r") as file:
            urls = file.read().splitlines()
        return [url.strip() for url in urls]

    def load_urls_with_date(self, filename: str = "urls_for_compare.csv") -> pd.DataFrame:
        file_path = os.path.join(self.input_files_folder, filename)
        if filename.endswith(".csv"):
            return pd.read_csv(file_path, sep=";")
        elif filename.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")

