from settings import logger
import json


class ResponseParser:

    @staticmethod
    def parse_best_links_data(response_text: str) -> tuple:

        logger.info("extracting first 50 from best backlinks")

        if response_text is None:
            logger.warning("Response text is None, returning default values")
            return "--", "--"

        try:
            response_to_json = json.loads(response_text)
            backlinks = response_to_json['backlinks']
            return backlinks
        except (ValueError, KeyError):
            logger.warning("Error parsing response text, returning default values")
            return "--", "--"

    @staticmethod
    def parse_domain_rating_response(response_text) -> tuple:
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


    @staticmethod
    def parse_backlink_stats(response_text) -> tuple:
        logger.info("parsing backlinks stats")

        if response_text is None:
            logger.warning("Response text is None, returning default values")
            return "--", "--", "--", "--"
        try:
            response_to_json = json.loads(response_text)
            live = response_to_json["metrics"]["live"]
            all_time = response_to_json["metrics"]["all_time"]
            live_refdomains = response_to_json["metrics"]["live_refdomains"]
            all_time_refdomains = response_to_json["metrics"]["all_time_refdomains"]
            return live, all_time, live_refdomains, all_time_refdomains
        except (ValueError, KeyError):
            logger.warning("Error parsing response text, returning default values")
            return "--", "--", "--", "--"





        try:
            response_to_json = json.loads(response_text)
            backlinks = response_to_json['backlinks']
            return backlinks
        except (ValueError, KeyError):
            logger.warning("Error parsing response text, returning default values")
            return "--", "--"
