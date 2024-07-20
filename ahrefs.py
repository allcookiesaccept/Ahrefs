from api.methods import AhrefsMethods
from api.tasks import AhrefsTasks
import os
from settings import DataManager

dm = DataManager.get_instance()
TOKEN = dm.token

class Ahrefs:

    def __init__(self, token=TOKEN):
        self.methods = AhrefsMethods(token)
        self.tasks = AhrefsTasks(self.methods)


if __name__ == "__main__":

    ahrefs = Ahrefs()
    file_name = "satellites.xlsx"
    file_path = os.path.join(ahrefs.tasks.output_files_folder, file_name)
    df = ahrefs.tasks.compare_data_rating()
    df.to_excel(file_path, index=False)
