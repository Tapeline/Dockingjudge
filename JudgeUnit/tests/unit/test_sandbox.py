import os.path
import shutil
from pathlib import Path

from judgelet.sandbox.sandbox import Sandbox


class SandboxWrapper:
    def __init__(self, directory):
        self.directory = directory
        self.sandbox: Sandbox | None = None

    def __enter__(self):
        Path(self.directory).mkdir(exist_ok=True)
        self.sandbox = Sandbox("_test_sandbox")
        shutil.copy("llaunch.py", "_test_sandbox/llaunch.py")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sandbox.destroy()


async def test_01_sandbox():
    with SandboxWrapper("_test_sandbox") as wrapper:
        with open(os.path.join("_test_sandbox", "hello_world.py"), "w") as f:
            f.write("print(\"Hello, World\")")

        result = await wrapper.sandbox.run("python hello_world.py", "", -1, -1)

        assert result.stdout.strip() == "Hello, World"


async def test_02_time_limit():
    with SandboxWrapper("_test_sandbox") as wrapper:
        with open(os.path.join("_test_sandbox", "tl.py"), "w") as f:
            f.write("n = 1\nfor i in range(1, 10000000):\n    n *= i\nprint(n)")

        result = await wrapper.sandbox.run("python tl.py", "", 1, 256)

        assert result.return_code == (TL_EXIT_CODE := 171)


async def test_03_memory_limit():
    with SandboxWrapper("_test_sandbox") as wrapper:
        with open(os.path.join("_test_sandbox", "ml.py"), "w") as f:
            f.write("a = bytearray(512000000)\nprint(a)")

        result = await wrapper.sandbox.run("python ml.py", "", 5, 256)

        assert result.return_code == (ML_EXIT_CODE := 170)
