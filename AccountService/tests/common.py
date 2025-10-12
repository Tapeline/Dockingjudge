def api(*url: str) -> str:
    assembled = "/api/v1/accounts/" + "/".join(url).strip("/")
    if assembled.endswith("/"):
        return assembled
    return f"{assembled}/"
