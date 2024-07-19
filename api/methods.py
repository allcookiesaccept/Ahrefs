from settings import logger
import requests, json
from datetime import datetime


class AhrefsMethods:
    def __init__(self, token) -> None:
        self.token = token
        self.headers = {
            "Accept": "application/json, application/xml",
            "Authorization": f"Bearer {self.token}",
        }

    def _logger_info(self, endpoint, params):
        target = params.get("target", "")
        if target != "":
            logger.info(f"Api {endpoint}\nTarget: {target}")
        else:
            logger.info(f"Request {endpoint} api")

    def _send_request(self, endpoint, params) -> requests.models.Response:
        self._logger_info(endpoint, params)

        if 'where' in params:
            params['where'] = json.dumps(params['where'])

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error: {e}")
            return None
        else:
            return response

    def get_best_links_data(self, **kwargs):
        endpoint = "https://api.ahrefs.com/v3/site-explorer/all-backlinks"

        params = {
            "target": kwargs.get("target", "legalbet.by"),
            "aggregation": kwargs.get("aggregation", "1_per_domain"),
            "history": kwargs.get("history", "live"),
            "mode": "domain",
            "where": {
                "and": [
                    {"field": "is_content", "is": ["eq", True]},
                    {"field": "links_external", "is": ["lte", 100]},
                    {"field": "is_dofollow", "is": ["eq", True]},
                    {"field": "is_text", "is": ["eq", True]},
                    {"field": "traffic_domain", "is": ["gte", 1000]},
                    {"field": "link_type", "is": ["eq", "text"]},
                    {"field": "is_redirect", "is": ["eq", False]}
                ],
                "not": [
                    {"field": "name_source", "is": ["phrase_match", "legalbet"]}
                ]
            },
            "select": kwargs.get("select", "domain_rating_source,traffic_domain,link_type,is_dofollow,anchor,name_source,title"),
        }
        return self._send_request(endpoint, params)


    def get_domain_rating(self, **kwargs) -> requests.models.Response:
        endpoint = "https://api.ahrefs.com/v3/site-explorer/domain-rating"
        params = {
            "output": kwargs.get("output", "json"),
            "protocol": kwargs.get("protocol", "both"),
            "date": kwargs.get("date", datetime.today()),
            "target": kwargs.get("target", "https://ahrefs.com/"),
        }

        return self._send_request(endpoint, params)

    def parse_domain_rating_response(self, response_text) -> tuple:
        logger.info("parsing domain rating")

        if response_text is None:
            logger.warning("Response text is None, returning default values")
            return "--", "--"

        try:
            response_to_json = json.loads(response_text)
            domain_rating = response_to_json["domain_rating"]["domain_rating"]
            ahrefs_rank = response_to_json["domain_rating"]["ahrefs_rank"]
            return domain_rating, ahrefs_rank
        except (ValueError, KeyError):
            logger.warning("Error parsing response text, returning default values")
            return "--", "--"

    def get_backlinks_stats(self, **kwargs):
        endpoint = "https://api.ahrefs.com/v3/site-explorer/backlinks-stats"

        params = {
            "mode": kwargs.get("mode", "exact"),
            "output": kwargs.get("output", "json"),
            "protocol": kwargs.get("protocol", "both"),
            "date": kwargs.get("date", datetime.today()),
            "target": kwargs.get("target", "https://ahrefs.com/"),
        }

        return self._send_request(endpoint, params)

    def parse_backlink_stats(self, response_text) -> tuple:
        logger.info("parsing backlinks stats")
        response_to_json = json.loads(response_text)
        live = response_to_json["metrics"]["live"]
        all_time = response_to_json["metrics"]["all_time"]
        live_refdomains = response_to_json["metrics"]["live_refdomains"]
        all_time_refdomains = response_to_json["metrics"]["all_time_refdomains"]

        return live, all_time, live_refdomains, all_time_refdomains


    def get_all_backlinks(self, **kwargs):
        ...


"""
from settings import DataManager
dm = DataManager.get_instance()
from api.methods import AhrefsMethods
a = AhrefsMethods(dm.token)
res = a.get_best_links_data()
"""