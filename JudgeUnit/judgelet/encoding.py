def try_to_decode(s: bytes):
    if s is None:
        return None
    try:
        return s.decode()
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
    return s.decode(errors="replace")
