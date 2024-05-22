from api.methods import AhrefsMethods
from api.tasks import AhrefsTasks
import os

if __name__ == '__main__':

    methods = AhrefsMethods()
    tasks = AhrefsTasks(methods)

    file_name = "domain_ratings_dynamics.xlsx"
    file_path = os.path.join(tasks.output_files_folder, file_name)
    df = tasks.compare_data_rating()
    df.to_excel(file_path, index=False)