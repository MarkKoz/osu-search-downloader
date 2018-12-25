from typing import Dict

import requests


class OsuClient:
    # TODO: Move to a config file.
    QUERY_ENDPOINT = "https://osusearch.com/query/"

    @staticmethod
    def query_beatmaps(query: Dict[str, str], offset: int) -> requests.Response:
        query["offset"] = offset
        response = requests.get(OsuClient.QUERY_ENDPOINT, params=query)
        response.raise_for_status()  # TODO: Handle raised exceptions.

        return response
