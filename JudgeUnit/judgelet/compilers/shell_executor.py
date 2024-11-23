import asyncio
from collections import namedtuple
from typing import Any

from judgelet import settings


ShellResult = namedtuple("ShellResult", ["stdout", "stderr", "return_code"])


async def execute_in_shell(
        command: str, *,
        proc_input: str = "",
        timeout: float | None = None,
        cwd: str | None = None,
        env: Any | None = None,
        io_encoding: str = settings.IO_ENCODING
) -> ShellResult:
    proc = await asyncio.create_subprocess_shell(
        command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd, env=env
    )
    proc.stdin.write(proc_input.encode(io_encoding))
    proc.stdin.write_eof()
    proc.stdin.close()
    return_code = await proc.wait()
    stdout = await proc.stdout.read()
    stderr = await proc.stderr.read()
    try:
        proc.terminate()
        proc.kill()
    except ProcessLookupError:
        pass
    return ShellResult(stdout, stderr, return_code)
