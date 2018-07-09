from argparse import ArgumentParser
from urllib.parse import urlparse
import math
import requests
import sys

VERSION = "0.1.0"
QUERY_ENDPOINT = "https://osusearch.com/query"
DOWNLOAD_BASE = "https://osu.ppy.sh/beatmapsets"

def get_download_urls(query: str, offset: int):
    response = requests.get(f"{QUERY_ENDPOINT}/?{query}&offset={offset}")
    response.raise_for_status() # TODO: Handle raised exceptions.
    data = response.json()

    if offset == 0:
        yield int(data["result_count"])

    for beatmap in data["beatmaps"]:
        yield f"{DOWNLOAD_BASE}/{beatmap['beatmapset_id']}/download?noVideo=1"

def get_all_urls(url: str):
    query = urlparse(url).query

    # Offset 0 yields result_count first.
    first_resp = get_download_urls(query, 0)

    # Each request returns at most 18 beatmaps.
    max_offset = math.ceil(next(first_resp) / 18)

    yield from first_resp # The remainder of the generator contains the urls.

    for offset in range(1, max_offset + 1):
        yield from get_download_urls(query, offset)

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
