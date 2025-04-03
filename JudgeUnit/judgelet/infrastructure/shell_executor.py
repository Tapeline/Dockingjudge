"""Abstract from dealing with subprocesses."""

import asyncio
import os
import subprocess
import sys
from typing import Any, Final

from attrs import frozen

from judgelet.infrastructure.encoding import try_to_decode


@frozen
class ShellResult:
    stdout: str
    stderr: str
    return_code: int


MEMORY_LIMIT_EXIT_CODE: Final = 170
TIMEOUT_EXIT_CODE: Final = 171


async def execute_in_shell(
        command: str,
        *,
        proc_input: str = "",
        cwd: str | None = None,
        env: Any | None = None,
        io_encoding: str | None = "utf-8"
) -> ShellResult:
    """
    Execute command in shell as an asyncio subprocess
    Args:
        command: target command
        proc_input: stdin for process
        cwd: working directory for process
        env: environment dict
        io_encoding: stdin, stdout, stderr encoding
    Returns:
        return code, decoded stdout and stderr
    """
    if not io_encoding:
        io_encoding = "utf-8"
    if True:  # TODO: fix async shell
        return _execute_in_sync_shell(
            command,
            proc_input=proc_input, cwd=cwd, env=env, io_encoding=io_encoding
        )
    return await _execute_in_async_shell(
        command,
        proc_input=proc_input, cwd=cwd, env=env, io_encoding=io_encoding
    )


async def _execute_in_async_shell(
        command: str,
        *,
        proc_input: str = "",
        cwd: str | None = None,
        env: Any | None = None,
        io_encoding: str = "utf-8"
) -> ShellResult:
    proc = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env
    )
    proc.stdin.write(proc_input.encode(io_encoding))
    proc.stdin.write_eof()
    proc.stdin.close()
    return_code = await proc.wait()
    stdout = try_to_decode(await proc.stdout.read(), preferred=io_encoding)
    stderr = try_to_decode(await proc.stderr.read(), preferred=io_encoding)
    try:  # noqa: WPS229 (too long try)
        proc.terminate()
        proc.kill()
    except ProcessLookupError:
        pass  # noqa: WPS420 (ignore)
    return ShellResult(stdout, stderr, return_code)


def _execute_in_sync_shell(
        command: str,
        *,
        proc_input: str = "",
        cwd: str | None = None,
        env: Any | None = None,
        io_encoding: str = "utf-8"
) -> ShellResult:
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        env=os.environ | (env or {}),
        shell=sys.platform != "win32"
    )
    stdout, stderr = proc.communicate(proc_input.encode(io_encoding))
    stdout = try_to_decode(stdout, preferred=io_encoding)
    stderr = try_to_decode(stderr, preferred=io_encoding)
    try:  # noqa: WPS229 (too long try)
        proc.terminate()
        proc.kill()
    except ProcessLookupError:
        pass  # noqa: WPS420 (ignore)
    return ShellResult(stdout, stderr, proc.returncode)
