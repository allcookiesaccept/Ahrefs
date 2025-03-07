from settings import logger
import requests, json
from datetime import datetime


class Methods:
    def __init__(self, token) -> None:
        self.token = token
        self.headers = {
            "Accept": "application/json, application/xml",
            "Authorization": f"Bearer {self.token}",
        }

    def __method_logger_info(self, endpoint, params):
        target = params.get("target", "")
        if target != "":
            logger.info(f"Api {endpoint}\nTarget: {target}")
        else:
            logger.info(f"Request {endpoint} api")

    def _send_request(self, endpoint, params) -> requests.models.Response:
        self.__method_logger_info(endpoint, params)

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
            "target": kwargs.get("target", "https://ahrefs.com/"),
            "aggregation": kwargs.get("aggregation", "1_per_domain"),
            "history": kwargs.get("history", "live"),
            "limit": kwargs.get("limit", 50),
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
                ]
            },
            "select": kwargs.get("select", "name_source,domain_rating_source,traffic_domain,link_type,is_dofollow,title,snippet_left,anchor,snippet_right,url_to"),


        }
        return self._send_request(endpoint, params)


    def get_best_refdomains_data(self, **kwargs):
        endpoint = "https://api.ahrefs.com/v3/site-explorer/refdomains"

        params = {
            "target": kwargs.get("target", "https://ahrefs.com/"),
            "aggregation": kwargs.get("aggregation", "1_per_domain"),
            "history": kwargs.get("history", "live"),

            "mode": "domain",
            "where": {
                "and": [
                    {"field": "is_content", "is": ["eq", True]},
                    {"field": "links_external", "is": ["lte", 100]},
                    {"field": "is_dofollow", "is": ["eq", True]},
                    {"field": "traffic_domain", "is": ["gte", 1000]},
                    {"field": "link_type", "is": ["eq", "text"]},
                ]
            },
            "select": kwargs.get("select", "domain_rating,dofollow_links,links_to_target,lost_links"),
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

    def get_pages_by_traffic(self, **kwargs):
        endpoint = "https://api.ahrefs.com/v3/site-explorer/pages-by-traffic"

        params = {
            "mode": kwargs.get("mode", "exact"),
            "output": kwargs.get("output", "json"),
            "protocol": kwargs.get("protocol", "both"),
            "country": kwargs.get("country", "by"),
            "target": kwargs.get("target", "https://ahrefs.com/"),

        }

        return self._send_request(endpoint, params)
