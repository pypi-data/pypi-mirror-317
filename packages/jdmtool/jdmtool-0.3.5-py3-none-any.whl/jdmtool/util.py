from typing import BinaryIO, Callable, Tuple
import zlib


CHUNK_SIZE = 0x8000


def copy_zlib_compressed(src_fd: BinaryIO, dest_fd: BinaryIO, progress_cb: Callable[[int], None]) -> Tuple[int, int]:
    obj = zlib.compressobj()

    orig_size = compressed_size = 0
    while True:
        block = src_fd.read(CHUNK_SIZE)
        if not block:
            break

        compressed_block = obj.compress(block)
        dest_fd.write(compressed_block)
        compressed_size += len(compressed_block)

        orig_size += len(block)
        progress_cb(len(block))

    compressed_block = obj.flush()
    dest_fd.write(compressed_block)
    compressed_size += len(compressed_block)

    return orig_size, compressed_size
