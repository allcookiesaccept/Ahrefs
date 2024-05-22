from api.methods import AhrefsMethods
from api.tasks import AhrefsTasks
import os

# TODO разобраться с датами из будущего после обработки datetime (пока для таких -1 год)
# TODO Дополнить проверку если compared_date уже был, не только на текущую дату


if __name__ == "__main__":
    methods = AhrefsMethods()
    tasks = AhrefsTasks(methods)

    file_name = "domain_ratings_dynamics_from_2024.xlsx"
    file_path = os.path.join(tasks.output_files_folder, file_name)
    df = tasks.compare_data_rating()
    df.to_excel(file_path, index=False)
