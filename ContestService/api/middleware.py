from corsheaders.middleware import CorsMiddleware


class SyncCorsMiddleware(CorsMiddleware):
    """I don't know why default CORS middleware wasn't working."""

    async_capable = False
