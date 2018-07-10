from typing import Generator
from urllib.parse import urlparse

import requests

class Searcher:
    def __init__(self, url: str):
        query: str = urlparse(url).query
        self._request_url: str = f"https://osusearch.com/query/?{query}&offset="

    def _search(self, offset: int) -> dict:
        response = requests.get(f"{self._request_url}{offset}")
        response.raise_for_status()  # TODO: Handle raised exceptions.

        return response.json()

    def get_ids(self) -> Generator[int, None, None]:
        results: dict = self._search(0) # Offset 0 has correct result_count.

        # Each request returns at most 18 beatmaps. Floor division is used
        # because the count includes offset 0's results and offset is 0-based.
        max_offset: int = results["result_count"] // 18

        yield from (m["beatmapset_id"] for m in results["beatmaps"])

        for offset in range(1, max_offset + 1):
            results = self._search(offset)

            yield from (m["beatmapset_id"] for m in results["beatmaps"])
