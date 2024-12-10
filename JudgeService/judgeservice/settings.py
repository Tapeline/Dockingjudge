"""
JudgeService settings
"""

import logging
import os

JUDGELET_ENDPOINT = "%s/run-suite/"
IO_ENCODING = os.getenv("IO_ENCODING") or "utf-8"
FILE_ENCODING = os.getenv("FILE_ENCODING") or "utf-8"
RMQ_ADDRESS = os.getenv("RMQ_ADDRESS")
RMQ_USER = os.getenv("RMQ_USER")
RMQ_PASSWORD = os.getenv("RMQ_PASSWORD")
CONFIG_PATH = os.getenv("CONFIG_PATH") or "config.yml"

logging.info("Using config on %s", CONFIG_PATH)
