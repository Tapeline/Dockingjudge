# Common agreements

## Schema

Schema of a JSON or a YAML content is described this way:

- a list of top-level key-value pairs
- then all sub-schemas

Each key-value pair is described as:

``` python 
key: type = default_value
# Optional description
```

If a key has a default value, this means that it's optional, otherwise
it's required.

Types (including, but not limited to):

| Type                | Description                                                     |
|---------------------|-----------------------------------------------------------------|
| `int`               | An integer                                                      |
| `float`             | A floating-point number                                         |
| `bool`              | A boolean value                                                 |
| `str`               | A string (text)                                                 |
| `None`              | Not set, `null`                                                 |
| `list[T]`           | A list of items of `T` type                                     |
| `dict[K, V]`        | An object/dictionary of keys of `K` type and values of `V` type |
| `Optional[T]` or `T | None` | Optional: not set/null or a value of `T` type         |
| `A | B`             | Either value of `A` type or `B` type                            |
| `X | Y`            | Either value `X` or `Y`. E.g. `"code" | "quiz"` can only accept "code" or "quiz"|
| `Any` | Any value |

