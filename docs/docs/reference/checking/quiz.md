---
toc-depth: 4
---

# Checker declaration

Checker declaration is described in JSON:

=== "Schema"

    Schema defined in pseudo-pydantic:

    ```py
    Checker:
        args: dict[str, Any]
        type: str
    ```

=== "Example 1"

    ```json
    {
      "args": {
        "pattern": "123"
      },
      "type": "text"
    }
    ```

=== "Example 2"

    ```json
    {
      "args": {
        "pattern": "print\\W*\\(\\W*a\\W*\\+\\W*b\\W*\\)"
      },
      "type": "regex"
    }
    ```

# Available validators

## `text`

Validator args:

### `pattern`

> string, required

Expected answer to match.

### `case_insensitive`

> bool, optional
>
> default: false

If enabled, case is ignored.

### `strict_match`

> bool, optional
>
> default: true

If disabled, final score will be decided
based on Levenshtein distance between
submitted answer and expected answer.

This means that participants still can
get some amout of points even if they get
the answer wrong.

## `regex`

Validator args:

### `pattern`

> string, required, regex

Regex pattern to match.


