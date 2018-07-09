# osu!search Bulk Downloader
### Description
Downloads all beatmaps from search results from osu!search.

Currently limited to fetching beatmap download links and printing them or
writing them to a file.

### Requirements
#### Binaries
* [Python 3.6](https://www.python.org/downloads/) or higher
    * Make sure the python directory and python/Scripts directory are in your
    system's `PATH` environment variable.

#### Packages
> **Note** `pipenv` can install these automatically from the provided pipfiles.

* [requests](http://docs.python-requests.org/en/master/)
* `OPTIONAL` [pipenv](https://docs.pipenv.org/)

### Installation
Download the program from
[releases](https://github.com/MarkKoz/osu-search-downloader/releases) and
extract the archive. For the latest features, instead clone the repository or
download the ZIP.

[pipenv](https://docs.pipenv.org/) can be used to simplify the installation
process. Once it is installed, `cd` into the root directory and install the
dependencies from the pipfile with

```bash
pipenv install
```

Alternatively, the required packages can be installed with [pip](https://pip.pypa.io/en/stable/quickstart/).

### Basic Usage
Run `downloader.py` to run the program. If using pipenv:

```bash
pipenv shell
cd src
python downloader.py "https://osusearch.com/search/"
```

otherwise

```bash
python downloader.py "https://osusearch.com/search/"
```

For more detailed usage, see help with the `-h` flag.
