from settings import logger
from datetime import datetime


class InputValidator:

    @staticmethod
    def validate_date(date_string):
        try:
            date_object = datetime.strptime(date_string, "%d.%m.%Y")
            current_date = datetime.now()

            if date_object > current_date:
                modified_date_object = date_object.replace(year=date_object.year - 1)
                return modified_date_object.strftime("%Y-%m-%d")
            else:
                return date_object.strftime("%Y-%m-%d")

        except ValueError:
            logger.error("Неизвестный формат даты:", date_string)
            return None

    @staticmethod
    def handle_none_response(response):
        if response is None:
            return "--", "--"
        else:
            return response