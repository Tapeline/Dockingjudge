import os


JUDGELET_ENDPOINT = "%s/run-suite/"
IO_ENCODING = os.getenv("IO_ENCODING") if "IO_ENCODING" in os.environ else "utf-8"
RMQ_ADDRESS = os.getenv("RMQ_ADDRESS")
RMQ_USER = os.getenv("RMQ_USER")
RMQ_PASSWORD = os.getenv("RMQ_PASSWORD")
