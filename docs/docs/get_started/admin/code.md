# Code tasks

![](../../img/ui-edit-code.png)

## Checker declaration

Checker declaration is described in JSON:

=== "Schema"

    Schema defined in pseudo-pydantic:

    ```py
    Checker:
        groups: list[TestGroup]
        precompile: list[PrecompileChecker]
        time_limit: float
        mem_limit_mb: float
        compile_timeout: int = 5
        place_files: dict[str, str] = {}  # list of files to supply to environment (path=content)
        public_cases: list[PublicCase] = []  # test cases to display publicly
        envs: dict[str, str] = {}  # additional environment vars

    TestGroup:
        name: str
        depends_on: list[str] = []
        # List of group names on which this group depends.
        # If one of dependency fails, this group will not be run.
        points: int
        scoring_rule: "polar" | "graded" = "graded"
        cases: list[TestCase]

    TestCase:
        validators: list[Validator]
        stdin: str
        files_in: dict = {}  # list of files to supply to environment (path=content)
        files_out: list = []  # list of files to require back from solution
        time_limit: Optional[float] = None
        mem_limit_mb: Optional[float] = None

    Validator:
        type: str
        args: dict[str, Any]

    PrecompileChecker:
        type: str
        args: dict[str, Any] = {}

    PublicCase:
        in: str
        out: str
    ```

=== "Example"

    ```json
    {
      "groups": [
        {
          "name": "A",
          "cases": [
            {
              "stdin": "2\n3\n",
              "validators": [
                {
                  "args": {
                    "expected": "5"
                  },
                  "type": "stdout"
                }
              ]
            },
            {
              "stdin": "10\n20\n",
              "validators": [
                {
                  "args": {
                    "expected": "30"
                  },
                  "type": "stdout"
                }
              ]
            }
          ],
          "points": 100,
          "depends_on": [],
          "scoring_rule": "graded"
        }
      ],
      "precompile": [],
      "time_limit": 2,
      "mem_limit_mb": 256,
      "public_cases": [
        {
          "in": "2\n3",
          "out": "5"
        },
        {
          "in": "10\n20",
          "out": "30"
        }
      ],
      "compile_timeout": 5
    }
    ```

## Available validators

### `stdout`

Validator args:

```py
expected: str
strip: bool = True
```

### `file`

Validator args:

```py
filename: str
expected: str
strip: bool = True
```

## Available precompile checkers

### `has_pattern`

Checker args:

```py
patterns: dict[
    str,  # compiler name
    list[str],  # regex patterns
]
```

Only pass if all patterns are present in solution.

### `no_pattern`

Checker args:

```py
patterns: dict[
    str,  # compiler name
    list[str],  # regex patterns
]
```

Only pass if all patterns are not present in solution.

### `no_import`

No checker args.

Only pass if there are no `import` statements.
