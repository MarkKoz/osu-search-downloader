from argparse import ArgumentParser
from typing import FrozenSet, Generator, Optional
import sys

from beatmap_filter import BeatmapFilter
from searcher import Searcher

VERSION = "0.2.0"

def get_urls(url: str, songs_path: Optional[str]) -> Generator[str, None, None]:
    search: Searcher = Searcher(url)
    existing_ids: Optional[FrozenSet[int]] = None
    skip_count: int = 0

    if songs_path:
        existing_ids = frozenset(BeatmapFilter(songs_path).get_existing_ids())

    for beatmap in search.get_ids():
        if existing_ids and beatmap in existing_ids:
            skip_count += 1
        else:
            yield f"https://osu.ppy.sh/beatmapsets/{beatmap}/download?noVideo=1"

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        prog="osu!search Bulk Downloader",
        description="Downloads all beatmaps from osu!search results.")
    arg_parser.add_argument("url", help="The URL to the osu!search results.")
    arg_parser.add_argument(
        "-o", "--out",
        dest="file_path",
        help="Path to a file to create and to which to write the URLs.")
    arg_parser.add_argument(
        "-s", "--songs-path",
        dest="songs_path",
        help="Path to osu!'s 'Songs' directory. If specified, existing "
             "beatmaps won't be downloaded.")
    arg_parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}")
    args = arg_parser.parse_args()

    # Prints to stdout if a file path isn't specified.
    file = open(args.file_path, "w") if args.file_path else sys.stdout

    for url in get_urls(args.url, args.songs_path):
        print(url, file=file)

    file.close()
