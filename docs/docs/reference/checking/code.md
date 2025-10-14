---
toc-depth: 4
---

# Checker declaration

Checker declaration is described in JSON:

=== "Schema"

    Schema defined in pseudo-pydantic:

    ``` python
    groups: list[TestGroup]
    # List of groups to run
    precompile: list[PrecompileChecker]
    # List of precompile checkers to run
    time_limit: float
    # Default time limit for a test in seconds
    mem_limit_mb: float
    # Default memory limit for a test in MiB
    compile_timeout: int = 5
    # Compilation timeout threshold in seconds
    place_files: dict[str, str] = {}  
    # List of files to supply to environment (path=content)
    public_cases: list[PublicCase] = []  
    # Test cases to display publicly
    envs: dict[str, str] = {}  
    # Additional environment variables

    TestGroup:
        name: str
        # Name of the test group
        depends_on: list[str] = []
        # List of group names on which this group depends.
        # If one of dependency fails, this group will not be run.
        points: int
        # How many points you can get for this group
        scoring_rule: "polar" | "graded" = "graded"
        # See "Scoring rules"
        cases: list[TestCase]
        # List of test cases to run

    TestCase:
        validators: list[Validator]
        # See "Avaliable validators"
        stdin: str
        # Standard input
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



# Available validators

## `stdout`

Checks contents of standard output.

Validator args:

### `pattern`

> string, required

Expected answer to match.

### `strip`

> bool, optional
> 
> default: true

Whether to ignore whitespace (` `, `\n`, `\t`, etc.) symbols.


## `file`

Checks contents of a specified file.

Validator args:

### `filename`

> string, required

File to validate.

### `pattern`

> string, required

Expected answer to match.

### `strip`

> bool, optional
> 
> default: true

Whether to ignore whitespace (` `, `\n`, `\t`, etc.) symbols.



# Available precompile checkers

## `has_pattern`

Only pass if all patterns are present in solution.

Checker args:

### `patterns`

> `dict[str, list[str]]`, i.e. mapping of string to a list of strings, required

A mapping of file extension to a list of regex patterns that should be tested in
files of this extension.


## `no_pattern`

Only pass if none of the patterns are present in solution.

Checker args:

### `patterns`

> `dict[str, list[str]]`, i.e. mapping of string to a list of strings, required

A mapping of file extension to a list of regex patterns that should be tested in
files of this extension.


## `no_import`

No checker args.

Only pass if there are no `import` statements.
