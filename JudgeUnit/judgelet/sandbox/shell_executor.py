import asyncio
from collections import namedtuple
from typing import Any

from judgelet import settings
from judgelet.encoding import try_to_decode

ShellResult = namedtuple("ShellResult", ["stdout", "stderr", "return_code"])


async def execute_in_shell(
        command: str, *,
        proc_input: str = "",
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
    stdout = try_to_decode(await proc.stdout.read(), preferred=io_encoding)
    stderr = try_to_decode(await proc.stderr.read(), preferred=io_encoding)
    try:
        proc.terminate()
        proc.kill()
    except ProcessLookupError:
        pass
    return ShellResult(stdout, stderr, return_code)
