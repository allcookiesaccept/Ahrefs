from api.methods import AhrefsMethods
from api.tasks import AhrefsTasks
import os
from settings import DataManager



dm = DataManager.get_instance()
TOKEN = dm.token


# TODO Дополнить проверку если compared_date уже был


if __name__ == "__main__":
    methods = AhrefsMethods(TOKEN)
    tasks = AhrefsTasks(methods)

    file_name = "domain_ratings_dynamics_from_2024.xlsx"
    file_path = os.path.join(tasks.output_files_folder, file_name)
    df = tasks.compare_data_rating()
    df.to_excel(file_path, index=False)
