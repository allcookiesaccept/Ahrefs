from api.methods import AhrefsMethods
from api.tasks import AhrefsTasks


if __name__ == '__main__':
    methods = AhrefsMethods()
    tasks = AhrefsTasks(methods)

    tasks.load_urls_for_compare()