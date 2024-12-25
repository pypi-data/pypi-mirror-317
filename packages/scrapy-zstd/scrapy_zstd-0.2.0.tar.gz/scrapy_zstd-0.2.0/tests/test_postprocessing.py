from io import BytesIO

from zstandard import MAGIC_NUMBER, decompress

from scrapy_zstd.postprocessing import ZstdPlugin


def test_compress_zstd() -> None:
    output_file = BytesIO()

    plugin = ZstdPlugin(output_file, {})
    plugin.write(b"hello")
    plugin.close()

    compressed_data = output_file.getvalue()
    assert int.from_bytes(compressed_data[:4], "little") == MAGIC_NUMBER
    assert decompress(compressed_data, 1024) == b"hello"
