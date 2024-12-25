from typing import Any, BinaryIO, Dict

from zstandard import ZstdCompressor


class ZstdPlugin:
    def __init__(self, file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        self.writer = ZstdCompressor().stream_writer(file, closefd=False)

    def write(self, data: bytes) -> int:
        return self.writer.write(data)

    def close(self) -> None:
        self.writer.close()
