import textwrap
from pathlib import Path


def define_env(env):
    @env.macro
    def indent_snippet(path, indent):
        contents = Path(path).read_text()
        return textwrap.indent(contents, indent)
