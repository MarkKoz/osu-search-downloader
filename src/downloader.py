from argparse import ArgumentParser
from typing import Generator, Union
from urllib.parse import urlparse
import sys

import requests

VERSION = "0.1.0"
QUERY_ENDPOINT = "https://osusearch.com/query"
DOWNLOAD_BASE = "https://osu.ppy.sh/beatmapsets"
DOWNLOAD_SUFFIX = "download?noVideo=1"

def search(query: str, offset: int) -> dict:
    response = requests.get(f"{QUERY_ENDPOINT}/?{query}&offset={offset}")
    response.raise_for_status()  # TODO: Handle raised exceptions.

    return response.json()

def get_download_urls(results: dict) -> Generator[str, None, None]:
    for beatmap in results["beatmaps"]:
        yield f"{DOWNLOAD_BASE}/{beatmap['beatmapset_id']}/{DOWNLOAD_SUFFIX}"

def get_max_offset(results: dict) -> int:
    # Each request returns at most 18 beatmaps. Floor division is used because
    # the count includes offset 0's results and the offset is 0-based.
    return results["result_count"] // 18

def get_all_urls(url: str) -> Generator[str, None, None]:
    query: str = urlparse(url).query

    result: dict = search(query, 0) # Offset 0 has correct result_count.
    max_offset: int = get_max_offset(result)
    yield from get_download_urls(result)

    for offset in range(1, max_offset + 1):
        result = search(query, offset)
        yield from get_download_urls(result)

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
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}")
    args = arg_parser.parse_args()

    # Prints to stdout if a file path isn't specified.
    file = open(args.file_path, "w") if args.file_path else sys.stdout

    for url in get_all_urls(args.url):
        print(url, file=file)

    file.close()
