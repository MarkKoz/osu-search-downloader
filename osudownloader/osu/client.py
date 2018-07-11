import requests

class OsuClient:
    # TODO: Move to a config file.
    QUERY_ENDPOINT: str = "https://osusearch.com/query/?{query}&offset={offset}"

    @staticmethod
    def query_beatmaps(query: str, offset: int) -> requests.Response:
        url: str = OsuClient.QUERY_ENDPOINT.format(query=query, offset=offset)
        response: requests.Response = requests.get(url)
        response.raise_for_status() # TODO: Handle raised exceptions.

        return response
