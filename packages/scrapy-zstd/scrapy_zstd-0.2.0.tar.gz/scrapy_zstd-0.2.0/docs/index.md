# scrapy-zstd

`scrapy-zstd` is a Scrapy plugin that provides support for compressing feed exports using the [Zstandard (zstd) compression algorithm]((https://datatracker.ietf.org/doc/html/rfc8878)). This extension allows you to efficiently compress your Scrapy feed exports, reducing the storage space required and potentially improving the speed of data transfer.

## Installation

`scrapy-zstd` is available on [PyPI](https://pypi.org/project/scrapy-zstd/) and can be installed with pip.

```
pip install scrapy-zstd
```

## Usage

To use `scrapy-zstd`, add `scrapy_zstd.postprocessing.ZstdPlugin` to the `postprocessing` list in your `FEEDS` configuration.

Here is an example configuration:

```
FEEDS = {
    "/path/to/file.csv.zst": {
        "format": "csv",
        "postprocessing": ["scrapy_zstd.postprocessing.ZstdPlugin"],
    }
}
```
