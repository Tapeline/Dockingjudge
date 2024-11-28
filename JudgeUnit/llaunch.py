import os
import subprocess
import sys
import time
from threading import Thread
from typing import Final

import psutil


MEMORY_LIMIT_EXIT_CODE: Final[int] = 170
TIMEOUT_EXIT_CODE: Final[int] = 171


process: subprocess.Popen | None = None
_return_code = None


def _will_terminate_by_timeout(time_limit_s: float) -> bool:
    try:
        proc = psutil.Process(process.pid)
        elapsed = time.time() - proc.create_time()
        return elapsed > time_limit_s
    except psutil.NoSuchProcess:
        return False


def _will_terminate_by_memory_limit(mem_limit_bytes: int) -> bool:
    try:
        proc = psutil.Process(process.pid)
        mem_bytes = proc.memory_info().rss
        return mem_bytes > mem_limit_bytes
    except psutil.NoSuchProcess:
        return False


def _kill_process():
    process.kill()


def _checker(target,
             time_limit_s: float,
             mem_limit_mb: float):
    global _return_code, process
    mem_limit_bytes = int(mem_limit_mb * 1024 * 1024)
    process = subprocess.Popen(
        target,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    while process.poll() is None:
        if _will_terminate_by_timeout(time_limit_s):
            _kill_process()
            _return_code = TIMEOUT_EXIT_CODE
            if os.getenv("LLAUNCH_MESSAGES") == "1":
                print("TL")
            return
        if _will_terminate_by_memory_limit(mem_limit_bytes):
            _kill_process()
            _return_code = MEMORY_LIMIT_EXIT_CODE
            if os.getenv("LLAUNCH_MESSAGES") == "1":
                print("ML")
            return
    _return_code = process.returncode


def _get_args() -> tuple[float, float, str]:
    time_limit, mem_limit, target = sys.argv[1:]
    return float(time_limit), float(mem_limit), target


def main():
    time_limit, mem_limit, target = _get_args()
    watch_thread = Thread(name="Watcher thread",
                          target=_checker,
                          args=(target, time_limit, mem_limit))
    watch_thread.start()
    watch_thread.join()
    return _return_code


if __name__ == '__main__':
    exit(main())
