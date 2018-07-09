from argparse import ArgumentParser
from urllib.parse import urlparse
import math
import requests
import sys

def get_download_urls(query: str, offset: int):
    response = requests.get(f"https://osusearch.com/query/?{query}&offset={offset}")
    response.raise_for_status() # Raises an exception if unsuccessful. TODO: Handle exceptions.
    data = req.json()

    if offset == 0:
        yield int(data["result_count"])

    for beatmap in data["beatmaps"]:
        yield f"https://osu.ppy.sh/beatmapsets/{beatmap['beatmapset_id']}/download?noVideo=1"

def get_all_urls(url: str):
    query = urlparse(url).query

    first_resp = get_download_urls(query, 0) # Offset 0 yields result_count first.
    max_offset = math.ceil(next(first_resp) / 18) # Each request returns at most 18 beatmaps.

    yield from first_resp # The remainder of the generator contains the urls.

    for offset in range(1, max_offset + 1):
        yield from get_download_urls(query, offset)

if __name__ == "__main__":
    version = "0.1.0"

    arg_parser = ArgumentParser(
        prog="osu!search Bulk Downloader",
        description="Downloads all beatmaps from search results from osu!search.")
    arg_parser.add_argument("url", help="The URL to the osu!search results.")
    arg_parser.add_argument(
        "-o", "--out",
        dest="file_path",
        help="Path to a file to create and to which to write the download URLs.")
    arg_parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version}")
    args = arg_parser.parse_args()

    # Prints to stdout if a file path isn't specified.
    file = open(args.file_path, "w") if args.file_path else sys.stdout

    for url in get_all_urls(args.url):
        print(url, file=file)

    file.close()
