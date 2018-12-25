import re
from pathlib import Path
from typing import Generator, Optional

from osudownloader import Searcher

# TODO: Move to a config file.
DOWNLOAD_URL = "https://osu.ppy.sh/beatmapsets/{id}/download?noVideo=1"


def _get_existing_ids(songs_path: str) -> Generator[int, None, None]:
    path = Path(songs_path).resolve(strict=True)

    if not path.is_dir():
        raise NotADirectoryError

    for beatmap in path.iterdir():
        match = re.match(r"(\d+) ", beatmap.name)

        if match:
            yield int(match.group(1))


def get_urls(url: str, songs_path: Optional[str]) -> Generator[str, None, None]:
    searcher = Searcher(url)
    existing_ids = None
    skip_count: int = 0

    if songs_path:
        existing_ids = frozenset(_get_existing_ids(songs_path))

    for beatmap in searcher.search():
        if existing_ids and beatmap.id in existing_ids:
            skip_count += 1
        else:
            yield DOWNLOAD_URL.format(id=beatmap.id)
