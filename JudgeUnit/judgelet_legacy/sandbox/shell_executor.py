"""Abstract from dealing with subprocesses"""

import asyncio
from collections import namedtuple
from typing import Any

from judgelet import settings
from judgelet.encoding import try_to_decode

ShellResult = namedtuple("ShellResult", ["stdout", "stderr", "return_code"])


async def execute_in_shell(
        command: str,
        *,
        proc_input: str = "",
        cwd: str | None = None,
        env: Any | None = None,
        io_encoding: str = settings.IO_ENCODING
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
