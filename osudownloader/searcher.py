from typing import Generator, Optional
from urllib.parse import urlparse

from osu.client import OsuClient
from osu.models import Beatmap, SearchResults


class Searcher:
    def __init__(self, url: str):
        self.query: str = urlparse(url).query

    def _get_results(self, offset: int) -> SearchResults:
        response = OsuClient.query_beatmaps(self.query, offset)
        results: Optional[bytes] = response.content

        return SearchResults.from_json(results)

    def search(self) -> Generator[Beatmap, None, None]:
        # Offset 0 has correct result_count.
        results: SearchResults = self._get_results(0)

        # Each request returns at most 18 beatmaps. Floor division is used
        # because the count includes offset 0's results and offset is 0-based.
        max_offset: int = results.result_count // 18

        yield from results.beatmaps

        for offset in range(1, max_offset + 1):
            results = self._get_results(offset)

            yield from results.beatmaps
