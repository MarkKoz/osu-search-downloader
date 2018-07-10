from pathlib import Path
from typing import Generator
import re

class BeatmapFilter:
    def __init__(self, songs_path: str):
        self.path: Path = Path(songs_path).resolve(strict=True)

        if not self.path.is_dir():
            raise IsADirectoryError

    def get_existing_ids(self) -> Generator[int, None, None]:
        for beatmap in self.path.iterdir():
            match = re.match(r"(\d+) ", beatmap.name)

            if match:
                yield int(match.group(1))
