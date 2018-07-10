from pathlib import Path
from typing import FrozenSet, Generator, Optional
import re

from searcher import Searcher

def _get_existing_ids(songs_path: str) -> Generator[int, None, None]:
    path: Path = Path(songs_path).resolve(strict = True)

    if not path.is_dir():
        raise IsADirectoryError

    for beatmap in path.iterdir():
        match = re.match(r"(\d+) ", beatmap.name)

        if match:
            yield int(match.group(1))

def get_urls(url: str, songs_path: Optional[str]) -> Generator[str, None, None]:
    search: Searcher = Searcher(url)
    existing_ids: Optional[FrozenSet[int]] = None
    skip_count: int = 0

    if songs_path:
        existing_ids = frozenset(_get_existing_ids(songs_path))

    for beatmap in search.get_ids():
        if existing_ids and beatmap in existing_ids:
            skip_count += 1
        else:
            yield f"https://osu.ppy.sh/beatmapsets/{beatmap}/download?noVideo=1"
