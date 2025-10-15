# Code tasks

![](../../img/ui-edit-code.png)

## How to create a code task

1. Press a button for adding a code task in **Settings**
2. Write a name and a statement
3. Write a [test suite declaration](../../reference/checking/code.md)

## Example data

- Name: `Addition`
- Statemtent:
  ``` markdown
  Write a program that sums two inputted numbers.
  
  ### Input data
  Two integer numbers $a$ and $b$ on two separate lines.
  
  ### Output data
  One integer number - sum of $a$ and $b$.
  ```
- Test suite:
  ``` json
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
      }
    ],
    "compile_timeout": 5
  }
  ```

> Learn more: 
> 
> - [Reference > Code page](../../reference/pages/code.md)
> - [Reference > Code solutions](../../reference/solutions/code.md)
> - [Reference > Code validators](../../reference/checking/code.md)
