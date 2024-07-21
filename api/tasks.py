from .methods import Methods
from .parser import ResponseParser
from settings import BASE_DIR, logger
import os
from datetime import datetime
import dateutil.parser
import pandas as pd
from .validator import InputValidator
from collections import defaultdict
from .data_loader import DataLoader


from abc import ABC, abstractmethod


class Task(ABC):
    def __init__(
        self,
        methods: Methods = Methods,
        data_loader: DataLoader = DataLoader,
        parser: ResponseParser = ResponseParser,
    ):
        self.methods = methods
        self.data_loader = data_loader
        self.parser = parser

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @staticmethod
    def _clean_to_domain(url: str) -> str:
        if "//" in url:
            return url.split("//")[1].split("/")[0]
        return url.split("/")[0]


class BusinessTask:
    def __init__(
        self, methods: Methods, data_loader: DataLoader, parser: ResponseParser
    ):
        self.methods = methods
        self.data_loader = data_loader
        self.parser = parser
        self.tasks = {
            "date_comparison": DateComparisonTask(methods, data_loader, parser),
            "actual_data_rating": ActualDataRating(methods, data_loader, parser),
            "best_links_check": BestLinksTask(methods, data_loader, parser),
        }

    def execute_task(self, task_name, *args, **kwargs):
        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")
        return self.tasks[task_name].execute(*args, **kwargs)


class BestLinksTask(Task):
    def execute(self, urls=None):
        if not urls:
            urls: list = self.data_loader.load_urls()

        data = []
        columns = ["domain", "limit50response", ">=50"]

        for url in urls:
            response = self.methods.get_best_links_data(target=url)
            backlinks = self.parser.parse_best_links_data(response.text)
            data.append([url, len(backlinks), len(backlinks) >= 50])

        df = pd.DataFrame(data, columns=columns)

        return df


class DateComparisonTask(Task):
    def execute(self, urls=None):
        if not urls:
            urls: list = self.data_loader.load_urls_with_date().to_dict("records")

        data = []
        data_dict = defaultdict(dict)
        today = datetime.today().strftime("%Y-%m-%d")

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

        for item in urls:
            url = item.get("url").strip()
            domain = self._clean_to_domain(url)
            date_to_compare = InputValidator.validate_date(item.get("date"))
            key = (domain, today)

            if key not in data_dict:
                actual_response = self.methods.get_domain_rating(target=domain)
                if actual_response is None:
                    dr = "--"
                    ar = "--"
                else:
                    dr, ar = self.parser.parse_domain_rating_response(
                        actual_response.text
                    )
                data_dict[key] = {"dr": dr, "ar": ar}

                compare_date_response = self.methods.get_domain_rating(
                    target=domain, date=date_to_compare
                )

                if compare_date_response is None:
                    compare_dr = "--"
                    compare_ar = "--"

                else:
                    compare_dr, compare_ar = self.parser.parse_domain_rating_response(
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
                    target=domain, date=date_to_compare
                )
                if compare_date_response is None:
                    compare_dr = "--"
                    compare_ar = "--"
                else:
                    compare_dr, compare_ar = self.parser.parse_domain_rating_response(
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


class ActualDataRating(Task):
    def execute(self, urls=None) -> pd.DataFrame:
        if not urls:
            urls = self.data_loader.load_urls()

        data = []
        columns = ["url", "domain_rating", "ahrefs_rank"]

        for url in urls:
            response = self.methods.get_domain_rating(target=url)
            domain_rating, ahrefs_rank = self.parser.parse_domain_rating_response(
                response.text
            )
            data.append([url, domain_rating, ahrefs_rank])

        df = pd.DataFrame(data, columns=columns)

        return df
