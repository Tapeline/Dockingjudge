import textwrap
import json
from pathlib import Path
from typing import Final

from openapidocs.mk.v3 import OpenAPIV3DocumentationHandler

_GLOSSARY: Final = "docs/reference/glossary.md"


def _read_glossary(glossary_path: str) -> dict[str, str]:
    md_text = Path(glossary_path).read_text()
    lines = md_text.splitlines()
    terms = {}
    i = 0
    current_term = None
    current_term_lines = []
    while i < len(lines):
        if lines[i].startswith("**term:"):
            if current_term_lines:
                terms[current_term] = "\n".join(current_term_lines)
                current_term = None
                current_term_lines.clear()
            current_term = lines[i].removeprefix("**term:").removesuffix("**")
        elif lines[i] == "" or lines[i].startswith(" "):
            current_term_lines.append(lines[i].strip())
        elif lines[i].startswith(":"):
            current_term_lines.append(lines[i][1:].strip())
        else:
            if current_term_lines:
                terms[current_term] = "\n".join(current_term_lines)
                current_term = None
                current_term_lines.clear()
        i += 1
    if current_term_lines:
        terms[current_term] = "\n".join(current_term_lines)
    return terms


def define_env(env):
    terms = _read_glossary(_GLOSSARY)

    @env.macro
    def indent_snippet(path, indent):
        contents = Path(path).read_text()
        return textwrap.indent(contents, indent)

    @env.macro
    def definition(term: str, indent: str = ""):
        if term not in terms:
            return textwrap.indent("Definition not found.", indent)
        return textwrap.indent(terms[term], indent)

    @env.macro
    def decorated_definition(term: str, indent: str = ""):
        if term not in terms:
            return textwrap.indent("> Definition not found.", indent)
        md = textwrap.indent(
            f"**{term}**\n\n{terms[term]}",
            "> "
        )
        return textwrap.indent(md, indent)

    @env.macro
    def openapi_json(path):
        return OpenAPIV3DocumentationHandler(
            json.loads(Path(path).read_text()),
            style="MKDOCS",
        ).write()
