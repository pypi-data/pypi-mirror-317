# scrapy-zstd

A Scrapy plugin to compress feeds with [Zstandard (zstd)](https://datatracker.ietf.org/doc/html/rfc8878).

## Installation

```
pip install scrapy-zstd
```

## Usage

Add `scrapy_zstd.postprocessing.ZstdPlugin` to the `postprocessing` list in the `FEEDS` configurations.

```
FEEDS = {
    "/path/to/file.csv.zst": {
        "format": "csv",
        "postprocessing": ["scrapy_zstd.postprocessing.ZstdPlugin"],
    }
}
```
