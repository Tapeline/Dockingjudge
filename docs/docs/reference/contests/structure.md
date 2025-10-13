# Contest structure

{{ decorated_definition("Contest") }}

Each <term:contest> consists of a handful of <term:page|pages>[^1]. 
One page is always associated with exaclty one contest. 

Pages in contest are ordered, and stored in an ordered way under `pages` attribute:

=== "Schema"

    ```python
    list[Page]

    Page:
        id: int
        type: "quiz" | "code" | "text"
    ```

=== "Example"

    ```json
    [
        {"type": "text", "id": 13},
        {"type": "quiz", "id": 48},
        {"type": "code", "id": 7}
    ]
    ```

By changing order of pages in this field, you can change how pages will appear in
sidebar and standings table.

When a page is created, it gets automatically appended to this list. 
When a page is deleted, it gets automatically removed from this list.

!!! attention
    Users will only see pages that are listed under `pages` attribute.
    Keep the list of pages in sync with actual pages collection of a contest,
    i.e. do not manually remove pages from this attribute.

[^1]: 
    Learn more about [quiz task](../pages/quiz.md), [code task](../pages/code.md)
    and [text](../pages/text.md) pages.

