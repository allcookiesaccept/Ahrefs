from api.methods import Methods
from api.parser import ResponseParser
from api.tasks import BusinessTask
from api.data_loader import DataLoader
import os
from settings import DataManager

dm = DataManager.get_instance()
TOKEN = dm.token

class Ahrefs:

    def __init__(self, token=TOKEN):
        self.data_loader = DataLoader()
        self.methods = Methods(token)
        self.parser = ResponseParser()
        self.tasks = BusinessTask(self.methods, self.data_loader, self.parser)

    def __call__(self, *args, **kwargs):
        return self



if __name__ == "__main__":

    ahrefs = Ahrefs()
    file_name = "satellites.xlsx"
    file_path = os.path.join(ahrefs.tasks.output_files_folder, file_name)
    df = ahrefs.tasks.compare_data_rating()
    df.to_excel(file_path, index=False)
