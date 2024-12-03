"""Utils for dealing with encoding."""


def try_to_decode(string: bytes, preferred: str | None = None):
    """
    Try different encoding to somehow decode a string
    on a Windows machine

    Args:
        string: decoding target
        preferred: preferred encoding
    Returns:
        *hopefully* decoded string
    """
    if string is None:
        return None
    try:
        return string.decode(encoding=preferred)
    except UnicodeDecodeError:
        pass  # noqa: WPS420 (wrong keyword)
    try:
        return string.decode("cp866")
    except UnicodeDecodeError:
        pass  # noqa: WPS420 (wrong keyword)
    try:
        return string.decode("cp1251")
    except UnicodeDecodeError:
        pass  # noqa: WPS420 (wrong keyword)
    return string.decode(encoding=preferred, errors="replace")
