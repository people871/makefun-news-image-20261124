#!/usr/bin/env python3
"""Tuesday 24 November 2026 in one image: 8 sourced stories, a world map
and a date check.

The entry image lives beside this program as entry.png (a JPEG, kept under
that name as the rules require). This program checks the image is whole and
within the competition limits, then copies its exact bytes to
$MAKEFUN_OUTPUT_DIR/entry.png and re-reads the copy to prove it matches.

No network, no randomness: every run writes the same bytes.
"""
import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
EXPECT_WIDTH = 1024
EXPECT_HEIGHT = 1024


class EntryError(Exception):
    """The image fails a competition rule."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jpeg_dimensions(data: bytes) -> tuple:
    """Walk JPEG segments; return (width, height) from the first SOF frame."""
    if data[:2] != b"\xff\xd8":
        raise EntryError("not a JPEG: missing SOI marker")
    if data[-2:] != b"\xff\xd9":
        raise EntryError("not a whole JPEG: missing EOI marker at the end")
    pos = 2
    saw_dqt = saw_dht = saw_sos = False
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise EntryError(f"bad JPEG marker at offset {pos}")
        marker = data[pos + 1]
        if marker == 0xD9:  # EOI
            break
        if marker == 0xDA:  # SOS: entropy data follows until EOI
            saw_sos = True
            break
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if size < 2 or pos + 2 + size > len(data):
            raise EntryError(f"JPEG segment overruns file at offset {pos}")
        if marker == 0xDB:
            saw_dqt = True
        if marker == 0xC4:
            saw_dht = True
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if size < 7:
                raise EntryError("short JPEG frame header")
            precision = data[pos + 4]
            height = struct.unpack(">H", data[pos + 5:pos + 7])[0]
            width = struct.unpack(">H", data[pos + 7:pos + 9])[0]
            components = data[pos + 9]
            if precision != 8 or not 1 <= components <= 4:
                raise EntryError("unsupported JPEG frame")
            return width, height
        pos += 2 + size
    if not (saw_dqt and saw_dht and saw_sos):
        raise EntryError("JPEG missing DQT, DHT or SOS segment")
    raise EntryError("JPEG has no frame header")


def png_dimensions(data: bytes) -> tuple:
    """Check the PNG signature, IHDR size and the IEND trailer.

    Walks every chunk (length + type + data + CRC) so a truncated file or a
    file with junk after IEND is refused, and requires an IDAT chunk: a PNG
    with a header but no image data is not a whole image.
    """
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise EntryError("not a PNG: bad signature")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise EntryError("PNG missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    pos = 8
    saw_idat = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            raise EntryError(f"PNG chunk {ctype!r} overruns the file")
        if ctype == b"IDAT":
            saw_idat = True
        if ctype == b"IEND":
            if length != 0 or end != len(data):
                raise EntryError("PNG has data after the IEND chunk")
            if not saw_idat:
                raise EntryError("PNG has no image data (no IDAT chunk)")
            return width, height
        pos = end
    raise EntryError("not a whole PNG: missing IEND trailer at the end")


def verify(data: bytes) -> str:
    """Return 'JPEG' or 'PNG' after checking format, wholeness and size."""
    if len(data) > MAX_BYTES:
        raise EntryError(f"image is {len(data)} bytes, over the 1 MiB limit")
    if len(data) < 32:
        raise EntryError("image too small to be a whole image")
    if data[:2] == b"\xff\xd8":
        kind = "JPEG"
        width, height = jpeg_dimensions(data)
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "PNG"
        width, height = png_dimensions(data)
    else:
        raise EntryError("image is neither JPEG nor PNG")
    if (width, height) != (EXPECT_WIDTH, EXPECT_HEIGHT):
        raise EntryError(
            f"image is {width}x{height}, must be {EXPECT_WIDTH}x{EXPECT_HEIGHT}"
        )
    return kind


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"

    raw = SOURCE.read_bytes()
    kind = verify(raw)
    digest = sha256_hex(raw)

    target.write_bytes(raw)
    again = target.read_bytes()
    if len(again) != len(raw) or sha256_hex(again) != digest:
        raise EntryError("output copy does not match the verified source")
    # Re-run the whole gate on the copy, so a disk or write fault is caught
    # by the same checks that cleared the source.
    if verify(again) != kind:
        raise EntryError("output copy fails the image gate on re-check")

    print(
        f"entry: wrote {target}: {kind} {EXPECT_WIDTH}x{EXPECT_HEIGHT}, "
        f"{len(raw)} bytes, sha256 {digest}"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except EntryError as exc:
        print(f"entry: FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
