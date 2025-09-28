def try_to_decode(
    string: bytes | str | None,
    preferred: str | None = None,
) -> str:
    """
    Try different encoding to somehow decode a string on a Windows machine.

    Args:
        string: decoding target
        preferred: preferred encoding

    Returns:
        *hopefully* decoded string

    """
    # wtf is this function...
    if string is None:
        return ""
    if isinstance(string, str):
        return string
    try:
        if preferred:
            return string.decode(encoding=preferred)
        return string.decode()
    except UnicodeDecodeError:
        pass
    try:
        return string.decode("cp866")
    except UnicodeDecodeError:
        pass
    try:
        return string.decode("cp1251")
    except UnicodeDecodeError:
        pass
    if preferred:
        return string.decode(encoding=preferred, errors="replace")
    return string.decode(errors="replace")
