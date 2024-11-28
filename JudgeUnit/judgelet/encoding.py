def try_to_decode(s: bytes, preferred=None):
    if s is None:
        return None
    try:
        return s.decode(encoding=preferred)
    except UnicodeDecodeError:
        pass
    try:
        return s.decode("cp866")
    except UnicodeDecodeError:
        pass
    try:
        return s.decode("cp1251")
    except UnicodeDecodeError:
        pass
    return s.decode(encoding=preferred, errors="replace")
