import os
import sqlite3
import sys

# Ensure paths are resolvable on local file system

REPLACE_FROM = "/app"
_pos = os.getcwd().find("JudgeUnit") + len("JudgeUnit")
REPLACE_TO = os.getcwd()[:_pos]

covdb = sqlite3.connect(sys.argv[1])
cur = covdb.cursor()
cur.execute(
    f"""
    UPDATE file
    SET path = SUBSTR(path, 1, INSTR('{REPLACE_FROM}', path) - 1) || '{REPLACE_TO}' || SUBSTR(path, INSTR('{REPLACE_FROM}', path) + 1 + {len(REPLACE_FROM)})
    WHERE path LIKE "{REPLACE_FROM}%";
    """
)
covdb.commit()
covdb.close()
