"""Identify the narrow set of local avatar source formats."""


def kind(path):
    """Return the decoder kind, rejecting mismatched image extensions."""
    suffix = path.suffix.lower()
    if suffix in (".mp4", ".mov"):
        return "mov"
    with path.open("rb") as stream:
        header = stream.read(8)
    if suffix == ".png" and header == b"\x89PNG\r\n\x1a\n":
        return "png"
    if suffix in (".jpg", ".jpeg") and header.startswith(b"\xff\xd8\xff"):
        return "mjpeg"
    raise ValueError("source must be an MP4, MOV, PNG or JPEG with a matching signature")
