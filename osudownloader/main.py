#!/usr/bin/env python
"""osu!search Bulk Downloader

Downloads all beatmaps from osu!search results.
"""

import sys
from argparse import ArgumentParser

import osudownloader as osd
from osudownloader import parsing


def main():
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
        version=f"%(prog)s {osd.__version__}")
    args = arg_parser.parse_args()

    # Prints to stdout if a file path isn't specified.
    file = open(args.file_path, "w") if args.file_path else sys.stdout

    for url in parsing.get_urls(args.url, args.songs_path):
        print(url, file=file)

    file.close()
