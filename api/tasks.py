from .methods import AhrefsMethods
from settings import BASE_DIR, logger
import os
from datetime import datetime
import dateutil.parser
import pandas as pd


class AhrefsTasks:
    def __init__(self, methods: AhrefsMethods):
        self.methods = AhrefsMethods()
        self.input_files_folder = os.path.join(BASE_DIR, "input_files")
        self.output_files_folder = os.path.join(BASE_DIR, "output_files")

    def load_only_urls(self, filename: str = "urls.txt") -> list:
        file_path = os.path.join(self.input_files_folder, filename)
        with open(f"{file_path}", "r") as file:
            urls = file.read().splitlines()

        self.urls = [url.strip() for url in urls]

        return self.urls

    def load_urls_for_compare(self, filename: str = "urls_for_compare.csv"):
        file_path = os.path.join(self.input_files_folder, filename)

        df = pd.DataFrame(columns=["url", "date"])

        if filename.find(".csv") > -1:
            df = pd.read_csv(file_path, sep=";")

        if filename.find(".xlsx") > -1:
            df = pd.read_excel(file_path)

        return df

    def collect_actual_data_rating(self, urls=None) -> pd.DataFrame:
        if not urls:
            self.load_only_urls()

        data = []
        columns = ["url", "domain_rating", "ahrefs_rank"]

        for url in self.urls:
            response = self.methods.get_domain_rating(target=url)
            domain_rating, ahrefs_rank = self.methods.parse_domain_rating_response(
                response.text
            )
            data.append([url, domain_rating, ahrefs_rank])

        df = pd.DataFrame(data, columns=columns)

        return df

    def parse_url_date(self, date_string):
        try:
            date_object = dateutil.parser.parse(date_string)
            return date_object.strftime("%Y-%m-%d")
        except ValueError:
            print("Неизвестный формат даты:", date_string)
            return None

    def __clean_to_domain(self, url: str) -> str:
        if url.find("/") == -1:
            return url

        if url.find("//") > -1:
            domain = url.split("//")[1].split("/")[0]
            return domain
        else:
            domain = url.split("/")[0]
            return domain

    def compare_data_rating(self, urls=None):
        if not urls:
            urls: list = self.load_urls_for_compare().to_dict("records")

        data = []
        data_dict = {}

        columns = [
            "Domain",
            "Url",
            "Date",
            "DR",
            "AR",
            "CompareDate",
            "DRSecondDate",
            "ARSecondDate",
        ]

        today = datetime.today().strftime("%Y-%m-%d")

        for item in urls:
            url = item.get("url").strip()
            domain = self.__clean_to_domain(url)
            date_to_compare = self.parse_url_date(item.get("date"))
            key = (domain, today)

            if key not in data_dict:
                actual_response = self.methods.get_domain_rating(target=url)

                if actual_response is None:
                    dr = "--"
                    ar = "--"
                else:
                    dr, ar = self.methods.parse_domain_rating_response(
                        actual_response.text
                    )
                data_dict[key] = {"dr": dr, "ar": ar}

                compare_date_response = self.methods.get_domain_rating(
                    target=url, date=date_to_compare
                )

                if compare_date_response is None:
                    compare_dr = "--"
                    compare_ar = "--"

                else:
                    compare_dr, compare_ar = self.methods.parse_domain_rating_response(
                        compare_date_response.text
                    )

                data.append(
                    [
                        domain,
                        url,
                        today,
                        dr,
                        ar,
                        date_to_compare,
                        compare_dr,
                        compare_ar,
                    ]
                )
            else:
                logger.info("Take DR data from history")
                compare_date_response = self.methods.get_domain_rating(
                    target=url, date=date_to_compare
                )
                compare_dr, compare_ar = self.methods.parse_domain_rating_response(
                    compare_date_response.text
                )
                data.append(
                    [
                        domain,
                        url,
                        today,
                        data_dict[key]["dr"],
                        data_dict[key]["ar"],
                        date_to_compare,
                        compare_dr,
                        compare_ar,
                    ]
                )

        df = pd.DataFrame(data, columns=columns)

        return df
