import os


def api_url(url):
    if os.getenv("JUDGELET_URL") is not None:
        jl_url = os.getenv("JUDGELET_URL")
        if not jl_url.startswith("http://"):
            jl_url = f"http://{jl_url}"
        if not jl_url.endswith("/"):
            jl_url += "/"
        return jl_url + url
    return f"http://localhost:8000/{url}"
